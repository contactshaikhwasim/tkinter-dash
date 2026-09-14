import tkinter as tk

from _common import finish_smoke
from tkinter_dash import DonutChart


root = tk.Tk()
root.title("tkinter-dash · Donut Chart")
root.geometry("760x500")

chart = DonutChart(
    root,
    data={"Complete": 72, "Remaining": 28},
    title="Project Completion",
    theme="dark",
    hole=0.62,
    center_text="72%",
    animate=True,
    tooltip=True,
)
chart.pack(fill="both", expand=True, padx=16, pady=16)

finish_smoke(root)
root.mainloop()
