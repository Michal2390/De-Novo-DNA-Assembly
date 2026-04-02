from pathlib import Path

from lab4.scripts.cnv_dgv_annotation import (
    annotate_calls,
    classify_dgv_variant_type,
    overlap_len,
    read_codex_calls,
    read_dgv,
)


def test_classify_dgv_variant_type() -> None:
    assert classify_dgv_variant_type("deletion") == "deletion"
    assert classify_dgv_variant_type("loss") == "deletion"
    assert classify_dgv_variant_type("duplication") == "duplication"
    assert classify_dgv_variant_type("gain+loss") == "deletion"


def test_annotate_calls(tmp_path: Path) -> None:
    codex = tmp_path / "calls.txt"
    codex.write_text(
        "sample_name chr cnv st_bp ed_bp length_kb st_exon ed_exon raw_cov norm_cov copy_no lratio mBIC\n"
        "S1 20 del 100 200 0.1 1 2 10 20 1 2 3\n"
        "S2 20 dup 300 400 0.1 3 4 10 20 3 2 3\n",
        encoding="utf-8",
    )

    dgv = tmp_path / "dgv.txt"
    dgv.write_text(
        "1\tchr20\t90\t110\tx\t0\t+\t0\t0\t0\tdeletion\n"
        "1\tchr20\t150\t260\tx\t0\t+\t0\t0\t0\tduplication\n"
        "1\tchr20\t320\t390\tx\t0\t+\t0\t0\t0\tgain\n",
        encoding="utf-8",
    )

    calls = read_codex_calls(codex)
    dgv_variants = read_dgv(dgv)
    rows = annotate_calls(calls, dgv_variants)

    assert len(rows) == 2
    assert rows[0]["dgv_del_overlap_any"] == 1
    assert rows[0]["dgv_dup_overlap_any"] == 1
    assert rows[0]["dgv_any_overlap_80pct"] == 0
    assert rows[1]["dgv_dup_overlap_any"] == 1


def test_overlap_len() -> None:
    from lab4.scripts.cnv_dgv_annotation import Interval

    a = Interval(chrom="chr1", start=100, end=200)
    b = Interval(chrom="chr1", start=150, end=210)
    c = Interval(chrom="chr2", start=150, end=210)

    assert overlap_len(a, b) == 50
    assert overlap_len(a, c) == 0

