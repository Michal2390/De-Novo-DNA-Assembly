#!/usr/bin/env python
"""Count how many VCF variants overlap each gene from refFlat (txStart-txEnd)."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import pyranges as pr


def load_vcf_as_pyranges(vcf_path: Path) -> pr.PyRanges:
    rows: list[tuple[str, int]] = []
    with vcf_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("#"):
                continue
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            pos_1based = int(parts[1])
            start_0based = pos_1based - 1
            rows.append((chrom, start_0based))

    df = pd.DataFrame(rows, columns=["Chromosome", "Start"])
    if df.empty:
        df = pd.DataFrame(columns=["Chromosome", "Start", "End"])
    else:
        df["End"] = df["Start"] + 1
    return pr.PyRanges(df)


def load_refflat_genes_as_pyranges(refflat_path: Path) -> pr.PyRanges:
    cols = [
        "geneSymbol",
        "name",
        "chrom",
        "strand",
        "txStart",
        "txEnd",
        "cdsStart",
        "cdsEnd",
        "exonCount",
        "exonStarts",
        "exonEnds",
    ]
    df = pd.read_csv(refflat_path, sep="\t", names=cols, usecols=[0, 2, 4, 5])
    df = df.rename(
        columns={
            "geneSymbol": "GeneSymbol",
            "chrom": "Chromosome",
            "txStart": "Start",
            "txEnd": "End",
        }
    )
    return pr.PyRanges(df)


def count_variants_per_gene(vcf_path: Path, refflat_path: Path) -> pd.DataFrame:
    variants = load_vcf_as_pyranges(vcf_path)
    genes = load_refflat_genes_as_pyranges(refflat_path)

    joined = variants.join(genes)
    if joined.df.empty:
        return pd.DataFrame(columns=["GeneSymbol", "VariantCount"])

    out = (
        joined.df.groupby("GeneSymbol", as_index=False)
        .size()
        .rename(columns={"size": "VariantCount"})
        .sort_values(["VariantCount", "GeneSymbol"], ascending=[False, True])
        .reset_index(drop=True)
    )
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Count VCF variants per gene using refFlat coordinates.")
    parser.add_argument("vcf", type=Path, help="Input VCF file")
    parser.add_argument("refflat", type=Path, help="Input refFlat.txt file")
    parser.add_argument("output", type=Path, help="Output TSV with columns: GeneSymbol, VariantCount")
    args = parser.parse_args()

    out = count_variants_per_gene(args.vcf, args.refflat)
    out.to_csv(args.output, sep="\t", index=False)
    print(f"output={args.output}")
    print(f"rows={len(out)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

