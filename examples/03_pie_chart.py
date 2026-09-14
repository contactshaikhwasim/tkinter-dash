import tkinter as tk

from _common import finish_smoke
from tkinter_dash import PieChart


root = tk.Tk()
root.title("tkinter-dash · Pie Chart")
root.geometry("760x500")

chart = PieChart(
    root,
    data={"Python": 42, "JavaScript": 28, "Go": 18, "Rust": 12},
    title="Language Share",
    theme="dark",
    animate=True,
    tooltip=True,
)
chart.pack(fill="both", expand=True, padx=16, pady=16)

finish_smoke(root)
root.mainloop()
