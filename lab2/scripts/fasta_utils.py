"""Minimal FASTA helpers used by lab2 scripts.

This avoids external parser dependencies for simple single-line workflows.
"""

from __future__ import annotations

from pathlib import Path


def read_fasta(path: Path) -> list[tuple[str, str]]:
    records: list[tuple[str, str]] = []
    header: str | None = None
    seq_parts: list[str] = []

    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header is not None:
                    records.append((header, "".join(seq_parts)))
                header = line[1:].split()[0]
                seq_parts = []
                continue
            if header is None:
                raise ValueError(f"Invalid FASTA format in {path}: missing header before sequence")
            seq_parts.append(line)

    if header is not None:
        records.append((header, "".join(seq_parts)))

    return records


def write_fasta(records: list[tuple[str, str]], path: Path, line_width: int = 80) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for header, seq in records:
            handle.write(f">{header}\n")
            for i in range(0, len(seq), line_width):
                handle.write(seq[i : i + line_width] + "\n")

