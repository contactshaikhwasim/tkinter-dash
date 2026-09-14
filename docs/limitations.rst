Current limitations
===================

``tkinter-dash`` is intentionally smaller than a general-purpose plotting framework.

Single-series charts
--------------------

``PieChart``, ``DonutChart`` and ``ScatterChart`` currently accept only one series. The library raises ``ValueError`` when multiple named series are supplied so invalid input does not silently disappear.

Scatter semantics
-----------------

The current scatter widget uses the label/value model. A true two-dimensional ``(x, y)`` scatter API is planned but not part of the current release.

Large datasets
--------------

Canvas-based rendering is appropriate for typical desktop dashboards, but very large datasets can become expensive because rendering and interaction work grow with the amount of visible data. The project does not currently promise smooth hover and animation for 100,000-point series.

A future release may introduce viewport-aware adaptive downsampling, but it should be driven by benchmarks rather than an arbitrary point-count limit.

Time-series axes
----------------

Applications can use date strings today, but the current release does not provide a dedicated datetime axis with calendar-aware tick formatting.

Streaming
---------

``set_data()`` and ``update()`` replace the current dataset. There is not yet a dedicated streaming API with rolling windows or incremental ingestion.

Export
------

There is no built-in PNG/SVG/PDF export API in the current release.

Data libraries
--------------

Pandas and NumPy are intentionally not core dependencies. Use them for ETL or numerical work, then hand a compact Python-native payload to the chart.

Why keep these limitations?
----------------------------

Each limitation represents a conscious scope boundary. Contributions are welcome when they solve a concrete problem without forcing the library into a much larger framework.
