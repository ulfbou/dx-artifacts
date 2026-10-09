from __future__ import annotations
from pathlib import Path
import subprocess, sys
import pytest

ROOT = Path(__file__).resolve().parents[1]
DX = ROOT / "dx.py"

@pytest.fixture
def run_dx(tmp_path):
    def run(*args: str, cwd: Path | None = None, input_bytes: bytes | None = None):
        return subprocess.run([sys.executable, str(DX), *args], cwd=cwd or tmp_path, input=input_bytes, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    return run
