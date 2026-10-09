from io import StringIO
import importlib.util
from pathlib import Path
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("accepted_dx", ROOT / "dx.py")
dx = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = dx
spec.loader.exec_module(dx)


def test_v2_and_legacy_versions_parse():
    assert dx.parse(StringIO("%%DX v2.0.0\n%%END\n"))[0] == "v2.0.0"
    assert dx.parse(StringIO("%%DX v1.3.1\n%%END\n"))[0] == "v1.3.1"


@pytest.mark.parametrize(
    "text,marker",
    [
        ("%%END\n", "missing %%DX header"),
        ("%%DX v9\n%%END\n", "unsupported DX version"),
        ("%%DX v2.0.0\n", "missing %%END"),
        ("%%DX v2.0.0\n%%END\nextra\n", "content after %%END"),
        (
            '%%DX v2.0.0\n%%FILE readonly="true"\n%%ENDBLOCK\n%%END\n',
            "FILE without path",
        ),
    ],
)
def test_invalid_structures(text, marker):
    with pytest.raises(dx.InvalidCarrierError, match=marker):
        dx.parse(StringIO(text))


def test_note_not_file():
    version, entries, notes = dx.parse(
        StringIO("%%DX v2.0.0\n%%NOTE\nx\n%%ENDBLOCK\n%%END\n")
    )
    assert version == "v2.0.0"
    assert entries == []
    assert notes == 1
