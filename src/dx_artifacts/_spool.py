"""Internal seekable binary artifact spool."""

from __future__ import annotations

import tempfile
from types import TracebackType
from typing import BinaryIO


DEFAULT_SPOOL_THRESHOLD = 8 * 1024 * 1024


class ArtifactSpool:
    """Own one seekable binary spool containing complete artifact bytes."""

    def __init__(
        self,
        *,
        max_memory_bytes: int = DEFAULT_SPOOL_THRESHOLD,
    ) -> None:
        if max_memory_bytes < 0:
            raise ValueError("max_memory_bytes must be non-negative")

        self._stream: BinaryIO = tempfile.SpooledTemporaryFile(
            max_size=max_memory_bytes,
            mode="w+b",
        )
        self._closed = False

    @property
    def closed(self) -> bool:
        return self._closed

    @property
    def rolled_to_disk(self) -> bool:
        self._require_open()
        return bool(getattr(self._stream, "_rolled", False))

    def write(self, data: bytes) -> int:
        self._require_open()
        if not isinstance(data, bytes):
            raise TypeError("artifact spool accepts bytes only")
        return self._stream.write(data)

    def tell(self) -> int:
        self._require_open()
        return self._stream.tell()

    def seek(self, offset: int, whence: int = 0) -> int:
        self._require_open()
        return self._stream.seek(offset, whence)

    def rewind(self) -> None:
        self.seek(0)

    def read(self, size: int = -1) -> bytes:
        self._require_open()
        return self._stream.read(size)

    def byte_length(self) -> int:
        self._require_open()
        position = self.tell()
        self.seek(0, 2)
        length = self.tell()
        self.seek(position)
        return length

    def complete_bytes(self) -> bytes:
        self._require_open()
        position = self.tell()
        self.rewind()
        data = self.read()
        self.seek(position)
        return data

    def close(self) -> None:
        if not self._closed:
            self._stream.close()
            self._closed = True

    def _require_open(self) -> None:
        if self._closed:
            raise ValueError("artifact spool is closed")

    def __enter__(self) -> "ArtifactSpool":
        self._require_open()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()
