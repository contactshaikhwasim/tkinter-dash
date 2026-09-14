import tkinter as tk

from _common import finish_smoke
from tkinter_dash import BarChart


root = tk.Tk()
root.title("tkinter-dash · Bar Chart")
root.geometry("900x520")

chart = BarChart(
    root,
    data={"Python": 86, "JavaScript": 72, "Go": 54, "Rust": 43},
    title="Developer Survey",
    animate=True,
    tooltip=True,
)
chart.pack(fill="both", expand=True, padx=16, pady=16)

finish_smoke(root)
root.mainloop()
