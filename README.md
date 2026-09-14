# tkinter-dash

[![CI](https://github.com/contactshaikhwasim/tkinter-dash/actions/workflows/ci.yml/badge.svg)](https://github.com/contactshaikhwasim/tkinter-dash/actions/workflows/ci.yml)
[![Documentation](https://readthedocs.org/projects/tkinter-dash/badge/?version=latest)](https://tkinter-dash.readthedocs.io/en/latest/)
[![PyPI](https://img.shields.io/pypi/v/tkinter-dash.svg)](https://pypi.org/project/tkinter-dash/)
[![Python](https://img.shields.io/pypi/pyversions/tkinter-dash.svg)](https://pypi.org/project/tkinter-dash/)

**Modern, interactive dashboard and visualization widgets for Tkinter.**

`tkinter-dash` is a lightweight Canvas-based visualization library designed for Python desktop applications. It focuses on a simple, native Tkinter API so you can add charts to an existing Tkinter or CustomTkinter application without introducing a web UI, Matplotlib, Seaborn, Plotly, or a separate dashboard framework.

> **Status:** Alpha (`0.1.4`). The API is usable, but compatibility and visualization behavior may evolve before `1.0`.

## Why tkinter-dash?

Typical Tkinter applications can embed Matplotlib, but that often means carrying a general-purpose plotting stack and writing integration code. `tkinter-dash` takes a different approach: charts are widgets, rendering happens on Tkinter Canvas, and common interactions are built in.

```python
import tkinter as tk
from tkinter_dash import LineChart

root = tk.Tk()

chart = LineChart(
    root,
    data={"Jan": 120, "Feb": 180, "Mar": 150, "Apr": 220},
    title="Revenue",
    theme="dark",
    animate=True,
    tooltip=True,
)
chart.pack(fill="both", expand=True, padx=16, pady=16)

root.mainloop()
```

## Current features

### Charts

- `LineChart`
- `BarChart`
- `PieChart`
- `DonutChart`
- `ScatterChart`

### Interaction

- Hover highlighting
- Tooltips
- Tkinter virtual click events (`<<DataPointClick>>`)
- Responsive resizing
- Animated rendering

### Data

- Mapping input, such as `{"Jan": 100, "Feb": 120}`
- Sequence-of-pairs input, such as `[("Jan", 100), ("Feb", 120)]`
- Multi-series `LineChart` and `BarChart`
- Finite numeric-value validation
- Live replacement of data with `set_data()` / `update()`

### Theming

- Built-in light and dark themes
- Custom `Theme` instances
- Runtime theme changes with `configure_theme()`

### Integration

- Native Tkinter Canvas widgets
- Works inside ordinary Tkinter containers
- CustomTkinter can host the widgets without a dedicated adapter class
- Core package has no plotting-library dependency

## Installation

```bash
pip install tkinter-dash
```

Development/test dependencies:

```bash
pip install -e ".[test]"
```

## Data examples

### Simple categorical data

```python
from tkinter_dash import BarChart

chart = BarChart(
    root,
    data={
        "Python": 86,
        "JavaScript": 72,
        "Go": 54,
    },
)
chart.pack(fill="both", expand=True)
```

### Sequence-of-pairs data

```python
chart = LineChart(
    root,
    data=[
        ("Jan", 120),
        ("Feb", 180),
        ("Mar", 150),
    ],
)
```

### Multi-series data

`LineChart` and `BarChart` accept named series with matching labels:

```python
series = {
    "Revenue": {"Q1": 120, "Q2": 180, "Q3": 155},
    "Cost": {"Q1": 80, "Q2": 105, "Q3": 92},
}

chart = LineChart(root, series, title="Revenue vs Cost")
chart.pack(fill="both", expand=True)
```

`PieChart`, `DonutChart`, and `ScatterChart` intentionally accept one series in the current release. Passing multiple named series raises `ValueError` instead of silently dropping data.

## Themes

Use either a built-in theme:

```python
chart = LineChart(root, data, theme="dark")
```

or a `Theme` instance:

```python
from tkinter_dash import Theme

custom = Theme(
    background="#101010",
    plot_background="#181818",
    text="#F5F5F5",
    muted_text="#A0A0A0",
    grid="#303030",
    axis="#808080",
    accent="#7C3AED",
    accent_2="#06B6D4",
    tooltip_background="#0B0B0B",
    tooltip_border="#7C3AED",
    tooltip_text="#FFFFFF",
    positive="#22C55E",
    negative="#EF4444",
)

chart.configure_theme(custom)
```

Only `light` and `dark` are currently supported. There is intentionally no fake `system` theme in this release.

## Interaction and events

Charts expose normal Tkinter event binding. For example:

```python
def on_click(_event):
    print(chart.last_clicked_index)
    print(chart.last_clicked_series)

chart.bind("<<DataPointClick>>", on_click)
```

Hover state and tooltip behavior are enabled by default for the charts that support them.

## Updating data

```python
chart.update({"Jan": 140, "Feb": 210, "Mar": 170})
```

or:

```python
chart.set_data(new_data, animate=False)
```

The current release treats updates as whole-dataset replacements rather than a dedicated streaming API.

## Examples

The repository includes runnable examples for each current chart and common usage patterns:

| Example | Demonstrates |
|---|---|
| `01_line_chart.py` | Line chart basics |
| `02_bar_chart.py` | Bar chart basics |
| `03_pie_chart.py` | Pie chart |
| `04_donut_chart.py` | Donut chart and center label |
| `05_scatter_chart.py` | Scatter chart |
| `06_multi_series.py` | Multi-series line/bar charts |
| `07_live_update.py` | Repeated data updates |
| `08_themes_and_events.py` | Themes, hover and click events |
| `09_all_charts.py` | All MVP charts together |
| `10_market_insights.py` | Real-world Pandas ETL feeding tkinter-dash |

Run an example from the repository root:

```bash
python examples/01_line_chart.py
```

For GUI smoke tests, the examples support `TKINTER_DASH_SMOKE=1` and exit automatically after a short delay.

## Real-data example

`10_market_insights.py` demonstrates a useful boundary for the library: **Pandas performs ETL and business calculations; tkinter-dash receives the resulting visualization-ready payload.**

This separation keeps data engineering out of the chart widget while still allowing real datasets to drive the UI.

## Current limitations

The project is intentionally narrower than a general plotting framework.

- `PieChart`, `DonutChart`, and `ScatterChart` are single-series only.
- `ScatterChart` currently uses the label/value model rather than a general `(x, y)` coordinate API.
- There is no dedicated zoom/pan or viewport model yet.
- There is no first-class streaming API; applications currently replace chart data with `update()` / `set_data()`.
- Very large datasets can become expensive because the renderer is Canvas-based and redraw-oriented. The project does not currently promise smooth interactive behavior for 100k-point workloads.
- Datetime-aware x-axis formatting is not yet a dedicated feature; applications can provide formatted labels today.
- Pandas and NumPy are not core dependencies. They are intentionally kept outside the runtime dependency set.
- Export formats such as SVG/PDF/PNG are not currently a core chart API.

These are deliberate scope boundaries, not hidden promises. See the roadmap and contribution guide before proposing a large feature.

## Roadmap

### Near term

- Strengthen axis tick and label layout
- Improve handling of large and dense time-series data
- Add better regression coverage for resize, hover and update behavior
- Improve public type annotations and API documentation
- Benchmark rendering and interaction on larger datasets

### Medium term

- Adaptive downsampling for dense line charts
- Datetime-aware x-axis support
- Crosshair support
- More explicit live/streaming data APIs
- A true XY scatter API
- Better chart transitions when replacing data

### Longer term

- Zoom and pan
- Linked/cross-filtered charts
- KPI, gauge, sparkline and other dashboard widgets
- Migration guidance/tools for common Tkinter + Matplotlib setups
- Optional data adapters for Pandas/NumPy

The roadmap is intentionally evidence-driven. New features should earn their place through a concrete use case, regression coverage, and a maintainable implementation.

## Help improve tkinter-dash

This project is deliberately designed to leave room for contributors. Some of the most useful work is not adding another chart type; it is making the existing widgets more correct, predictable and useful on real datasets.

Good contribution targets include:

- reproducing a rendering bug with a small regression test;
- improving axis/tick calculations;
- benchmarking a proposed rendering optimization;
- improving accessibility and keyboard behavior;
- adding well-scoped data adapters;
- improving examples and documentation;
- validating behavior on Windows, macOS and Linux;
- investigating dense time-series interaction and downsampling.

Please read `CONTRIBUTING.md` before opening a pull request.

## Design philosophy

`tkinter-dash` favors simple, maintainable code over a large plotting framework. The goal is to provide clear widget boundaries and a useful native API without recreating all of Matplotlib.

## License

MIT. See `LICENSE` when the repository is published with the project license file.
