#!/usr/bin/env python
"""Convert amino acid FASTA sequences to RNA FASTA sequences."""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    from lab2.scripts.fasta_utils import read_fasta, write_fasta
except ModuleNotFoundError:  # direct script execution
    from fasta_utils import read_fasta, write_fasta

# One deterministic codon per amino acid for reproducible output.
AA_TO_CODON = {
    "A": "GCU",
    "C": "UGU",
    "D": "GAU",
    "E": "GAA",
    "F": "UUU",
    "G": "GGU",
    "H": "CAU",
    "I": "AUU",
    "K": "AAA",
    "L": "UUA",
    "M": "AUG",
    "N": "AAU",
    "P": "CCU",
    "Q": "CAA",
    "R": "CGU",
    "S": "UCU",
    "T": "ACU",
    "V": "GUU",
    "W": "UGG",
    "Y": "UAU",
    "*": "UAA",
}


def amino_acid_to_rna(sequence: str) -> str:
    codons: list[str] = []
    for aa in sequence.upper():
        if aa in {" ", "\t", "\n", "\r"}:
            continue
        if aa not in AA_TO_CODON:
            raise ValueError(f"Unsupported amino acid symbol: {aa!r}")
        codons.append(AA_TO_CODON[aa])
    return "".join(codons)


def convert_file(input_fasta: Path, output_fasta: Path) -> int:
    count = 0
    records: list[tuple[str, str]] = []
    for record_id, aa_seq in read_fasta(input_fasta):
        rna_seq = amino_acid_to_rna(aa_seq)
        records.append((f"{record_id} translated_to_rna", rna_seq))
        count += 1

    write_fasta(records, output_fasta)
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert amino acid FASTA sequences to RNA FASTA")
    parser.add_argument("input_fasta", type=Path, help="Input FASTA with amino acid sequences")
    parser.add_argument("output_fasta", type=Path, help="Output FASTA with RNA sequences")
    args = parser.parse_args()

    converted = convert_file(args.input_fasta, args.output_fasta)
    print(f"input={args.input_fasta}")
    print(f"output={args.output_fasta}")
    print(f"records_converted={converted}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



