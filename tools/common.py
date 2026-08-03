import csv
import os
import time
from datetime import datetime

# Round 1 (archived) pass criteria — VN30 futures intraday
PASS_THRESHOLDS = {
    "sharpe": 1.3,
    "cagr": 0.15,
    "max_drawdown": -0.35,
    "profit_factor": 1.2,
    "calmar": 1.1,
}

# Round 2 (stage_2) pass criteria — per universe (source: user, 2026-08-01)
PASS_THRESHOLDS_BY_UNIVERSE = {
    "VN-SMALL-CAP": {
        "sharpe": 1.0,
        "cagr": 0.25,
        "max_drawdown": -0.45,
        "profit_factor": 1.3,
        "calmar": 0.8,
    },
    "VN-MID-CAP": {
        "sharpe": 1.1,
        "cagr": 0.20,
        "max_drawdown": -0.40,
        "profit_factor": 1.25,
        "calmar": 1.0,
    },
    "VN-LARGE-CAP": {
        "sharpe": 1.2,
        "cagr": 0.15,
        "max_drawdown": -0.35,
        "profit_factor": 1.2,
        "calmar": 1.1,
    },
}

VALID_UNIVERSES = set(PASS_THRESHOLDS_BY_UNIVERSE)

# Submit statuses that represent a real, usable simulation result
SIMULATED_STATUS = "SIMULATED"
VALID_METRIC_KEYS = ["sharpe", "cagr", "max_drawdown", "profit_factor", "calmar"]
RESULT_STAGES = ("simulate", "train", "test")
STAGE_PREFIXES = {"simulate": "", "train": "train_", "test": "test_"}
SUMMARY_URL = "https://api.xnoquant.io/xalpha-api/v1/strategies/{strategy_id}/stages/{stage}/summary-aggregate"


def thresholds_for(universe):
    """Pick pass thresholds for a universe. Unknown/empty universe -> KeyError (fail closed)."""
    if universe not in PASS_THRESHOLDS_BY_UNIVERSE:
        raise KeyError(f"Unknown universe '{universe}' — expected one of {sorted(VALID_UNIVERSES)}")
    return PASS_THRESHOLDS_BY_UNIVERSE[universe]


def getf(row, key):
    try:
        val = row.get(key, "")
        if isinstance(val, str):
            val = val.strip()
        if val == "" or val is None:
            return None
        return float(val)
    except (ValueError, TypeError):
        return None


def row_status(row):
    """Return the effective status of a result row."""
    status = (row.get("status") or "").strip().upper()
    return status


def has_all_metrics(row, prefix=""):
    """True when every required metric is a real number in the row."""
    return all(getf(row, f"{prefix}{key}") is not None for key in VALID_METRIC_KEYS)


def stage_pass(row, prefix="", universe=None):
    """Evaluate one complete aggregate/train/test metric set against its universe."""
    if not has_all_metrics(row, prefix):
        return False
    thresholds = thresholds_for(universe or row.get("universe"))
    return all(getf(row, f"{prefix}{key}") >= threshold
               for key, threshold in thresholds.items())


def is_pass(row, universe=None):
    """Pass requires complete aggregate, train, and test sets to pass independently."""
    status = row_status(row)
    if status != SIMULATED_STATUS:
        return False
    u = universe or row.get("universe")
    return all(stage_pass(row, prefix, u) for prefix in ("", "train_", "test_"))


def fetch_stage_metrics(session, strategy_id, stage):
    """Fetch one summary stage. Missing/null fields remain missing, never become zero."""
    if stage not in RESULT_STAGES:
        raise ValueError(f"Unknown result stage '{stage}'")
    url = SUMMARY_URL.format(strategy_id=strategy_id, stage=stage)
    try:
        response = session.get(url)
        if response.status_code != 200:
            return {}
        data = response.json().get("data") or {}
        return {key: data[key] for key in VALID_METRIC_KEYS
                if key in data and data[key] is not None}
    except Exception:
        return {}


def wait_for_stage_metrics(session, strategy_id, timeout, poll_interval=5):
    """Poll until all simulate/train/test summaries contain all five metrics."""
    ready = {}
    elapsed = 0
    while elapsed < timeout:
        for stage in RESULT_STAGES:
            if stage in ready:
                continue
            metrics = fetch_stage_metrics(session, strategy_id, stage)
            if all(metrics.get(key) is not None for key in VALID_METRIC_KEYS):
                ready[stage] = metrics
        if len(ready) == len(RESULT_STAGES):
            return ready
        time.sleep(poll_interval)
        elapsed += poll_interval
    return {}


def flatten_stage_metrics(stages):
    """Map API stage dictionaries to aggregate and prefixed CSV columns."""
    flat = {}
    for stage, prefix in STAGE_PREFIXES.items():
        for key, value in (stages.get(stage) or {}).items():
            if key in VALID_METRIC_KEYS:
                flat[f"{prefix}{key}"] = value
    return flat


def load_results_csv(csv_path="backtest/results_stage_2.csv"):
    if not os.path.isfile(csv_path):
        return []
    with open(csv_path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def row_key(row):
    """Identity for a result row: (filepath, universe). Never plain basename."""
    filepath = (row.get("filepath") or "").strip()
    universe = (row.get("universe") or "").strip()
    return (filepath, universe)


def load_previous_results(csv_path="backtest/results_stage_2.csv"):
    """Return { (filepath, universe): passed_bool } for SIMULATED passing rows only."""
    rows = load_results_csv(csv_path)
    prev = {}
    for r in rows:
        key = row_key(r)
        if not key[0]:
            continue
        try:
            passed = is_pass(r)
        except KeyError:
            continue
        if passed:
            prev[key] = True
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
    """Latest row per (filepath, universe). Preserves metadata rows (non-simulated)."""
    latest = {}
    order = []
    for r in rows:
        key = row_key(r)
        if not key[0]:
            continue
        if key not in latest:
            order.append(key)
        latest[key] = r
    return latest


def status_label(row):
    """Human-readable status grouping for check_results."""
    status = row_status(row)
    if status == SIMULATED_STATUS:
        try:
            return "PASS" if is_pass(row) else "FAIL"
        except KeyError:
            return "INVALID_METADATA"
    if status in ("UPDATE_FAILED", "VERIFY_FAILED", "SIMULATE_FAILED", "RATE_LIMITED"):
        return "API_ERROR"
    if status in ("METRICS_TIMEOUT", "NO_STRATEGY_ID"):
        return "PENDING"
    if not status:
        return "INVALID_METADATA"
    return status


def timestamp_today():
    return datetime.now().strftime("%Y-%m-%d")
