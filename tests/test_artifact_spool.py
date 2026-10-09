from __future__ import annotations

import pytest

from dx_artifacts._spool import ArtifactSpool


def test_spool_is_seekable_and_returns_complete_bytes():
    with ArtifactSpool(max_memory_bytes=1024) as spool:
        assert spool.write(b"alpha") == 5
        assert spool.tell() == 5

        spool.rewind()
        assert spool.read(2) == b"al"
        assert spool.tell() == 2

        assert spool.complete_bytes() == b"alpha"
        assert spool.tell() == 2
        assert spool.byte_length() == 5
        assert spool.tell() == 2


def test_spool_spills_beyond_memory_threshold_without_byte_drift():
    payload = b"0123456789abcdef"

    with ArtifactSpool(max_memory_bytes=4) as spool:
        spool.write(payload)

        assert spool.rolled_to_disk is True
        assert spool.complete_bytes() == payload


def test_spool_rejects_text_and_negative_threshold():
    with pytest.raises(ValueError, match="non-negative"):
        ArtifactSpool(max_memory_bytes=-1)

    with ArtifactSpool() as spool:
        with pytest.raises(TypeError, match="bytes only"):
            spool.write("text")  # type: ignore[arg-type]


def test_spool_closes_deterministically():
    spool = ArtifactSpool()
    spool.write(b"x")
    spool.close()

    assert spool.closed is True

    with pytest.raises(ValueError, match="closed"):
        spool.read()
