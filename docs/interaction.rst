Interaction and themes
======================

Hover and tooltips
------------------

Hover interaction is enabled by default. When the pointer enters a data point or bar, the chart can highlight the target and show a tooltip.

Disable tooltips when they are not useful:

.. code-block:: python

   chart = LineChart(root, data, tooltip=False)

Click events
------------

Clicking a data point emits the Tkinter virtual event ``<<DataPointClick>>``.

.. code-block:: python

   def on_click(_event):
       print("index:", chart.last_clicked_index)
       print("series:", chart.last_clicked_series)

   chart.bind("<<DataPointClick>>", on_click)

``last_clicked_index`` is the clicked point index. ``last_clicked_series`` identifies the series for charts that support multiple series.

Themes
------

Built-in themes are:

* ``light``
* ``dark``

Choose a theme during construction:

.. code-block:: python

   chart = LineChart(root, data, theme="dark")

Change a theme later:

.. code-block:: python

   chart.configure_theme("light")

Or provide a custom ``Theme`` instance.

The project does not currently implement automatic operating-system theme detection. There is intentionally no ``system`` theme option in this release.

Animation
---------

Animations are enabled by default. Control them with ``animate`` and ``duration``:

.. code-block:: python

   chart = LineChart(
       root,
       data,
       animate=True,
       duration=500,
   )

The animation is driven by Tkinter's event loop and does not intentionally block the UI thread.
