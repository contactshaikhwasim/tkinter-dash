Data model
==========

The core library accepts small, Python-native data structures. Data preparation and business logic can be performed outside the chart widget.

Simple data
-----------

A mapping is interpreted as labels mapped to values:

.. code-block:: python

   {"Jan": 120, "Feb": 180, "Mar": 150}

A sequence of pairs is also accepted:

.. code-block:: python

   [("Jan", 120), ("Feb", 180), ("Mar", 150)]

Values are converted to finite ``float`` values. Boolean values, non-numeric values, ``NaN`` and positive/negative infinity are rejected.

Multi-series data
-----------------

``LineChart`` and ``BarChart`` support named series with matching labels:

.. code-block:: python

   {
       "Revenue": {"Q1": 120, "Q2": 180, "Q3": 155},
       "Cost": {"Q1": 80, "Q2": 105, "Q3": 92},
   }

All series must use the same labels in the same order.

Single-series charts
--------------------

``PieChart``, ``DonutChart`` and ``ScatterChart`` are intentionally single-series in the current release. Passing multiple named series raises ``ValueError``.

Pandas and NumPy
----------------

Pandas and NumPy are not runtime dependencies. A useful architecture is to use them for ETL and business calculations, then pass a small visualization-ready structure into ``tkinter-dash``.

For example:

.. code-block:: python

   yearly = (
       df.sort_values("Date")
         .groupby(df["Date"].dt.year)["Close"]
         .last()
   )

   data = [(str(year), float(close)) for year, close in yearly.items()]
   chart.set_data(data)

This keeps data engineering separate from rendering.
