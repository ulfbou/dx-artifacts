"""Internal artifact publication sinks.

These classes publish complete artifact bytes. They do not construct,
interpret, transform, or verify an artifact.
"""

from __future__ import annotations

import os
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Protocol


COPY_BUFFER_SIZE = 1024 * 1024


class ArtifactByteSource(Protocol):
    """Minimum seekable byte-source contract consumed by artifact sinks."""

    def seek(self, offset: int, whence: int = 0) -> int:
        ...

    def read(self, size: int = -1) -> bytes:
        ...


class SinkError(OSError):
    """Base class for artifact publication failures."""


class SinkConflictError(SinkError):
    """The selected filesystem destination cannot be replaced safely."""


@dataclass(frozen=True)
class DeliveryResult:
    """Internal result of one complete sink delivery."""

    sink: str
    bytes_written: int
    completed: bool
    destination: Path | None = None


def _copy_complete(
    source: ArtifactByteSource,
    destination: BinaryIO,
) -> int:
    source.seek(0)
    total = 0

    while True:
        chunk = source.read(COPY_BUFFER_SIZE)
        if not chunk:
            break

        written = destination.write(chunk)
        if written is None:
            written = len(chunk)

        if written != len(chunk):
            raise SinkError(
                "artifact sink accepted only part of an output chunk"
            )

        total += written

    return total


@dataclass(frozen=True)
class StdoutSink:
    """Publish exact artifact bytes to standard output."""

    stream: BinaryIO | None = None

    def publish(
        self,
        source: ArtifactByteSource,
    ) -> DeliveryResult:
        stream = (
            self.stream
            if self.stream is not None
            else sys.stdout.buffer
        )

        try:
            written = _copy_complete(source, stream)
            stream.flush()
        except BrokenPipeError:
            raise
        except OSError as exc:
            raise SinkError(str(exc)) from exc

        return DeliveryResult(
            sink="stdout",
            bytes_written=written,
            completed=True,
        )


@dataclass(frozen=True)
class FilesystemSink:
    """Publish through a temporary sibling and atomic replacement."""

    destination: Path
    replace: bool = False

    def publish(
        self,
        source: ArtifactByteSource,
    ) -> DeliveryResult:
        requested = self.destination

        if requested.is_symlink():
            raise SinkConflictError(
                f"refusing to replace symlink: {requested}"
            )

        parent = requested.parent
        parent.mkdir(parents=True, exist_ok=True)

        # Termux may expose shared storage through a directory symlink.
        # Resolve only the parent and continue to reject a symlink at the
        # destination object itself.
        destination = parent.resolve() / requested.name

        if destination.is_symlink():
            raise SinkConflictError(
                f"refusing to replace symlink: {requested}"
            )

        if destination.exists() and not self.replace:
            raise SinkConflictError(
                "output already exists; use --force to replace it: "
                f"{requested}"
            )

        fd: int | None = None
        temporary: Path | None = None

        try:
            fd, temporary_name = tempfile.mkstemp(
                prefix=destination.name + ".tmp.",
                dir=destination.parent,
            )
            temporary = Path(temporary_name)

            with os.fdopen(fd, "wb") as stream:
                fd = None
                written = _copy_complete(source, stream)
                stream.flush()
                os.fsync(stream.fileno())

            if destination.exists() and not self.replace:
                raise SinkConflictError(
                    "output already exists; use --force to replace it: "
                    f"{requested}"
                )

            if destination.is_symlink():
                raise SinkConflictError(
                    f"refusing to replace symlink: {requested}"
                )

            os.replace(temporary, destination)
            temporary = None

            return DeliveryResult(
                sink="filesystem",
                bytes_written=written,
                completed=True,
                destination=requested,
            )
        except SinkConflictError:
            raise
        except OSError as exc:
            raise SinkError(str(exc)) from exc
        finally:
            if fd is not None:
                os.close(fd)

            if temporary is not None:
                try:
                    temporary.unlink()
                except FileNotFoundError:
                    pass


@dataclass(frozen=True)
class CheckSink:
    """Consume complete artifact bytes without external publication."""

    def publish(
        self,
        source: ArtifactByteSource,
    ) -> DeliveryResult:
        source.seek(0)
        total = 0

        while True:
            chunk = source.read(COPY_BUFFER_SIZE)
            if not chunk:
                break
            total += len(chunk)

        return DeliveryResult(
            sink="check",
            bytes_written=total,
            completed=True,
        )
