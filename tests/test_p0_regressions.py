import re
from unittest.mock import patch

import pytest


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_chart_data_rejects_non_finite_numbers(value):
    from tkinter_dash.data import normalize_xy

    with pytest.raises(ValueError, match="finite"):
        normalize_xy({"A": value})


def test_system_theme_is_not_supported():
    from tkinter_dash.theme import resolve_theme

    with pytest.raises(ValueError, match="light.*dark"):
        resolve_theme("system")


@pytest.mark.parametrize("chart_name", ["PieChart", "DonutChart", "ScatterChart"])
def test_single_series_charts_reject_multi_series_data(chart_name):
    import tkinter as tk
    import tkinter_dash as td

    root = tk.Tk()
    try:
        chart_class = getattr(td, chart_name)
        data = {
            "Revenue": {"Q1": 10, "Q2": 20},
            "Cost": {"Q1": 5, "Q2": 8},
        }
        with pytest.raises(ValueError, match="one series only"):
            chart_class(root, data, animate=False)
    finally:
        root.destroy()


def test_destroy_cancels_animation_configure_and_tooltip_callbacks():
    import tkinter as tk
    from tkinter_dash import LineChart

    root = tk.Tk()
    chart = LineChart(
        root,
        {"A": 10, "B": 20, "C": 15},
        animate=True,
        duration=1000,
        tooltip=True,
    )
    chart.pack(fill="both", expand=True)
    root.update_idletasks()
    root.update()

    chart._show_custom_tooltip(10, 10, "A", "10")
    assert chart._tooltip is not None

    # Force a pending configure debounce timer as well as the animation timer.
    chart._on_configure(None)
    assert chart._animation_after_id is not None
    assert chart._configure_id is not None

    chart.destroy()

    assert chart._destroyed is True
    assert chart._animation_after_id is None
    assert chart._configure_id is None
    assert chart._tooltip is None

    # Canceled callbacks must not fire after destruction.
    root.after(50, root.quit)
    root.mainloop()
    root.destroy()


def test_rapid_updates_cancel_previous_animation():
    import tkinter as tk
    from tkinter_dash import LineChart

    root = tk.Tk()
    chart = LineChart(root, {"A": 1, "B": 2}, animate=True, duration=500)
    chart.pack()
    root.update_idletasks()
    root.update()

    first_id = chart._animation_after_id
    assert first_id is not None

    chart.update({"A": 3, "B": 4}, animate=True)
    second_id = chart._animation_after_id
    assert second_id is not None
    assert second_id != first_id

    chart.update({"A": 5, "B": 6}, animate=True)
    third_id = chart._animation_after_id
    assert third_id is not None
    assert third_id != second_id

    root.after(50, root.quit)
    root.mainloop()
    assert chart._progress < 1.0

    chart.destroy()
    root.destroy()


def test_rapid_update_to_non_animated_data_finishes_cleanly():
    import tkinter as tk
    from tkinter_dash import LineChart

    root = tk.Tk()
    chart = LineChart(root, {"A": 1, "B": 2}, animate=True, duration=500)
    chart.pack()
    root.update_idletasks()
    root.update()
    assert chart._animation_after_id is not None

    chart.update({"A": 10, "B": 20}, animate=False)
    assert chart._animation_after_id is None
    assert chart._progress == 1.0

    root.after(50, root.quit)
    root.mainloop()
    assert chart._progress == 1.0

    chart.destroy()
    root.destroy()


def _geometry_xy(geometry):
    match = re.search(r"[+-](\d+)[+-](\d+)$", geometry)
    assert match, geometry
    return int(match.group(1)), int(match.group(2))


def test_tooltip_is_clamped_to_screen_boundaries():
    import tkinter as tk
    from tkinter_dash import LineChart

    root = tk.Tk()
    root.geometry("300x220+0+0")
    chart = LineChart(root, {"A": 10, "B": 20}, animate=False, tooltip=True)
    chart.pack(fill="both", expand=True)
    root.update_idletasks()
    root.update()

    with patch.object(chart, "winfo_rootx", return_value=250), \
         patch.object(chart, "winfo_rooty", return_value=190), \
         patch.object(chart, "winfo_screenwidth", return_value=300), \
         patch.object(chart, "winfo_screenheight", return_value=220):
        chart._show_custom_tooltip(100, 100, "A", "10")
        root.update_idletasks()

    assert chart._tooltip is not None
    x, y = _geometry_xy(chart._tooltip.geometry())
    tooltip_width = chart._tooltip.winfo_width()
    tooltip_height = chart._tooltip.winfo_height()
    assert 0 <= x <= 300 - tooltip_width
    assert 0 <= y <= 220 - tooltip_height

    chart.destroy()
    root.destroy()
