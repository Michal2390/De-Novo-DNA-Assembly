#!/usr/bin/env python
"""Annotate CODEX CNV calls with overlap counts from DGV.

For each CNV call this script reports:
- number of overlapping DGV deletions,
- number of overlapping DGV duplications,
- number of any DGV variants with >=80% overlap of the CNV length.
"""

from __future__ import annotations

import argparse
import csv
import gzip
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Interval:
    chrom: str
    start: int
    end: int


@dataclass(frozen=True)
class CnvCall:
    sample_name: str
    cnv: str
    interval: Interval


@dataclass(frozen=True)
class DgvVariant:
    var_type: str
    interval: Interval


def classify_dgv_variant_type(raw: str) -> str:
    value = raw.strip().lower()
    if "del" in value or "loss" in value:
        return "deletion"
    if "dup" in value or "gain" in value:
        return "duplication"
    return "other"


def overlap_len(a: Interval, b: Interval) -> int:
    if a.chrom != b.chrom:
        return 0
    return max(0, min(a.end, b.end) - max(a.start, b.start))


def read_codex_calls(path: Path) -> list[CnvCall]:
    calls: list[CnvCall] = []
    with path.open("r", encoding="utf-8") as handle:
        header = handle.readline().strip().split()
        idx = {name: i for i, name in enumerate(header)}
        required = ["sample_name", "chr", "cnv", "st_bp", "ed_bp"]
        for col in required:
            if col not in idx:
                raise ValueError(f"Missing required column in CODEX file: {col}")

        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            parts = line.split()
            calls.append(
                CnvCall(
                    sample_name=parts[idx["sample_name"]],
                    cnv=parts[idx["cnv"]],
                    interval=Interval(
                        chrom=f"chr{parts[idx['chr']]}" if not parts[idx["chr"]].startswith("chr") else parts[idx["chr"]],
                        start=int(parts[idx["st_bp"]]),
                        end=int(parts[idx["ed_bp"]]),
                    ),
                )
            )
    return calls


def open_maybe_gzip(path: Path):
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="utf-8", newline="")
    return path.open("r", encoding="utf-8", newline="")


def read_dgv(path: Path) -> list[DgvVariant]:
    variants: list[DgvVariant] = []
    with open_maybe_gzip(path) as handle:
        reader = csv.reader(handle, delimiter="\t")
        for row in reader:
            if not row:
                continue
            # UCSC dgvMerged: chrom at col=1, chromStart=2, chromEnd=3, varType=10
            if len(row) < 11:
                continue
            chrom = row[1]
            if not chrom.startswith("chr"):
                chrom = f"chr{chrom}"
            start = int(row[2])
            end = int(row[3])
            variants.append(
                DgvVariant(
                    var_type=classify_dgv_variant_type(row[10]),
                    interval=Interval(chrom=chrom, start=start, end=end),
                )
            )
    return variants


def annotate_calls(calls: list[CnvCall], dgv_variants: list[DgvVariant]) -> list[dict[str, str | int]]:
    out: list[dict[str, str | int]] = []
    by_chrom: dict[str, list[DgvVariant]] = {}
    for variant in dgv_variants:
        by_chrom.setdefault(variant.interval.chrom, []).append(variant)

    for call in calls:
        chrom_variants = by_chrom.get(call.interval.chrom, [])
        cnv_len = max(1, call.interval.end - call.interval.start)

        del_any = 0
        dup_any = 0
        any_80pct = 0

        for variant in chrom_variants:
            ov = overlap_len(call.interval, variant.interval)
            if ov <= 0:
                continue
            if variant.var_type == "deletion":
                del_any += 1
            elif variant.var_type == "duplication":
                dup_any += 1
            if (ov / cnv_len) >= 0.8:
                any_80pct += 1

        out.append(
            {
                "sample_name": call.sample_name,
                "chr": call.interval.chrom,
                "cnv": call.cnv,
                "st_bp": call.interval.start,
                "ed_bp": call.interval.end,
                "dgv_del_overlap_any": del_any,
                "dgv_dup_overlap_any": dup_any,
                "dgv_any_overlap_80pct": any_80pct,
            }
        )
    return out


def write_tsv(rows: list[dict[str, str | int]], output_path: Path) -> None:
    if not rows:
        output_path.write_text("", encoding="utf-8")
        return

    fieldnames = list(rows[0].keys())
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Annotate CODEX CNV calls with DGV overlaps.")
    parser.add_argument("codex_calls", type=Path, help="CODEX CNV calls file (e.g. *_CODEX_frac.txt)")
    parser.add_argument("dgv_file", type=Path, help="DGV file (UCSC dgvMerged.txt or .gz)")
    parser.add_argument("output_tsv", type=Path, help="Output TSV path")
    args = parser.parse_args()

    calls = read_codex_calls(args.codex_calls)
    dgv_variants = read_dgv(args.dgv_file)
    rows = annotate_calls(calls, dgv_variants)
    write_tsv(rows, args.output_tsv)

    print(f"calls={len(calls)}")
    print(f"dgv_variants={len(dgv_variants)}")
    print(f"output={args.output_tsv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

