#!/usr/bin/env python
"""Summarize selected GFF feature types used in MBI lab2."""

from __future__ import annotations

import argparse
from pathlib import Path

TARGET_FEATURES = {"expressed_sequence_match", "protein_match"}


def count_features(gff_path: Path) -> dict[str, int]:
    counts = {feature: 0 for feature in TARGET_FEATURES}
    with gff_path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line == "##FASTA":
                break
            parts = line.split("\t")
            if len(parts) < 3:
                continue
            feature_type = parts[2]
            if feature_type in counts:
                counts[feature_type] += 1
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description="Count selected feature types in a GFF file.")
    parser.add_argument("gff", type=Path, help="Path to Maker .gff file")
    args = parser.parse_args()

    counts = count_features(args.gff)
    for feature in sorted(counts):
        print(f"{feature}={counts[feature]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

