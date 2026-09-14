import tkinter as tk

from _common import finish_smoke
from tkinter_dash import ScatterChart


root = tk.Tk()
root.title("tkinter-dash · Scatter Chart")
root.geometry("900x520")

chart = ScatterChart(
    root,
    data={"A": 32, "B": 74, "C": 55, "D": 88, "E": 64, "F": 92},
    title="Response Time Samples",
    animate=True,
    tooltip=True,
)
chart.pack(fill="both", expand=True, padx=16, pady=16)

finish_smoke(root)
root.mainloop()
