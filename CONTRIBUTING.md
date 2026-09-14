# Contributing to tkinter-dash

Thanks for considering a contribution.

`tkinter-dash` is intentionally a small library. Contributions should improve a real user outcome without turning the project into a general-purpose plotting framework.

## Before you code

Please check:

1. Is the behavior already implemented or documented?
2. Is the issue a real bug, a reproducible limitation, or a concrete user need?
3. Can the change be made smaller?
4. Does the proposal fit the scope of a native Tkinter visualization library?
5. Can you add a regression test for the behavior?

For larger features, open an issue first so the API and scope can be discussed before implementation.

## Development setup

Use a supported Python version (the package currently declares Python `>=3.9`).

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[test]"
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -e ".[test]"
```

## Run tests

```bash
pytest
```

The widget tests require a working Tk display. In CI on Linux, use `xvfb-run` as shown in the GitHub Actions workflow.

## Run examples

```bash
python examples/01_line_chart.py
```

The examples also support a smoke mode:

```bash
TKINTER_DASH_SMOKE=1 python examples/01_line_chart.py
```

On Windows PowerShell:

```powershell
$env:TKINTER_DASH_SMOKE="1"
python examples/01_line_chart.py
```

## Regression-first changes

When fixing a bug:

1. Reproduce it with a failing test.
2. Make the smallest code change that fixes the behavior.
3. Run the focused test.
4. Run the complete suite.
5. Run the affected example(s).
6. Update documentation when public behavior changes.

Examples of high-value regression cases include:

- destroy a chart while animation is running;
- rapid `update()` calls;
- non-finite numeric data;
- resize during animation;
- tooltip near screen edges;
- large real-world datasets;
- multiple series with mismatched labels;
- theme changes while a chart is visible.

## Code style

Prefer readable Python with focused functions and clear names.

Avoid introducing abstractions just because they sound architecturally impressive. New layers should isolate a real responsibility or remove meaningful duplication.

Do not add speculative plugin systems, complex factories, or broad configuration surfaces without a concrete requirement.

## New chart types

A new chart should:

- behave like a normal Tkinter widget;
- use the shared chart/data/theme behavior where appropriate;
- have a small, predictable API;
- validate invalid input explicitly;
- support resize behavior;
- have tests for normal and edge cases;
- include a runnable example;
- document known limitations.

Do not add a chart merely to increase the feature count.

## Performance work

Do not optimize from intuition alone.

For rendering changes, include a reproducible benchmark when performance is part of the motivation. Prefer profiling and measured regressions over speculative micro-optimizations.

For dense datasets, consider the user's actual viewport: thousands of raw records do not necessarily need thousands of distinguishable pixels.

## Data integrations

Keep the core package lightweight. Pandas, NumPy and other data libraries should remain optional unless there is a compelling reason to make them mandatory.

A useful pattern is:

```text
Data preparation / ETL
        ↓
visualization-ready Python data
        ↓
tkinter-dash
```

This keeps the chart widget focused on rendering and interaction.

## Documentation

Documentation lives in `docs/` and is built with Sphinx for Read the Docs.

When public APIs or behavior change, update both:

- `README.md` for the quick overview;
- the relevant documentation page for detailed behavior.

## Pull requests

A good pull request should explain:

- what problem it solves;
- why the current behavior is insufficient;
- how the change works at a high level;
- which regression tests were added;
- which examples or docs were updated.

Keep unrelated cleanup out of the same pull request.

## Reporting bugs

Please include:

- Python version;
- operating system;
- Tk version when relevant;
- `tkinter-dash` version;
- smallest reproducible example;
- expected behavior;
- actual behavior;
- traceback or screenshot when useful.

For rendering issues, a small reproducible dataset is especially valuable.

## Areas where help is useful

The project currently has several intentional areas for improvement:

- dense time-series rendering;
- adaptive downsampling;
- datetime axes;
- richer crosshair/interaction behavior;
- true XY scatter data;
- streaming updates;
- visual regression testing;
- cross-platform validation;
- accessibility improvements;
- packaging and documentation.

A focused improvement in one of these areas is more valuable than a large speculative rewrite.
