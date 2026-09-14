Charts
======

LineChart
---------

``LineChart`` is intended for categorical or ordered series and supports one or multiple named series.

.. code-block:: python

   chart = LineChart(
       root,
       {"Jan": 20, "Feb": 35, "Mar": 28},
       title="Monthly trend",
   )

Features include:

* animated rendering;
* point markers;
* hover highlighting;
* tooltips;
* responsive resizing;
* multi-series line charts;
* data replacement with ``set_data()`` / ``update()``.

BarChart
--------

``BarChart`` supports one or multiple named series.

.. code-block:: python

   chart = BarChart(
       root,
       {"Python": 86, "Go": 54, "Rust": 43},
       title="Survey",
   )

Multiple series are rendered as grouped bars.

PieChart
--------

``PieChart`` accepts one series and automatically converts values into slice percentages.

.. code-block:: python

   chart = PieChart(
       root,
       {"Python": 42, "JavaScript": 28, "Go": 18, "Rust": 12},
       title="Language share",
   )

Negative values are rejected, and the total must be positive.

DonutChart
----------

``DonutChart`` extends ``PieChart`` with a configurable inner hole and optional center text.

.. code-block:: python

   chart = DonutChart(
       root,
       {"Complete": 72, "Remaining": 28},
       hole=0.62,
       center_text="72%",
   )

ScatterChart
------------

The current ``ScatterChart`` uses the same label/value data model as the other basic categorical charts. It is not yet a general two-dimensional ``(x, y)`` scatter API.

.. code-block:: python

   chart = ScatterChart(
       root,
       {"A": 32, "B": 74, "C": 55},
       title="Samples",
   )

That limitation is documented intentionally and is a candidate for a future API revision.
