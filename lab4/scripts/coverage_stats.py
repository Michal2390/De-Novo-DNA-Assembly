#!/usr/bin/env python
"""Compute per-sample median normalized depth from coverage files.

Input can be:
- a directory with files `*.bam.coverage_chr20.txt`, or
- a tar.gz archive containing those files.
"""

from __future__ import annotations

import argparse
import csv
import statistics
import tarfile
from pathlib import Path


def parse_coverage_lines(lines: list[str]) -> float:
    values: list[float] = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) < 4:
            continue
        start = int(parts[1])
        stop = int(parts[2])
        read_count = int(parts[3])
        width = max(1, stop - start)
        values.append((100.0 * read_count) / width)
    if not values:
        return 0.0
    return float(statistics.median(values))


def sample_name_from_filename(name: str) -> str:
    return name.split(".")[0]


def load_from_tar(tar_path: Path) -> dict[str, float]:
    medians: dict[str, float] = {}
    with tarfile.open(tar_path, "r:gz") as tf:
        members = [m for m in tf.getmembers() if m.isfile() and m.name.endswith(".bam.coverage_chr20.txt")]
        for member in members:
            sample = sample_name_from_filename(Path(member.name).name)
            payload = tf.extractfile(member)
            if payload is None:
                continue
            lines = payload.read().decode("utf-8", errors="replace").splitlines()
            medians[sample] = parse_coverage_lines(lines)
    return medians


def load_from_dir(dir_path: Path) -> dict[str, float]:
    medians: dict[str, float] = {}
    for path in sorted(dir_path.glob("*.bam.coverage_chr20.txt")):
        sample = sample_name_from_filename(path.name)
        lines = path.read_text(encoding="utf-8").splitlines()
        medians[sample] = parse_coverage_lines(lines)
    return medians


def write_tsv(medians: dict[str, float], out_path: Path) -> None:
    with out_path.open("w", encoding="utf-8", newline="\n") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["SampleName", "MedianDepthNorm"]) 
        for sample in sorted(medians):
            writer.writerow([sample, f"{medians[sample]:.4f}"])


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute median normalized coverage for each sample.")
    parser.add_argument("input_path", type=Path, help="Coverage directory or coverage.tar.gz")
    parser.add_argument("output_tsv", type=Path, help="Output TSV file")
    args = parser.parse_args()

    if args.input_path.is_dir():
        medians = load_from_dir(args.input_path)
    else:
        medians = load_from_tar(args.input_path)

    write_tsv(medians, args.output_tsv)

    if medians:
        min_sample = min(medians, key=medians.get)
        max_sample = max(medians, key=medians.get)
        print(f"samples={len(medians)}")
        print(f"min_sample={min_sample}\tmedian={medians[min_sample]:.4f}")
        print(f"max_sample={max_sample}\tmedian={medians[max_sample]:.4f}")
    else:
        print("samples=0")

    print(f"output={args.output_tsv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

