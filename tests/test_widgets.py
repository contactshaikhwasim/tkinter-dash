import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from tkinter_dash.data import normalize_xy


def get_tk():
    import tkinter as tk
    return tk


def test_all_widgets_create_resize_update():
    tk = get_tk()
    from tkinter_dash import BarChart, DonutChart, LineChart, PieChart, ScatterChart

    root = tk.Tk()
    try:
        root.geometry("700x500")
        root.update_idletasks()

        widgets = [
            LineChart(root, {"A": 10, "B": 20, "C": 15}, animate=False),
            BarChart(root, {"A": 10, "B": 20, "C": 15}, animate=False),
            ScatterChart(root, {"A": 10, "B": 20, "C": 15}, animate=False),
            PieChart(root, {"A": 40, "B": 30, "C": 30}, animate=False),
            DonutChart(root, {"A": 40, "B": 30, "C": 30}, animate=False),
        ]
        for widget in widgets:
            widget.configure(width=500, height=350)
            widget.pack(fill="both", expand=True)
            root.update_idletasks()
            root.update()
            assert int(widget.cget("width")) == 500
            widget.set_data({"A": 5, "B": 12, "C": 8}, animate=False)
            root.update()
            widget.event_generate("<Configure>")
            root.update()
    finally:
        root.destroy()


def test_click_event_and_hover_tooltip():
    tk = get_tk()
    from tkinter_dash import LineChart

    root = tk.Tk()
    root.geometry("500x350")
    chart = LineChart(root, {"A": 10, "B": 20, "C": 15}, animate=False, tooltip=True)
    chart.pack(fill="both", expand=True)
    root.update_idletasks()
    root.update()

    hits = []
    chart.bind("<<DataPointClick>>", lambda _e: hits.append(chart.last_clicked_index))
    left, top, right, bottom = chart._chart_bounds()
    x = left
    low, high = __import__("tkinter_dash.data", fromlist=["value_range"]).value_range(chart._data_values)
    y = bottom - ((chart._data_values[0] - low) / (high - low)) * (bottom - top)
    chart.event_generate("<Motion>", x=int(x), y=int(y))
    root.update()
    assert chart._hover_index == 0
    assert chart._tooltip is not None

    chart.event_generate("<Button-1>", x=int(x), y=int(y))
    root.update()
    assert hits == [0]

    chart.event_generate("<Leave>")
    root.update()
    assert chart._hover_index == -1
    assert chart._tooltip is None
    root.destroy()


def test_pie_rejects_non_positive_total():
    tk = get_tk()
    from tkinter_dash import PieChart

    root = tk.Tk()
    chart = PieChart(root, {"A": 1, "B": 1}, animate=False)
    chart.pack()
    root.update_idletasks()
    chart._data_values = [0.0, 0.0]
    with pytest.raises(ValueError):
        chart._slices()
    chart._data_values = [1.0, -1.0]
    with pytest.raises(ValueError):
        chart._slices()
    root.destroy()


def test_theme_change():
    tk = get_tk()
    from tkinter_dash import LineChart

    root = tk.Tk()
    chart = LineChart(root, {"A": 1, "B": 2}, animate=False)
    chart.pack()
    root.update_idletasks()
    chart.configure_theme("dark")
    assert chart.theme.background == "#0D1117"
    root.destroy()


def test_multi_series_charts():
    tk = get_tk()
    from tkinter_dash import BarChart, LineChart

    root = tk.Tk()
    data = {
        "Revenue": {"Q1": 65, "Q2": 85, "Q3": 45},
        "Cost": {"Q1": 40, "Q2": 55, "Q3": 30},
    }
    for Chart in (LineChart, BarChart):
        chart = Chart(root, data, animate=False)
        chart.pack(fill="both", expand=True)
        root.update_idletasks()
        root.update()
        assert set(chart.series) == {"Revenue", "Cost"}
        assert len(chart.find_all()) > 0
        chart.destroy()
    root.destroy()


def test_animation_advances_and_finishes():
    tk = get_tk()
    from tkinter_dash import LineChart

    root = tk.Tk()
    chart = LineChart(root, {"A": 10, "B": 20}, animate=True, duration=32)
    chart.pack()
    root.update_idletasks()
    start = chart._progress

    deadline = time.monotonic() + 0.5
    while chart._progress < 1.0 and time.monotonic() < deadline:
        root.update()
        time.sleep(0.005)
    assert start == 0.0
    assert chart._progress == 1.0
    chart.destroy()
    root.destroy()


def test_multi_series_hover_reports_series():
    tk = get_tk()
    from tkinter_dash import LineChart

    root = tk.Tk()
    chart = LineChart(root, {
        "Revenue": {"Q1": 10, "Q2": 20},
        "Cost": {"Q1": 8, "Q2": 15},
    }, animate=False, tooltip=True)
    chart.pack()
    root.update_idletasks()
    root.update()
    left, top, right, bottom = chart._chart_bounds()
    x = left
    low, high = __import__("tkinter_dash.data", fromlist=["value_range"]).value_range([10, 20, 8, 15])
    y = bottom - ((8 - low) / (high - low)) * (bottom - top)
    chart.event_generate("<Motion>", x=int(x), y=int(y))
    root.update()
    assert chart._hover_series == 1
    assert chart._tooltip is not None
    chart.destroy()
    root.destroy()


def test_line_curve_passes_through_data_points():
    from tkinter_dash.charts import _catmull_rom_points

    points = [(0.0, 0.0), (10.0, 20.0), (20.0, 5.0), (30.0, 25.0)]
    curve = _catmull_rom_points(points, samples_per_segment=10)
    assert curve[0] == points[0]
    assert points[1] in curve
    assert points[2] in curve
    assert curve[-1] == points[-1]
