import random
import tkinter as tk

from _common import finish_smoke
from tkinter_dash import LineChart


root = tk.Tk()
root.title("tkinter-dash · Live Update")
root.geometry("1000x560")

values = {f"{i:02d}": random.randint(50, 120) for i in range(12)}
chart = LineChart(root, values, title="Live System Load", theme="dark", animate=False)
chart.pack(fill="both", expand=True, padx=16, pady=16)

step = 0

def update():
    global step
    step += 1
    labels = list(values)[-12:]
    points = values.copy()
    points[str(12 + step)] = random.randint(50, 120)
    while len(points) > 12:
        points.pop(next(iter(points)))
    values.clear()
    values.update(points)
    chart.update(values, animate=True)
    root.after(900, update)

root.after(900, update)
finish_smoke(root)
root.mainloop()
