import tkinter as tk

from _common import finish_smoke
from tkinter_dash import LineChart


root = tk.Tk()
root.title("tkinter-dash · Line Chart")
root.geometry("900x520")

chart = LineChart(
    root,
    data={"Jan": 120, "Feb": 180, "Mar": 150, "Apr": 220, "May": 195},
    title="Monthly Revenue",
    theme="dark",
    animate=True,
    tooltip=True,
)
chart.pack(fill="both", expand=True, padx=16, pady=16)

finish_smoke(root)
root.mainloop()
