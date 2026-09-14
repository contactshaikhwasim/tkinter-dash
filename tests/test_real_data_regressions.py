import os
from pathlib import Path

import pytest

pd = pytest.importorskip("pandas")

DATA_PATH = Path("/mnt/data/indexData_extracted/indexData.csv")


def etl_market_insights():
    df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    df = df.sort_values(["Index", "Date"])

    # Business-ready ETL: remove rows without an index/date, keep OHLC rows with
    # usable Close, and derive stable annual metrics for dashboard consumption.
    clean = df.dropna(subset=["Index", "Date", "Close"]).copy()
    clean["Year"] = clean["Date"].dt.year
    clean["DailyReturnPct"] = clean.groupby("Index")["Close"].pct_change() * 100

    annual = (
        clean.groupby(["Index", "Year"], as_index=False)
        .agg(
            Close=("Close", "last"),
            AvgClose=("Close", "mean"),
            VolatilityPct=("DailyReturnPct", "std"),
        )
    )
    annual["AnnualReturnPct"] = annual.groupby("Index")["Close"].pct_change() * 100

    latest = (
        annual.sort_values("Year")
        .groupby("Index", as_index=False)
        .tail(1)
        .sort_values("Close", ascending=False)
    )

    # A drawdown series is a useful business insight that stresses signed values.
    clean["RunningPeak"] = clean.groupby("Index")["Close"].cummax()
    clean["DrawdownPct"] = (clean["Close"] / clean["RunningPeak"] - 1) * 100
    worst_drawdown = (
        clean.loc[clean.groupby("Index")["DrawdownPct"].idxmin(), ["Index", "Date", "DrawdownPct"]]
        .sort_values("DrawdownPct")
        .reset_index(drop=True)
    )

    return clean, annual, latest, worst_drawdown


def test_real_dataset_etl_produces_non_empty_business_insights():
    clean, annual, latest, worst_drawdown = etl_market_insights()

    assert len(clean) > 100_000
    assert clean["Index"].nunique() == 14
    assert not clean["Close"].isna().any()
    assert not annual.empty
    assert len(latest) == 14
    assert len(worst_drawdown) == 14
    assert worst_drawdown["DrawdownPct"].le(0).all()


def test_business_insight_payloads_are_valid_tkinter_dash_inputs():
    _, annual, latest, worst_drawdown = etl_market_insights()

    # KPI/ranking payload: one value per index.
    ranking = dict(zip(latest["Index"], latest["Close"].round(2)))
    assert len(ranking) == 14

    # Time-series payload: yearly closes for one index.
    n225 = annual.loc[annual["Index"] == "N225"].dropna(subset=["Close"])
    yearly_close = [
        (str(int(year)), float(close))
        for year, close in zip(n225["Year"], n225["Close"])
    ]
    assert len(yearly_close) > 40
    assert yearly_close[0][0].isdigit()

    # Signed business insight: drawdown is valid for bar/line charts.
    drawdown_payload = {
        str(row["Index"]): float(row["DrawdownPct"])
        for _, row in worst_drawdown.iterrows()
    }
    assert any(value < 0 for value in drawdown_payload.values())


def test_n225_raw_history_does_not_create_one_x_label_per_row():
    import tkinter as tk
    from tkinter_dash import LineChart

    _, _, _, _ = etl_market_insights()
    df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    n225 = df.loc[(df["Index"] == "N225") & df["Close"].notna(), ["Date", "Close"]]

    root = tk.Tk()
    try:
        chart = LineChart(
            root,
            [(date.strftime("%Y-%m-%d"), float(close)) for date, close in zip(n225["Date"], n225["Close"])],
            animate=False,
            show_legend=False,
            width=1100,
            height=500,
        )
        chart.pack(fill="both", expand=True)
        root.update_idletasks()
        root.update()

        labels = chart._x_label_indices(len(chart._data_labels), chart.winfo_width())
        assert len(labels) <= 20
        assert labels[0] == 0
        assert labels[-1] == len(chart._data_labels) - 1
        chart.destroy()
    finally:
        root.destroy()


def test_business_insights_render_through_all_mvp_charts():
    import tkinter as tk
    from tkinter_dash import BarChart, DonutChart, LineChart, PieChart

    clean, annual, latest, worst_drawdown = etl_market_insights()
    n225 = annual.loc[annual["Index"] == "N225"].dropna(subset=["Close", "AnnualReturnPct"]).copy()

    annual_close = [
        (str(int(year)), float(close))
        for year, close in zip(n225["Year"], n225["Close"])
    ]
    drawdown = {
        str(index): float(value)
        for index, value in zip(worst_drawdown["Index"], worst_drawdown["DrawdownPct"])
    }

    outcome_counts = {
        "Positive years": int((n225["AnnualReturnPct"] > 0).sum()),
        "Negative years": int((n225["AnnualReturnPct"] < 0).sum()),
        "Flat years": int((n225["AnnualReturnPct"].fillna(0) == 0).sum()),
    }

    root = tk.Tk()
    charts = []
    try:
        charts = [
            LineChart(root, annual_close, animate=False, show_legend=False, width=900, height=420),
            BarChart(root, drawdown, animate=False, show_legend=False, width=900, height=420),
            PieChart(root, outcome_counts, animate=False, width=500, height=350),
            DonutChart(root, outcome_counts, animate=False, width=500, height=350),
        ]
        for chart in charts:
            chart.pack()
        root.update_idletasks()
        root.update()
        assert all(chart.winfo_width() > 1 and chart.winfo_height() > 1 for chart in charts)
        assert all(chart.find_all() for chart in charts)
    finally:
        for chart in charts:
            chart.destroy()
        root.destroy()


def test_real_market_multi_series_compare_uses_matching_years():
    import tkinter as tk
    from tkinter_dash import LineChart

    _, annual, _, _ = etl_market_insights()
    common_years = sorted(
        set(annual.loc[annual["Index"] == "N225", "Year"])
        & set(annual.loc[annual["Index"] == "NYA", "Year"])
    )
    assert len(common_years) > 40

    series = {}
    for index in ("N225", "NYA"):
        subset = annual.loc[(annual["Index"] == index) & annual["Year"].isin(common_years)]
        subset = subset.sort_values("Year")
        assert subset["Year"].tolist() == common_years
        series[index] = {
            str(year): float(close)
            for year, close in zip(subset["Year"], subset["Close"])
        }

    root = tk.Tk()
    try:
        chart = LineChart(root, series, animate=False, width=1000, height=450)
        chart.pack(fill="both", expand=True)
        root.update_idletasks()
        root.update()
        assert len(chart.series) == 2
        assert set(chart.series) == {"N225", "NYA"}
        assert len(chart._x_label_indices(len(common_years), chart.winfo_width())) <= 20
        chart.destroy()
    finally:
        root.destroy()
