"""Real-data dashboard example using pandas for ETL and tkinter-dash for presentation.

Usage:
    python examples/10_market_insights.py /path/to/indexData.csv
"""

from __future__ import annotations

import sys
import tkinter as tk
from pathlib import Path

import pandas as pd

from _common import finish_smoke
from tkinter_dash import BarChart, DonutChart, LineChart


def build_insights(path: Path):
    df = pd.read_csv(path, parse_dates=["Date"])
    df = df.sort_values(["Index", "Date"])
    clean = df.dropna(subset=["Index", "Date", "Close"]).copy()
    clean["Year"] = clean["Date"].dt.year
    clean["DailyReturnPct"] = clean.groupby("Index")["Close"].pct_change() * 100

    annual = (
        clean.groupby(["Index", "Year"], as_index=False)
        .agg(Close=("Close", "last"), VolatilityPct=("DailyReturnPct", "std"))
    )
    annual["AnnualReturnPct"] = annual.groupby("Index")["Close"].pct_change() * 100

    latest = (
        annual.sort_values("Year")
        .groupby("Index", as_index=False)
        .tail(1)
        .sort_values("Close", ascending=False)
    )

    clean["RunningPeak"] = clean.groupby("Index")["Close"].cummax()
    clean["DrawdownPct"] = (clean["Close"] / clean["RunningPeak"] - 1) * 100
    worst = (
        clean.loc[clean.groupby("Index")["DrawdownPct"].idxmin(), ["Index", "DrawdownPct"]]
        .sort_values("DrawdownPct")
    )

    n225 = annual.loc[annual["Index"] == "N225"].dropna(subset=["Close", "AnnualReturnPct"])
    n225_close = [(str(int(y)), float(v)) for y, v in zip(n225["Year"], n225["Close"])]
    worst_drawdown = {str(i): float(v) for i, v in zip(worst["Index"], worst["DrawdownPct"])}
    outcome_counts = {
        "Positive years": int((n225["AnnualReturnPct"] > 0).sum()),
        "Negative years": int((n225["AnnualReturnPct"] < 0).sum()),
        "Flat years": int((n225["AnnualReturnPct"] == 0).sum()),
    }
    return latest, n225_close, worst_drawdown, outcome_counts


def main(path: Path):
    latest, n225_close, worst_drawdown, outcome_counts = build_insights(path)

    root = tk.Tk()
    root.title("tkinter-dash · Market Insights")
    root.geometry("1100x900")

    LineChart(root, n225_close, title="N225 Annual Close", theme="dark", height=300).pack(
        fill="both", expand=True, padx=16, pady=(16, 8)
    )
    BarChart(root, worst_drawdown, title="Worst Drawdown by Index", theme="dark", height=260).pack(
        fill="both", expand=True, padx=16, pady=8
    )
    DonutChart(root, outcome_counts, title="N225 Annual Return Outcomes", theme="dark", height=260).pack(
        fill="both", expand=True, padx=16, pady=(8, 16)
    )

    finish_smoke(root)
    root.mainloop()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python examples/10_market_insights.py /path/to/indexData.csv")
    main(Path(sys.argv[1]))
