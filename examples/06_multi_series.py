import tkinter as tk

from _common import finish_smoke
from tkinter_dash import BarChart, LineChart


data = {
    "Revenue": {"Q1": 120, "Q2": 180, "Q3": 155, "Q4": 220},
    "Cost": {"Q1": 80, "Q2": 105, "Q3": 92, "Q4": 128},
}

root = tk.Tk()
root.title("tkinter-dash · Multi-Series")
root.geometry("1100x620")

line = LineChart(root, data=data, title="Revenue vs Cost", theme="dark")
line.pack(fill="both", expand=True, padx=16, pady=(16, 8))

bar = BarChart(root, data=data, title="Quarterly Comparison", theme="dark")
bar.pack(fill="both", expand=True, padx=16, pady=(8, 16))

finish_smoke(root)
root.mainloop()
