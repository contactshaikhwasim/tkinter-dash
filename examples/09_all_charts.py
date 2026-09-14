import tkinter as tk

from _common import finish_smoke
from tkinter_dash import BarChart, DonutChart, LineChart, PieChart, ScatterChart


root = tk.Tk()
root.title("tkinter-dash · All MVP Charts")
root.geometry("1200x760")

data = {"A": 25, "B": 48, "C": 36, "D": 68}

charts = [
    LineChart(root, data, title="Line", theme="dark"),
    BarChart(root, data, title="Bar", theme="dark"),
    PieChart(root, data, title="Pie", theme="dark"),
    DonutChart(root, data, title="Donut", theme="dark", center_text="44%"),
    ScatterChart(root, data, title="Scatter", theme="dark"),
]

for index, chart in enumerate(charts):
    row, column = divmod(index, 2)
    chart.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

root.grid_rowconfigure((0, 1, 2), weight=1)
root.grid_columnconfigure((0, 1), weight=1)

finish_smoke(root)
root.mainloop()
