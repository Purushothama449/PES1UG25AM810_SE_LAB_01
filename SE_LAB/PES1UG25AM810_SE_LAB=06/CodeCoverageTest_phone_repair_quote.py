import pytest
from phone_repair_quote import repair_quote, repair_days, trade_in_value


def test_budget_screen():
    assert repair_quote("screen", "budget", False, False) == 4600


def test_flagship_battery():
    assert repair_quote("battery", "flagship", False, False) == 3300


def test_other_part_labour():
    assert repair_quote("camera", "budget", False, False) == 2800


def test_warranty_non_screen():
    assert repair_quote("battery", "budget", True, False) == 300


def test_warranty_screen():
    assert repair_quote("screen", "budget", True, False) == 4600


def test_express_repair():
    assert repair_quote("charging_port", "budget", False, True) == 1600


def test_invalid_part():
    with pytest.raises(ValueError):
        repair_quote("speaker", "budget", False, False)


def test_invalid_brand():
    with pytest.raises(ValueError):
        repair_quote("battery", "premium", False, False)


def test_in_stock_quick():
    assert repair_days("battery", True, 2) == 1


def test_no_technician():
    assert repair_days("battery", True, 0) == 3


def test_no_parts_screen():
    assert repair_days("screen", False, 2) == 6


def test_no_parts_camera():
    assert repair_days("camera", False, 2) == 6


def test_no_parts_other():
    assert repair_days("battery", False, 2) == 3


def test_invalid_original_price():
    with pytest.raises(ValueError):
        trade_in_value(0, 12, False)


def test_invalid_age():
    with pytest.raises(ValueError):
        trade_in_value(5000, -1, False)


def test_over_48_months():
    assert trade_in_value(10000, 49, False) == 0


def test_age_12_months():
    assert trade_in_value(10000, 12, False) == 6000


def test_age_24_months():
    assert trade_in_value(10000, 24, False) == 4000


def test_age_36_months():
    assert trade_in_value(10000, 36, False) == 2000


def test_cracked_screen():
    assert trade_in_value(10000, 12, True) == 3000