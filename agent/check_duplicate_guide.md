# check_duplicate.py — Usage Guide

## Overview

Duplicate detection tool for data-type alpha strategies in `output/data_type_alpha/`.
Scans strategy files, extracts features/data/conditions, and compares them for similarity.

## Location

- Tool: `backtest/check_duplicate.py`
- Index: `backtest/strategy_index.json` (auto-generated)
- Target: `output/data_type_alpha/*.py`

## Modes

### 1. Build Index
```bash
python backtest/check_duplicate.py --index
```
Scans all `.py` files in `output/data_type_alpha/`, extracts features/data/conditions, saves to `backtest/strategy_index.json`.

### 2. Check Duplicates
```bash
python backtest/check_duplicate.py --check
```
Compares all strategies pairwise. Reports pairs with feature similarity ≥ 80% AND data similarity ≥ 80%.

Adjust thresholds:
```bash
python backtest/check_duplicate.py --check --feat-threshold 0.7 --data-threshold 0.7
```

### 3. Find by Feature
```bash
python backtest/check_duplicate.py --feature adx
```
Lists all strategies using a specific feature (e.g. `adx`, `sma`, `rsi`).

### 4. Find Similar to an Idea
```bash
python backtest/check_duplicate.py --idea DT_TSF_TREND_15min.py
```
Ranks all strategies by similarity to a target file (feature overlap + data field overlap).

### 5. Combined
```bash
python backtest/check_duplicate.py --index --check
```
Build index first, then check duplicates.

## Similarity Scoring

- **Feature similarity** (60% weight): Jaccard index of `self.feat.*` calls
- **Data similarity** (40% weight): Jaccard index of `self.data.*` fields
- **Combined score**: 0.6 × feat_sim + 0.4 × data_sim

## Output

- `backtest/strategy_index.json` — full strategy index with features, data fields, conditions
- Console output — duplicate pairs with similarity scores
