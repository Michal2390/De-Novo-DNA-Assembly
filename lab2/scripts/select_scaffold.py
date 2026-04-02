#!/usr/bin/env python
"""Select one scaffold/contig sequence from a FASTA file by student album number."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

try:
    from lab2.scripts.fasta_utils import read_fasta, write_fasta
except ModuleNotFoundError:  # direct script execution
    from fasta_utils import read_fasta, write_fasta


def read_mapping(mapping_path: Path) -> dict[int, str]:
    mapping: dict[int, str] = {}
    with mapping_path.open("r", encoding="utf-8") as handle:
        reader = csv.reader(handle, delimiter="\t")
        next(reader, None)  # header
        for row in reader:
            if len(row) < 2:
                continue
            idx = int(row[0].strip())
            seq_id = row[1].strip()
            mapping[idx] = seq_id
    return mapping


def extract_digits(value: str) -> int:
    digits = "".join(ch for ch in value if ch.isdigit())
    if not digits:
        raise ValueError("Album number must contain at least one digit.")
    return int(digits)


def choose_sequence_id(album_number: str, mapping: dict[int, str], modulo: int = 150) -> tuple[int, str]:
    album_int = extract_digits(album_number)
    idx = album_int % modulo
    if idx not in mapping:
        raise KeyError(f"Index {idx} is missing in mapping file.")
    return idx, mapping[idx]


def save_single_scaffold(input_fasta: Path, output_fasta: Path, wanted_id: str) -> None:
    for record_id, seq in read_fasta(input_fasta):
        if record_id == wanted_id:
            write_fasta([(record_id, seq)], output_fasta)
            return
    raise ValueError(f"Sequence ID '{wanted_id}' was not found in {input_fasta}.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract single scaffold FASTA for a selected student index.")
    parser.add_argument("--album", required=True, help="Album number, e.g. 307340")
    parser.add_argument("--mapping", type=Path, required=True, help="Path to lab2_sequences_id.txt")
    parser.add_argument("--input-fasta", type=Path, required=True, help="Path to scaffold FASTA file")
    parser.add_argument("--output-fasta", type=Path, default=Path("input/single_scaffold.fa"), help="Output path")
    parser.add_argument("--modulo", type=int, default=150, help="Modulo used to select mapping index")
    args = parser.parse_args()

    mapping = read_mapping(args.mapping)
    idx, seq_id = choose_sequence_id(args.album, mapping, args.modulo)
    save_single_scaffold(args.input_fasta, args.output_fasta, seq_id)

    print(f"album_number={args.album}")
    print(f"selected_index={idx}")
    print(f"selected_sequence_id={seq_id}")
    print(f"output_fasta={args.output_fasta}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



