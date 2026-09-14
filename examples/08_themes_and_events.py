import tkinter as tk

from _common import finish_smoke
from tkinter_dash import LineChart


root = tk.Tk()
root.title("tkinter-dash · Themes and Events")
root.geometry("900x540")

status = tk.StringVar(value="Hover a point or click it")

chart = LineChart(
    root,
    {"Jan": 42, "Feb": 72, "Mar": 58, "Apr": 91, "May": 66},
    title="Interactive Demo",
    theme="dark",
)
chart.pack(fill="both", expand=True, padx=16, pady=(16, 8))

tk.Label(root, textvariable=status).pack(pady=(0, 12))

chart.bind(
    "<<DataPointClick>>",
    lambda _event: status.set(f"Clicked point #{chart.last_clicked_index}"),
)

def toggle_theme():
    chart.configure(theme="light" if chart.theme.background != "#FFFFFF" else "dark")

button = tk.Button(root, text="Toggle Theme", command=toggle_theme)
button.pack(pady=(0, 16))

finish_smoke(root)
root.mainloop()
