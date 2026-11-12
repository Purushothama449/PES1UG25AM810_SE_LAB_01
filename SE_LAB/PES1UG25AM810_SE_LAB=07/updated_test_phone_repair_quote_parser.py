
from hypothesis import given, strategies as st
from phone_repair_quote_parser import (
    mask_imei,
    parse_parts_order,
    parse_model
)


@given(st.text() | st.none())
def test_mask_imei_no_crash(s):
    try:
        result = mask_imei(s)
        assert isinstance(result, str)
    except Exception as e:
        assert False, f"mask_imei crashed with {s!r}: {e}"


@given(st.text() | st.none())
def test_parse_parts_order_no_crash(s):
    try:
        result = parse_parts_order(s)
        assert isinstance(result, dict)
    except Exception as e:
        assert False, f"parse_parts_order crashed with {s!r}: {e}"


@given(st.text() | st.none())
def test_parse_model_no_crash(s):
    try:
        result = parse_model(s)
        assert isinstance(result, tuple)
        assert len(result) == 2
    except Exception as e:
        assert False, f"parse_model crashed with {s!r}: {e}"
