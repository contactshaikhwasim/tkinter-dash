Examples
========

The repository includes runnable examples for the complete MVP.

.. list-table::
   :header-rows: 1
   :widths: 20 70

   * - File
     - Purpose
   * - ``01_line_chart.py``
     - Basic animated line chart
   * - ``02_bar_chart.py``
     - Basic bar chart
   * - ``03_pie_chart.py``
     - Pie chart and percentage legend
   * - ``04_donut_chart.py``
     - Donut chart and center text
   * - ``05_scatter_chart.py``
     - Current label/value scatter-style chart
   * - ``06_multi_series.py``
     - Multi-series line and bar charts
   * - ``07_live_update.py``
     - Repeated chart updates
   * - ``08_themes_and_events.py``
     - Theme switching and click events
   * - ``09_all_charts.py``
     - All MVP charts in one window
   * - ``10_market_insights.py``
     - Pandas ETL/business insights feeding chart widgets

Run examples from the repository root, for example:

.. code-block:: console

   python examples/01_line_chart.py

Smoke testing
-------------

Examples support the ``TKINTER_DASH_SMOKE`` environment variable. When set, an example closes after a short delay so automated GUI smoke tests can launch it without human interaction.

.. code-block:: console

   TKINTER_DASH_SMOKE=1 python examples/09_all_charts.py

Real-data workflow
------------------

The market-insights example demonstrates the intended separation of concerns:

.. code-block:: text

   Raw CSV
      |
      v
   Pandas ETL / business calculations
      |
      v
   Visualization-ready Python structures
      |
      v
   tkinter-dash widgets

This pattern keeps the chart library focused on visualization rather than becoming a data-processing framework.
