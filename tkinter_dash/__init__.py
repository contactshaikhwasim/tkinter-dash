"""Native dashboard and visualization widgets for Tkinter."""

from .charts import BarChart, DonutChart, LineChart, PieChart, ScatterChart
from .theme import DARK, LIGHT, Theme

__all__ = [
    "BarChart",
    "DonutChart",
    "LineChart",
    "PieChart",
    "ScatterChart",
    "Theme",
    "LIGHT",
    "DARK",
]

__version__ = "0.1.4"
