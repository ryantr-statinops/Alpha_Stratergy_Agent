"""
Duplicate Detection Tool — Data-Type Alpha Strategies
Scans output/data_type_alpha/ for feature-based similarity.

Modes:
  --index       Build/update strategy index JSON
  --feature F   Find strategies using feature F (e.g. --feature adx)
  --idea FILE   Find strategies similar to a given idea file
  --check       Check all strategies for duplicates (default)
"""
import os, re, json, sys
from pathlib import Path
from collections import defaultdict

ALPHA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output", "data_type_alpha")
INDEX_PATH = os.path.join(os.path.dirname(__file__), "strategy_index.json")

FEAT_PATTERN = re.compile(r"self\.feat\.(\w+)\(")
DATA_PATTERN = re.compile(r"self\.data\.(\w+)")
COND_PATTERN = re.compile(r"(long_setup|short_setup|exit_setup)\s*=\s*(.+?)(?:\n|$)")


def parse_strategy(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    name = os.path.splitext(os.path.basename(filepath))[0]

    features = sorted(set(FEAT_PATTERN.findall(content)))
    data_fields = sorted(set(DATA_PATTERN.findall(content)))

    conditions = {}
    for match in COND_PATTERN.finditer(content):
        key = match.group(1)
        val = match.group(2).strip()
        conditions[key] = val

    return {
        "name": name,
        "file": os.path.basename(filepath),
        "features": features,
        "data_fields": data_fields,
        "conditions": conditions,
    }


def build_index(alpha_dir=None):
    if alpha_dir is None:
        alpha_dir = ALPHA_DIR
    if not os.path.isdir(alpha_dir):
        print(f"ERROR: Directory not found: {alpha_dir}")
        return []

    index = []
    for fname in sorted(os.listdir(alpha_dir)):
        if not fname.endswith(".py"):
            continue
        fpath = os.path.join(alpha_dir, fname)
        info = parse_strategy(fpath)
        index.append(info)

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    print(f"Index saved: {INDEX_PATH} ({len(index)} strategies)")
    return index


def load_index():
    if not os.path.exists(INDEX_PATH):
        print("No index found. Run with --index first.")
        return []
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def find_by_feature(index, feature_name):
    matches = []
    for s in index:
        if feature_name in s["features"]:
            matches.append(s["name"])
    return matches


def find_similar(index, target_name, threshold=0.5):
    target = None
    for s in index:
        if s["name"] == target_name:
            target = s
            break
    if not target:
        print(f"Strategy '{target_name}' not found in index.")
        return []

    target_feats = set(target["features"])
    target_data = set(target["data_fields"])

    scores = []
    for s in index:
        if s["name"] == target_name:
            continue
        feats = set(s["features"])
        data = set(s["data_fields"])

        feat_intersection = len(feats & target_feats)
        feat_union = len(feats | target_feats)
        feat_sim = feat_intersection / feat_union if feat_union > 0 else 0

        data_intersection = len(data & target_data)
        data_union = len(data | target_data)
        data_sim = data_intersection / data_union if data_union > 0 else 0

        combined = 0.6 * feat_sim + 0.4 * data_sim
        scores.append((s["name"], combined, feat_sim, data_sim))

    scores.sort(key=lambda x: -x[1])
    return scores


def check_duplicates(index, feat_threshold=0.8, data_threshold=0.8):
    n = len(index)
    duplicates = []
    for i in range(n):
        for j in range(i + 1, n):
            a, b = index[i], index[j]
            feats_a, feats_b = set(a["features"]), set(b["features"])
            data_a, data_b = set(a["data_fields"]), set(b["data_fields"])

            feat_sim = len(feats_a & feats_b) / len(feats_a | feats_b) if feats_a | feats_b else 0
            data_sim = len(data_a & data_b) / len(data_a | data_b) if data_a | data_b else 0

            if feat_sim >= feat_threshold and data_sim >= data_threshold:
                duplicates.append({
                    "a": a["name"],
                    "b": b["name"],
                    "feat_similarity": round(feat_sim, 3),
                    "data_similarity": round(data_sim, 3),
                    "shared_features": sorted(feats_a & feats_b),
                    "shared_data": sorted(data_a & data_b),
                })

    return duplicates


def print_results(index, duplicates, similar=None, target=None):
    print(f"\n{'='*60}")
    print(f"Strategy Index: {len(index)} strategies")
    print(f"{'='*60}")

    if duplicates:
        print(f"\nPotential Duplicates ({len(duplicates)} pairs):")
        print(f"{'─'*60}")
        for d in duplicates:
            print(f"  {d['a']}  ↔  {d['b']}")
            print(f"    feat_sim={d['feat_similarity']:.2f}  data_sim={d['data_similarity']:.2f}")
            print(f"    shared features: {', '.join(d['shared_features'][:5])}{'...' if len(d['shared_features']) > 5 else ''}")
            print()

    if similar is not None:
        print(f"\nStrategies similar to '{target}':")
        print(f"{'─'*60}")
        for name, combined, feat_sim, data_sim in similar[:10]:
            print(f"  {name:40s} combined={combined:.2f}  feat={feat_sim:.2f}  data={data_sim:.2f}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Duplicate detection for data-type alpha strategies")
    parser.add_argument("--index", action="store_true", help="Build/update strategy index JSON")
    parser.add_argument("--feature", type=str, help="Find strategies using a specific feature (e.g. adx)")
    parser.add_argument("--idea", type=str, help="Find strategies similar to a given idea file")
    parser.add_argument("--check", action="store_true", help="Check all strategies for duplicates")
    parser.add_argument("--feat-threshold", type=float, default=0.8, help="Feature similarity threshold (default: 0.8)")
    parser.add_argument("--data-threshold", type=float, default=0.8, help="Data similarity threshold (default: 0.8)")
    args = parser.parse_args()

    if args.index:
        index = build_index()
    else:
        index = load_index()

    if not index:
        print("No strategies found. Use --index to build index first.")
        return

    if args.feature:
        matches = find_by_feature(index, args.feature)
        print(f"\nStrategies using '{args.feature}':")
        for m in matches:
            print(f"  {m}")

    if args.idea:
        target = os.path.splitext(os.path.basename(args.idea))[0]
        similar = find_similar(index, target)
        print_results(index, [], similar, target)

    if args.check or not (args.index or args.feature or args.idea):
        duplicates = check_duplicates(index, args.feat_threshold, args.data_threshold)
        print_results(index, duplicates)


if __name__ == "__main__":
    main()
