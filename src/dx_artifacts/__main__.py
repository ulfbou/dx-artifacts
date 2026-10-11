"""Module and installed-console entry point."""
from __future__ import annotations

import sys
from pathlib import Path


def _repository_main():
    try:
        from dx_artifacts._standalone_runtime import load_main
    except ModuleNotFoundError:
        root = Path(__file__).resolve().parents[2]
        source = root / "dx.py"
        if not source.is_file():
            raise RuntimeError("DX command runtime is unavailable")
        namespace = {
            "__file__": str(source),
            "__name__": "dx_artifacts._repository_runtime",
            "__package__": None,
        }
        exec(compile(source.read_bytes(), str(source), "exec"), namespace)
        return namespace["main"]
    return load_main()


def console_main() -> None:
    raise SystemExit(_repository_main()())


if __name__ == "__main__":
    console_main()
