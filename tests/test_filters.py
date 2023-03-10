from app.filters import format_float


def test_format_float():
    assert format_float(None) == ""
    assert format_float("") == ""
    assert format_float("", default="-") == "-"
    assert format_float(0.1) == "0.1"
    assert format_float(10) == "10"
    assert format_float(10, digits=0) == "10"
    assert format_float(10, digits=4) == "10.0000"
