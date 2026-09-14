Quickstart
==========

Installation
------------

Install the package from PyPI:

.. code-block:: console

   pip install tkinter-dash

The core library does not require Matplotlib, Seaborn, Plotly, Pandas or NumPy.

Your first chart
----------------

.. code-block:: python

   import tkinter as tk
   from tkinter_dash import LineChart

   root = tk.Tk()
   root.geometry("900x520")

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

The chart is a normal Tkinter widget, so ``pack()``, ``grid()`` and other Tkinter layout tools can be used with it.

CustomTkinter
-------------

CustomTkinter can host the widgets directly:

.. code-block:: python

   import customtkinter as ctk
   from tkinter_dash import LineChart

   root = ctk.CTk()
   frame = ctk.CTkFrame(root)
   frame.pack(fill="both", expand=True, padx=16, pady=16)

   chart = LineChart(frame, {"A": 10, "B": 18, "C": 14})
   chart.pack(fill="both", expand=True)

CustomTkinter is optional and is not a core dependency.

Updating a chart
----------------

Use ``set_data()`` or its ``update()`` alias:

.. code-block:: python

   chart.update({"Jan": 140, "Feb": 210, "Mar": 170})

Pass ``animate=False`` when an immediate replacement is preferred:

.. code-block:: python

   chart.update(new_data, animate=False)
