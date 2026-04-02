#!/usr/bin/env python
"""Summarize CODEX CNV calls."""

from __future__ import annotations

import argparse
from pathlib import Path

from lab4.scripts.cnv_dgv_annotation import read_codex_calls


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize CODEX calls (total, del, dup, homozygous deletions).")
    parser.add_argument("codex_calls", type=Path, help="CODEX CNV calls file")
    parser.add_argument("output_txt", type=Path, help="Output TXT summary")
    args = parser.parse_args()

    calls = read_codex_calls(args.codex_calls)
    total = len(calls)
    deletions = sum(1 for x in calls if x.cnv.lower().startswith("del"))
    duplications = sum(1 for x in calls if x.cnv.lower().startswith("dup"))

    # copy_no is not loaded by the shared parser, so we estimate from CNV class only here.
    # exact homozygous deletion count is read from the source file directly below.
    hom_del = 0
    with args.codex_calls.open("r", encoding="utf-8") as handle:
        header = handle.readline().strip().split()
        idx = {name: i for i, name in enumerate(header)}
        if "copy_no" in idx:
            for line in handle:
                parts = line.strip().split()
                if not parts:
                    continue
                if float(parts[idx["copy_no"]]) == 0.0:
                    hom_del += 1

    text = (
        f"total_calls={total}\n"
        f"deletions={deletions}\n"
        f"duplications={duplications}\n"
        f"homozygous_deletions_copy_no_0={hom_del}\n"
    )
    args.output_txt.write_text(text, encoding="utf-8")
    print(text, end="")
    print(f"output={args.output_txt}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

