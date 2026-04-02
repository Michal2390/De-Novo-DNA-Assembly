#!/usr/bin/env python
"""Prepare lab4 inputs and generate lab4 outputs from public archives.

This script extracts only required files and runs local Python analyses.
"""

from __future__ import annotations

import argparse
import csv
import tarfile
from pathlib import Path

from lab4.scripts.cnv_dgv_annotation import annotate_calls, read_codex_calls, read_dgv, write_tsv
from lab4.scripts.coverage_stats import load_from_tar, write_tsv as write_cov_tsv


def extract_member(archive_path: Path, member_name: str, output_path: Path) -> None:
    with tarfile.open(archive_path, "r:gz") as tf:
        member = tf.getmember(member_name)
        payload = tf.extractfile(member)
        if payload is None:
            raise RuntimeError(f"Cannot extract {member_name}")
        output_path.write_bytes(payload.read())


def main() -> int:
    parser = argparse.ArgumentParser(description="Run all Python parts for MBI lab4.")
    parser.add_argument("--tmp-dir", type=Path, required=True, help="Directory with downloaded archives")
    parser.add_argument("--lab4-dir", type=Path, required=True, help="Path to lab4 directory")
    args = parser.parse_args()

    input_dir = args.lab4_dir / "input"
    output_dir = args.lab4_dir / "output"
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    codex_tar = args.tmp_dir / "codex_output_all.tar.gz"
    coverage_tar = args.tmp_dir / "coverage.tar.gz"
    dgv_file = args.tmp_dir / "dgvMerged2.txt.gz"

    codex_chr20 = input_dir / "TGP99_20_4_CODEX_frac.txt"
    extract_member(codex_tar, "codex_output_all/TGP99_20_4_CODEX_frac.txt", codex_chr20)

    cov_tsv = output_dir / "coverage_medians_chr20.tsv"
    medians = load_from_tar(coverage_tar)
    write_cov_tsv(medians, cov_tsv)

    min_sample = min(medians, key=medians.get)
    max_sample = max(medians, key=medians.get)

    cov_summary = output_dir / "coverage_summary.txt"
    cov_summary.write_text(
        f"samples={len(medians)}\n"
        f"min_sample={min_sample}\tmedian={medians[min_sample]:.4f}\n"
        f"max_sample={max_sample}\tmedian={medians[max_sample]:.4f}\n",
        encoding="utf-8",
    )

    calls = read_codex_calls(codex_chr20)
    dgv_variants = read_dgv(dgv_file)
    ann_rows = annotate_calls(calls, dgv_variants)
    ann_tsv = output_dir / "cnv_dgv_annotation.tsv"
    write_tsv(ann_rows, ann_tsv)

    del_count = sum(1 for c in calls if c.cnv.lower().startswith("del"))
    dup_count = sum(1 for c in calls if c.cnv.lower().startswith("dup"))

    hom_del = 0
    with codex_chr20.open("r", encoding="utf-8") as handle:
        header = handle.readline().strip().split()
        idx = {name: i for i, name in enumerate(header)}
        for line in handle:
            parts = line.strip().split()
            if not parts:
                continue
            if "copy_no" in idx and float(parts[idx["copy_no"]]) == 0.0:
                hom_del += 1

    codex_summary = output_dir / "codex_summary.txt"
    codex_summary.write_text(
        f"total_calls={len(calls)}\n"
        f"deletions={del_count}\n"
        f"duplications={dup_count}\n"
        f"homozygous_deletions_copy_no_0={hom_del}\n",
        encoding="utf-8",
    )

    # Small quick-look table for report
    top5 = output_dir / "cnv_dgv_annotation_top5.tsv"
    with ann_tsv.open("r", encoding="utf-8", newline="") as in_h, top5.open("w", encoding="utf-8", newline="\n") as out_h:
        reader = csv.reader(in_h, delimiter="\t")
        writer = csv.writer(out_h, delimiter="\t")
        for i, row in enumerate(reader):
            writer.writerow(row)
            if i >= 5:
                break

    print(f"Prepared {codex_chr20}")
    print(f"Wrote {cov_tsv}")
    print(f"Wrote {cov_summary}")
    print(f"Wrote {ann_tsv}")
    print(f"Wrote {top5}")
    print(f"Wrote {codex_summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

