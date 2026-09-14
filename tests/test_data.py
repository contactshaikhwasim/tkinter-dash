import pytest

from tkinter_dash.data import normalize_xy, value_range


def test_normalize_mapping():
    assert normalize_xy({"Jan": 10, "Feb": 20}) == (["Jan", "Feb"], [10.0, 20.0])


def test_normalize_pairs():
    assert normalize_xy([("Jan", 10), ("Feb", "20")]) == (["Jan", "Feb"], [10.0, 20.0])


def test_reject_bad_pairs():
    with pytest.raises(ValueError):
        normalize_xy([("Jan", 10, "extra")])


def test_reject_booleans():
    with pytest.raises(TypeError):
        normalize_xy({"Jan": True})


def test_value_range_has_padding():
    low, high = value_range([10, 20])
    assert low < 10
    assert high > 20


def test_normalize_multi_series():
    from tkinter_dash.data import normalize_series
    result = normalize_series({
        "Revenue": {"Q1": 10, "Q2": 20},
        "Cost": {"Q1": 7, "Q2": 12},
    })
    assert result["Revenue"][0] == ["Q1", "Q2"]
    assert result["Cost"][1] == [7.0, 12.0]


def test_reject_mismatched_multi_series_labels():
    from tkinter_dash.data import normalize_series
    with pytest.raises(ValueError):
        normalize_series({
            "Revenue": {"Q1": 10},
            "Cost": {"Q2": 5},
        })
