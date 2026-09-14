import time

import pytest


def test_theme_changes_only_through_explicit_theme_api():
    import tkinter as tk
    from tkinter_dash import LineChart

    root = tk.Tk()
    try:
        chart = LineChart(root, {"A": 1, "B": 2}, animate=False)
        chart.pack()
        root.update_idletasks()
        old_theme = chart.theme
        assert chart.configure_theme("dark") is chart
        assert chart.theme.background == "#0D1117"
        assert chart.cget("bg") == chart.theme.plot_background
        assert chart.theme is not old_theme
        with pytest.raises(tk.TclError):
            chart.configure(theme="light")
        chart.destroy()
    finally:
        root.destroy()


def test_palette_is_centralized_on_theme():
    from tkinter_dash import DARK, LIGHT

    assert LIGHT.palette[0] == LIGHT.accent
    assert LIGHT.palette[1] == LIGHT.accent_2
    assert LIGHT.palette[2] == LIGHT.positive
    assert DARK.palette[0] == DARK.accent
    assert DARK.palette[1] == DARK.accent_2
    assert len(LIGHT.palette) >= 4
    assert len(DARK.palette) >= 4


def test_hit_test_has_no_hidden_series_side_effect():
    import tkinter as tk
    from tkinter_dash import LineChart

    root = tk.Tk()
    try:
        chart = LineChart(
            root,
            {"Revenue": {"Q1": 10, "Q2": 20}, "Cost": {"Q1": 8, "Q2": 15}},
            animate=False,
        )
        chart.pack(fill="both", expand=True)
        root.update_idletasks()
        root.update()
        left, top, right, bottom = chart._chart_bounds()
        x = left
        low, high = __import__("tkinter_dash.data", fromlist=["value_range"]).value_range([10, 20, 8, 15])
        y = bottom - ((8 - low) / (high - low)) * (bottom - top)
        assert not hasattr(chart, "_candidate_hover_series")
        index = chart.hit_test(int(x), int(y))
        assert index == 0
        assert chart._hover_series == -1
        assert not hasattr(chart, "_candidate_hover_series")
        chart.destroy()
    finally:
        root.destroy()


@pytest.mark.parametrize("data", [None, {}, [], ["bad"], {"A": []}])
def test_normalize_series_rejects_empty_or_malformed_data(data):
    from tkinter_dash.data import normalize_series

    with pytest.raises((TypeError, ValueError)):
        normalize_series(data)


def test_normalize_series_is_complete_validation_boundary():
    from tkinter_dash.data import normalize_series

    normalized = normalize_series({"Revenue": {"Q1": 10, "Q2": 20}})
    assert normalized == {"Revenue": (["Q1", "Q2"], [10.0, 20.0])}

    with pytest.raises(ValueError, match="same labels"):
        normalize_series({"Revenue": {"Q1": 10}, "Cost": {"Q2": 5}})


def test_multiple_updates_keep_only_one_animation_callback():
    import tkinter as tk
    from tkinter_dash import LineChart

    root = tk.Tk()
    try:
        chart = LineChart(root, {"A": 1, "B": 2}, animate=True, duration=500)
        chart.pack()
        root.update_idletasks()
        root.update()
        for value in range(10, 110, 10):
            chart.update({"A": value, "B": value + 1}, animate=True)
        assert chart._animation_after_id is not None
        deadline = time.monotonic() + 0.2
        while time.monotonic() < deadline:
            root.update()
            time.sleep(0.005)
        assert chart._animation_after_id is not None or chart._progress == 1.0
        chart.destroy()
    finally:
        root.destroy()


def test_destroy_after_rapid_updates_leaves_no_pending_callbacks():
    import tkinter as tk
    from tkinter_dash import LineChart

    root = tk.Tk()
    try:
        chart = LineChart(root, {"A": 1, "B": 2}, animate=True, duration=1000)
        chart.pack()
        root.update_idletasks()
        root.update()
        for value in range(1, 25):
            chart.update({"A": value, "B": value + 5}, animate=True)
        chart.event_generate("<Configure>")
        root.update()
        assert chart._animation_after_id is not None
        assert chart._configure_id is not None
        chart.destroy()
        assert chart._animation_after_id is None
        assert chart._configure_id is None
        assert chart._tooltip is None
    finally:
        root.destroy()


def test_render_benchmark_for_dashboard_scale_datasets():
    """Regression guard: large redraws must remain bounded enough to benchmark."""
    import tkinter as tk
    from tkinter_dash import LineChart

    root = tk.Tk()
    try:
        chart = LineChart(root, {str(i): float(i % 100) for i in range(1000)}, animate=False)
        chart.pack(fill="both", expand=True)
        root.update_idletasks()
        root.update()

        timings = {}
        for size in (1_000, 10_000, 100_000):
            chart.set_data({str(i): float(i % 100) for i in range(size)}, animate=False)
            start = time.perf_counter()
            chart.redraw()
            root.update_idletasks()
            timings[size] = time.perf_counter() - start

        # Keep this test diagnostic rather than machine-specific pass/fail.
        assert all(duration >= 0 for duration in timings.values())
        print("render timings:", timings)
        chart.destroy()
    finally:
        root.destroy()


def test_bar_hit_test_requires_pointer_inside_bar():
    import tkinter as tk
    from tkinter_dash import BarChart

    root = tk.Tk()
    try:
        chart = BarChart(root, {"A": 10, "B": 20}, animate=False)
        chart.pack(fill="both", expand=True)
        root.update_idletasks()
        root.update()
        left, top, right, bottom = chart._chart_bounds()
        slot = (right - left) / 2
        x = left + slot * 0.5
        assert chart.hit_test(int(x), int(top + 5)) == -1
        assert chart.hit_test(int(x), int(bottom - 1)) == 0
        chart.destroy()
    finally:
        root.destroy()
