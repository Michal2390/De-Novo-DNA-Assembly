#!/usr/bin/env python
"""Count VCF variants per gene using refFlat txStart-txEnd intervals.

Implementation is dependency-free (standard library only).
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path


def load_variants(vcf_path: Path) -> list[tuple[str, int]]:
    variants: list[tuple[str, int]] = []
    with vcf_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("#"):
                continue
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            pos_1based = int(parts[1])
            variants.append((chrom, pos_1based - 1))
    return variants


def load_genes(refflat_path: Path) -> list[tuple[str, str, int, int]]:
    genes: list[tuple[str, str, int, int]] = []
    with refflat_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 6:
                continue
            gene_symbol = parts[0]
            chrom = parts[2]
            tx_start = int(parts[4])
            tx_end = int(parts[5])
            genes.append((gene_symbol, chrom, tx_start, tx_end))
    return genes


def count_variants_per_gene(vcf_path: Path, refflat_path: Path) -> list[tuple[str, int]]:
    variants = load_variants(vcf_path)
    genes = load_genes(refflat_path)

    by_chrom: dict[str, list[tuple[str, int, int]]] = defaultdict(list)
    for gene_symbol, chrom, tx_start, tx_end in genes:
        by_chrom[chrom].append((gene_symbol, tx_start, tx_end))

    counts: dict[str, int] = defaultdict(int)
    for chrom, pos in variants:
        for gene_symbol, tx_start, tx_end in by_chrom.get(chrom, []):
            if tx_start <= pos < tx_end:
                counts[gene_symbol] += 1

    return sorted(counts.items(), key=lambda x: (-x[1], x[0]))


def write_tsv(rows: list[tuple[str, int]], output_path: Path) -> None:
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("GeneSymbol\tVariantCount\n")
        for gene_symbol, count in rows:
            handle.write(f"{gene_symbol}\t{count}\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Count VCF variants per gene from refFlat coordinates.")
    parser.add_argument("vcf", type=Path, help="Input VCF file")
    parser.add_argument("refflat", type=Path, help="Input refFlat.txt file")
    parser.add_argument("output", type=Path, help="Output TSV path")
    args = parser.parse_args()

    rows = count_variants_per_gene(args.vcf, args.refflat)
    write_tsv(rows, args.output)
    print(f"output={args.output}")
    print(f"rows={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


