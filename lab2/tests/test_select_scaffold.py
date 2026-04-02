from pathlib import Path

from lab2.scripts.fasta_utils import read_fasta
from lab2.scripts.select_scaffold import choose_sequence_id, read_mapping, save_single_scaffold


def test_choose_sequence_id_for_307340() -> None:
    mapping = {140: "HDID_scaffold0000126"}
    idx, seq_id = choose_sequence_id("307340", mapping)
    assert idx == 140
    assert seq_id == "HDID_scaffold0000126"


def test_read_mapping_and_extract(tmp_path: Path) -> None:
    mapping_file = tmp_path / "mapping.txt"
    mapping_file.write_text("indeks\tidentyfikator sekwencji\n140\tSEQ_140\n", encoding="utf-8")
    mapping = read_mapping(mapping_file)
    assert mapping[140] == "SEQ_140"

    input_fasta = tmp_path / "all.fa"
    input_fasta.write_text(">SEQ_120\nAAAA\n>SEQ_140\nCCGG\n", encoding="utf-8")
    output_fasta = tmp_path / "single.fa"

    save_single_scaffold(input_fasta, output_fasta, "SEQ_140")
    records = read_fasta(output_fasta)
    assert len(records) == 1
    assert records[0][0] == "SEQ_140"
    assert records[0][1] == "CCGG"


