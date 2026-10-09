from __future__ import annotations

from io import BytesIO
from pathlib import Path

import pytest

from dx_artifacts.sinks import (
    CheckSink,
    FilesystemSink,
    SinkConflictError,
    StdoutSink,
)


def test_stdout_sink_publishes_exact_bytes():
    payload = b"\x00alpha\r\nomega\xff"
    source = BytesIO(payload)
    destination = BytesIO()

    result = StdoutSink(destination).publish(source)

    assert destination.getvalue() == payload
    assert result.sink == "stdout"
    assert result.bytes_written == len(payload)
    assert result.completed is True
    assert result.destination is None


def test_filesystem_sink_publishes_exact_bytes(tmp_path):
    payload = b"\x00alpha\r\nomega\xff"
    output = tmp_path / "artifact.dx.txt"

    result = FilesystemSink(output).publish(BytesIO(payload))

    assert output.read_bytes() == payload
    assert result.sink == "filesystem"
    assert result.bytes_written == len(payload)
    assert result.completed is True
    assert result.destination == output
    assert list(tmp_path.glob(output.name + ".tmp.*")) == []


def test_filesystem_sink_requires_explicit_replace(tmp_path):
    output = tmp_path / "artifact.dx.txt"
    output.write_bytes(b"original")

    with pytest.raises(
        SinkConflictError,
        match="use --force",
    ):
        FilesystemSink(output).publish(BytesIO(b"replacement"))

    assert output.read_bytes() == b"original"

    result = FilesystemSink(
        output,
        replace=True,
    ).publish(BytesIO(b"replacement"))

    assert result.completed is True
    assert output.read_bytes() == b"replacement"


def test_filesystem_sink_rejects_destination_symlink(tmp_path):
    target = tmp_path / "target.dx.txt"
    target.write_bytes(b"target")

    output = tmp_path / "output.dx.txt"

    try:
        output.symlink_to(target)
    except (NotImplementedError, OSError):
        pytest.skip("symlinks are unavailable")

    with pytest.raises(
        SinkConflictError,
        match="refusing to replace symlink",
    ):
        FilesystemSink(
            output,
            replace=True,
        ).publish(BytesIO(b"replacement"))

    assert target.read_bytes() == b"target"


def test_check_sink_consumes_without_publication(tmp_path):
    payload = b"complete artifact"
    source = BytesIO(payload)

    result = CheckSink().publish(source)

    assert result.sink == "check"
    assert result.bytes_written == len(payload)
    assert result.completed is True
    assert result.destination is None
    assert list(tmp_path.iterdir()) == []
