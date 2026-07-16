#!/usr/bin/env python3
"""
Count strategy files in output/ and generate STATS.md + optionally patch GUIDE.md.

Usage:
    python tools/update_guide_stats.py              # Generate STATS.md only
    python tools/update_guide_stats.py --patch      # Also update GUIDE.md placeholders
"""

import os
import re
import sys
import glob
from datetime import datetime

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
GUIDE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "agent", "GUIDE.md")
STATS_PATH = os.path.join(OUTPUT_DIR, "STATS.md")


def count_files(directory: str, pattern: str) -> int:
    return len(glob.glob(os.path.join(directory, pattern), recursive=True))


def get_thesis_groups(output_dir: str) -> list[str]:
    groups = []
    for item in sorted(os.listdir(output_dir)):
        if item.startswith("thesis_") and os.path.isdir(os.path.join(output_dir, item)):
            groups.append(item)
    return groups


def generate_stats(output_dir: str) -> dict:
    thesis_dirs = get_thesis_groups(output_dir)
    thesis_files = sum(
        count_files(os.path.join(output_dir, d), "**/*.py") for d in thesis_dirs
    )
    single_feat_files = count_files(
        os.path.join(output_dir, "single_feat_alpha"), "*.py"
    )
    single_feat_tier2_files = count_files(
        os.path.join(output_dir, "single_feat_alpha", "tier2"), "*.py"
    )
    multi_feat_files = count_files(
        os.path.join(output_dir, "multi_feat_alpha"), "*.py"
    )
    total = thesis_files + single_feat_files + multi_feat_files

    with open(STATS_PATH, "w", encoding="utf-8") as f:
        f.write(f"# Strategy Statistics\n\n")
        f.write(f"_Auto-generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n\n")
        f.write(f"| Category | Count |\n")
        f.write(f"|----------|:-----:|\n")
        f.write(f"| Thesis groups | {len(thesis_dirs)} |\n")
        f.write(f"| Thesis strategies | {thesis_files} |\n")
        f.write(f"| Single-feat alpha (Tier 1) | {single_feat_files} |\n")
        f.write(f"| Single-feat alpha (Tier 2) | {single_feat_tier2_files} |\n")
        f.write(f"| Multi-feat alpha | {multi_feat_files} |\n")
        f.write(f"| **Total** | **{total}** |\n")

    print(f"Generated: {STATS_PATH}")
    print(f"  Thesis groups: {len(thesis_dirs)}")
    print(f"  Thesis strategies: {thesis_files}")
    print(f"  Single-feat (Tier 1): {single_feat_files}")
    print(f"  Single-feat (Tier 2): {single_feat_tier2_files}")
    print(f"  Multi-feat: {multi_feat_files}")
    print(f"  Total: {total}")

    return {
        "STRATEGY_COUNT": str(total),
        "THESIS_COUNT": str(len(thesis_dirs)),
    }


def patch_guide(values: dict, guide_path: str):
    if not os.path.isfile(guide_path):
        print(f"  [!] GUIDE.md not found: {guide_path}")
        return

    with open(guide_path, "r", encoding="utf-8") as f:
        content = f.read()

    for key, val in values.items():
        placeholder = "{{" + key + "}}"
        if placeholder in content:
            content = content.replace(placeholder, val)
            print("  [PATCH] {} -> {}".format(placeholder, val))
        else:
            print(f"  [!] Placeholder {placeholder} not found in GUIDE.md")

    with open(guide_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Saved: {guide_path}")


def main():
    patch = "--patch" in sys.argv

    counts = generate_stats(OUTPUT_DIR)

    if patch:
        patch_guide(counts, GUIDE_PATH)

    # Template count — detect from TEMPLATES list in generate_strategies.py
    gen_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "tools", "generate_strategies.py"
    )
    if os.path.isfile(gen_path):
        with open(gen_path, "r", encoding="utf-8") as f:
            gen_code = f.read()
        template_count = gen_code.count('"name":') + gen_code.count("'name':")
        print(f"  Templates in generator: {template_count}")
        template_count = str(template_count)
    else:
        template_count = "?"
    if patch:
        patch_guide({"TEMPLATE_COUNT": template_count}, GUIDE_PATH)


if __name__ == "__main__":
    main()
