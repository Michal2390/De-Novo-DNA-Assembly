from pathlib import Path

from lab3.scripts.count_variants_per_gene import count_variants_per_gene


def test_count_variants_per_gene(tmp_path: Path) -> None:
    vcf = tmp_path / "x.vcf"
    vcf.write_text(
        "##fileformat=VCFv4.2\n"
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n"
        "chr1\t110\t.\tA\tG\t.\tPASS\t.\n"
        "chr1\t210\t.\tC\tT\t.\tPASS\t.\n"
        "chr2\t50\t.\tG\tA\t.\tPASS\t.\n",
        encoding="utf-8",
    )

    refflat = tmp_path / "refFlat.txt"
    refflat.write_text(
        "GENE1\tNM_1\tchr1\t+\t100\t200\t100\t200\t1\t100,\t200,\n"
        "GENE2\tNM_2\tchr1\t+\t200\t300\t200\t300\t1\t200,\t300,\n"
        "GENE3\tNM_3\tchr2\t+\t10\t80\t10\t80\t1\t10,\t80,\n",
        encoding="utf-8",
    )

    out = count_variants_per_gene(vcf, refflat)

    got = {row.GeneSymbol: int(row.VariantCount) for row in out.itertuples(index=False)}
    assert got == {"GENE1": 1, "GENE2": 1, "GENE3": 1}

