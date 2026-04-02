#!/usr/bin/env python
"""Compute GC content for FASTA files using Biopython."""

from __future__ import annotations

import argparse
from pathlib import Path

from Bio import SeqIO


def gc_percent(sequence: str) -> float:
    seq = sequence.upper()
    acgt = sum(seq.count(base) for base in "ACGT")
    if acgt == 0:
        return 0.0
    gc = seq.count("G") + seq.count("C")
    return (gc / acgt) * 100.0


def compute_file_gc(fasta_path: Path) -> tuple[float, int]:
    total_gc = 0
    total_acgt = 0

    for rec in SeqIO.parse(str(fasta_path), "fasta"):
        seq = str(rec.seq).upper()
        g = seq.count("G")
        c = seq.count("C")
        a = seq.count("A")
        t = seq.count("T")
        total_gc += g + c
        total_acgt += a + c + g + t

    if total_acgt == 0:
        return 0.0, 0

    return (total_gc / total_acgt) * 100.0, total_acgt


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate GC content for FASTA.")
    parser.add_argument("fasta", type=Path, help="Path to FASTA file")
    args = parser.parse_args()

    gc, length = compute_file_gc(args.fasta)
    print(f"file={args.fasta}")
    print(f"acgt_bases={length}")
    print(f"gc_percent={gc:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

