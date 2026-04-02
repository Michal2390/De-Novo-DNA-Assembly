from pathlib import Path

from lab2.scripts.aa_to_rna import amino_acid_to_rna, convert_file
from lab2.scripts.fasta_utils import read_fasta


def test_amino_acid_to_rna_basic() -> None:
    assert amino_acid_to_rna("MA*") == "AUGGCUUAA"


def test_convert_file(tmp_path: Path) -> None:
    input_fasta = tmp_path / "aa.fa"
    output_fasta = tmp_path / "rna.fa"
    input_fasta.write_text(">seq1\nMA\n>seq2\nFW\n", encoding="utf-8")

    converted = convert_file(input_fasta, output_fasta)

    records = read_fasta(output_fasta)
    assert converted == 2
    assert records[0][1] == "AUGGCU"
    assert records[1][1] == "UUUUGG"


