import csv
import os
from datetime import datetime

PASS_THRESHOLDS = {
    "sharpe": 1.3,
    "cagr": 0.15,
    "max_drawdown": -0.35,
    "profit_factor": 1.2,
    "calmar": 1.1,
}


def getf(row, key):
    try:
        val = row.get(key, "")
        return float(val) if val.strip() else None
    except (ValueError, TypeError):
        return None


def is_pass(row):
    for key, threshold in PASS_THRESHOLDS.items():
        val = getf(row, key)
        if val is None or val < threshold:
            return False
    return True


def load_results_csv(csv_path="backtest/results.csv"):
    if not os.path.isfile(csv_path):
        return []
    with open(csv_path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_previous_results(csv_path="backtest/results.csv"):
    rows = load_results_csv(csv_path)
    prev = {}
    for r in rows:
        fname = r.get("filename", "")
        if fname:
            prev[fname] = is_pass(r)
    return prev


def format_metrics(metrics):
    parts = []
    for key, label in [
        ("cagr", "CAGR"),
        ("sharpe", "Sharpe"),
        ("calmar", "Calmar"),
        ("max_drawdown", "MaxDD"),
        ("profit_factor", "PF"),
    ]:
        val = metrics.get(key)
        if val is not None:
            parts.append(f"{label}: {val:.4f}")
        else:
            parts.append(f"{label}: N/A")
    return " | ".join(parts)


def build_latest(rows):
    latest = {}
    for r in rows:
        fname = r.get("filename", "")
        if fname:
            latest[fname] = r
    return latest


def timestamp_today():
    return datetime.now().strftime("%Y-%m-%d")