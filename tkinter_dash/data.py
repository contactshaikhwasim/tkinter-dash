from collections.abc import Mapping, Sequence
import math


def _number(value):
    if isinstance(value, bool):
        raise TypeError("boolean values are not valid chart data")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise TypeError(f"chart value {value!r} is not numeric") from exc
    if not math.isfinite(number):
        raise ValueError(f"chart value {value!r} must be finite")
    return number


def normalize_xy(data):
    """Return labels and numeric values from mapping or (label, value) pairs."""
    if data is None:
        return [], []
    if isinstance(data, Mapping):
        labels = list(data.keys())
        values = [_number(value) for value in data.values()]
        return labels, values

    try:
        items = list(data)
    except TypeError as exc:
        raise TypeError("data must be a mapping or a sequence of (label, value) pairs") from exc

    labels = []
    values = []
    for item in items:
        if not isinstance(item, Sequence) or isinstance(item, (str, bytes)) or len(item) != 2:
            raise ValueError("sequence data items must be (label, value) pairs")
        labels.append(item[0])
        values.append(_number(item[1]))
    return labels, values


def normalize_series(data):
    """Normalize and validate chart input into {series: (labels, values)}."""
    if not isinstance(data, Mapping) or not data:
        labels, values = normalize_xy(data)
        if not values:
            raise ValueError("chart data cannot be empty")
        validate_non_empty(labels, values)
        return {"Value": (labels, values)}

    values = list(data.values())
    if not all(isinstance(item, Mapping) for item in values):
        labels, numeric = normalize_xy(data)
        if not numeric:
            raise ValueError("chart data cannot be empty")
        validate_non_empty(labels, numeric)
        return {"Value": (labels, numeric)}

    series = {}
    for name, mapping in data.items():
        labels, numeric = normalize_xy(mapping)
        if not numeric:
            raise ValueError(f"series {name!r} cannot be empty")
        validate_non_empty(labels, numeric)
        series[str(name)] = (labels, numeric)

    first_labels = next(iter(series.values()))[0]
    for name, (labels, _) in series.items():
        if labels != first_labels:
            raise ValueError(f"series {name!r} must use the same labels as the first series")
    return series


def validate_non_empty(labels, values):
    if not values:
        raise ValueError("chart data cannot be empty")
    if len(labels) != len(values):
        raise ValueError("labels and values must have the same length")


def value_range(values):
    low = min(values)
    high = max(values)
    if low == high:
        pad = 1 if low == 0 else abs(low) * 0.1
        return low - pad, high + pad
    pad = (high - low) * 0.08
    return low - pad, high + pad
