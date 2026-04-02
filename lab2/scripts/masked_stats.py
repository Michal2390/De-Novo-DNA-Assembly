#!/usr/bin/env python
"""Calculate masking statistics for RepeatMasker outputs."""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    from lab2.scripts.fasta_utils import read_fasta
except ModuleNotFoundError:  # direct script execution
    from fasta_utils import read_fasta


def count_masked_positions(original_fasta: Path, masked_fasta: Path) -> tuple[int, int, float]:
    original_records = read_fasta(original_fasta)
    masked_records = read_fasta(masked_fasta)
    if not original_records or not masked_records:
        raise ValueError("Both FASTA files must contain at least one record.")

    _, original_seq = original_records[0]
    _, masked_seq = masked_records[0]

    if len(original_seq) != len(masked_seq):
        raise ValueError("Original and masked sequences have different lengths.")

    original = original_seq.upper()
    masked = masked_seq.upper()

    masked_positions = sum(1 for o, m in zip(original, masked) if m == "N" and o != "N")
    total_len = len(original)
    percent = (masked_positions / total_len) * 100 if total_len else 0.0
    return masked_positions, total_len, percent


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute how many nucleotides were masked by RepeatMasker.")
    parser.add_argument("original", type=Path, help="Original FASTA")
    parser.add_argument("masked", type=Path, help="Masked FASTA")
    args = parser.parse_args()

    masked_count, seq_len, masked_percent = count_masked_positions(args.original, args.masked)
    print(f"sequence_length={seq_len}")
    print(f"masked_positions={masked_count}")
    print(f"masked_percent={masked_percent:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



