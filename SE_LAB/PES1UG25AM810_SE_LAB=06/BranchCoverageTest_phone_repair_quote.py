import pytest
from phone_repair_quote import repair_quote, repair_days, trade_in_value


# repair_quote branches

def test_invalid_part():
    with pytest.raises(ValueError):
        repair_quote("speaker", "budget", False, False)


def test_invalid_brand():
    with pytest.raises(ValueError):
        repair_quote("battery", "premium", False, False)


def test_budget_part():
    assert repair_quote("battery", "budget", False, False) == 1800


def test_flagship_part():
    assert repair_quote("battery", "flagship", False, False) == 3300


def test_screen_labour():
    assert repair_quote("screen", "budget", False, False) == 4600


def test_non_screen_labour():
    assert repair_quote("camera", "budget", False, False) == 2800


def test_warranty_true():
    assert repair_quote("battery", "budget", True, False) == 300


def test_warranty_false():
    assert repair_quote("battery", "budget", False, False) == 1800


def test_express_true():
    assert repair_quote("battery", "budget", False, True) == 2300


def test_express_false():
    assert repair_quote("battery", "budget", False, False) == 1800


# repair_days branches

def test_technician_free():
    assert repair_days("battery", True, 1) == 1


def test_technician_not_free():
    assert repair_days("battery", True, 0) == 3


def test_parts_in_stock():
    assert repair_days("battery", True, 1) == 1


def test_screen_not_in_stock():
    assert repair_days("screen", False, 1) == 6


def test_camera_not_in_stock():
    assert repair_days("camera", False, 1) == 6


def test_other_part_not_in_stock():
    assert repair_days("battery", False, 1) == 3


# trade_in_value branches

def test_invalid_price():
    with pytest.raises(ValueError):
        trade_in_value(0, 12, False)


def test_invalid_age():
    with pytest.raises(ValueError):
        trade_in_value(10000, -1, False)


def test_over_48_months():
    assert trade_in_value(10000, 49, False) == 0


def test_up_to_12_months():
    assert trade_in_value(10000, 12, False) == 6000


def test_13_to_24_months():
    assert trade_in_value(10000, 24, False) == 4000


def test_25_to_48_months():
    assert trade_in_value(10000, 36, False) == 2000


def test_screen_cracked():
    assert trade_in_value(10000, 12, True) == 3000


def test_screen_not_cracked():
    assert trade_in_value(10000, 12, False) == 6000