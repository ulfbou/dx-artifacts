from io import StringIO
import importlib.util
from pathlib import Path
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("accepted_dx_extended", ROOT / "dx.py")
dx = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = dx
spec.loader.exec_module(dx)


def parse(text: str):
    return dx.parse(StringIO(text))


@pytest.mark.parametrize(
    "text, marker",
    [
        ("%%DX v2.0.0\n%%DX v2.0.0\n%%END\n", "multiple %%DX headers"),
        ('%%DX v2.0.0\n%%FILE path="a"\n%%ENDBLOCK\n%%FILE path="a"\n%%ENDBLOCK\n%%END\n', "duplicate path"),
        ('%%DX v2.0.0\n%%FILE path="../a"\n%%ENDBLOCK\n%%END\n', "unsafe carrier path"),
        ('%%DX v2.0.0\n%%FILE path="a" nope="x"\n%%ENDBLOCK\n%%END\n', "unsupported attribute"),
        ('%%DX v2.0.0\n%%FILE path="a" readonly="yes"\n%%ENDBLOCK\n%%END\n', "readonly must be"),
        ('%%DX v2.0.0\n%%FILE path="a" escaped="yes"\n%%ENDBLOCK\n%%END\n', "escaped must be"),
        ('%%DX v2.0.0\n%%FILE path="a" encoding="hex"\n%%ENDBLOCK\n%%END\n', "unsupported encoding"),
        ('%%DX v2.0.0\n%%FILE path="a" encoding="base64" escaped="true"\n%%ENDBLOCK\n%%END\n', "only valid for text"),
        ('%%DX v2.0.0\n%%FILE path="a" encoding="base64" trailing_newlines="1"\n%%ENDBLOCK\n%%END\n', "only valid for text"),
        ('%%DX v2.0.0\n%%FILE path="a" trailing_newlines="-1"\n%%ENDBLOCK\n%%END\n', "non-negative"),
        ('%%DX v2.0.0\n%%FILE path="a" encoding="base64"\n%%%\n%%ENDBLOCK\n%%END\n', "invalid base64"),
        ('%%DX v2.0.0\n%%FILE path="a"\n', "unterminated file block"),
        ('%%DX v2.0.0\n%%NOTE\nx\n', "unterminated NOTE block"),
    ],
)
def test_extended_invalid_carriers(text, marker):
    with pytest.raises((dx.InvalidCarrierError, ValueError), match=marker):
        parse(text)


def test_readonly_and_trailing_newlines_are_retained():
    _, entries, _ = parse(
        '%%DX v2.0.0\n%%FILE path="a.txt" readonly="true" trailing_newlines="2"\nx\n%%ENDBLOCK\n%%END\n'
    )
    assert len(entries) == 1
    assert entries[0].readonly is True
    assert entries[0].data == b"x\n\n"
