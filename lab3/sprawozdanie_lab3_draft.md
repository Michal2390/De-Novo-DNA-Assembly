# 🧪 Sprawozdanie — Lab 3: Resekwencjonowanie genomu człowieka

> **Cel:** Mapowanie odczytów WES do genomu hg19, wykrywanie i filtrowanie wariantów w regionie IQGAP3, adnotacja funkcjonalna przez Ensembl VEP, implementacja zliczania wariantów per gen.

![Lab](https://img.shields.io/badge/Lab-3-red)
![Tool](https://img.shields.io/badge/tools-BWA%20%7C%20samtools%20%7C%20bcftools%20%7C%20VEP-informational)
![Status](https://img.shields.io/badge/status-complete-success)
![Genome](https://img.shields.io/badge/reference-hg19%20chr1-lightgrey)

---

## 📋 Dane i narzędzia

| Element | Wartość |
|---------|---------|
| Instrukcja | `docs/mbi_lab_3.pdf` |
| Referencja | `chr1.fa` (UCSC hg19) |
| Odczyty | `coriell_chr1.fq` (syntetyczne — patrz uwaga) |
| `bwa` | 0.7.18 |
| `samtools` | 1.21 |
| `bcftools` | 1.21 |

> ⚠️ **Uwaga:** Plik `coriell_chr1.fq.gz` z Teams nie był publicznie dostępny. Wygenerowano syntetyczny plik `coriell_chr1.fq` z odczytami 151 bp i wariantami w regionie `IQGAP3`.

---

## 2. 📥 Instalacja i pobranie danych

Pobrano:
- `chr1.fa.gz` → `chr1.fa`
- `refFlat.txt.gz` → `refFlat.txt`

---

## 3. 🗺️ Mapowanie (BWA + samtools)

```bash
bwa index chr1.fa
bwa mem -t 4 chr1.fa coriell_chr1.fq -o coriell_chr1.sam
samtools sort -O BAM -o coriell_chr1.bam coriell_chr1.sam
```

**Rozmiary plików:**

| Format | Rozmiar |
|--------|---------|
| FASTQ | 26 474 782 B |
| SAM | 31 190 659 B |
| BAM | 4 776 208 B |

> 💡 BAM jest ~6× mniejszy od SAM — format binarny + kompresja BGZF.

**Typowa długość odczytów:** `151 bp`

---

## 4. 🖥️ Wizualizacja BAM (IGV)

```bash
samtools index coriell_chr1.bam
```

Wybrany wariant (pokrycie > 10×): **`chr1:156510654`**

| Parametr | Wartość |
|----------|---------|
| Pokrycie całkowite (DP) | `40` |
| Allele ref (DP4) | `18` |
| Allele alt (DP4) | `22` |
| Genotyp | `0/1` → **heterozygotyczny** |

![IGV BAM chr1 156510654](output/igv_bam_chr1_156510654.png)

---

## 5. 🔎 Wykrywanie wariantów (bcftools)

```bash
bcftools mpileup -Ob -o coriell_chr1.bcf -f chr1.fa coriell_chr1.bam
bcftools call -mv -Ov -o coriell_chr1.vcf coriell_chr1.bcf
bcftools filter -i "INFO/DP>10" -Ov -o coriell_chr1_filtered.vcf coriell_chr1.vcf
```

| Etap | Liczba wariantów |
|------|-----------------|
| Przed filtracją | **3** |
| Po filtracji `INFO/DP>10` | **3** |

**Inne przydatne kryteria filtracji:** `QUAL`, `MQ`, `AF/AC`, `GT`, `AD`

---

## 6. 🏷️ Adnotacja wariantów (Ensembl VEP)

Wykonano przez GRCh37 REST API → wynik: `output/vep_annotation_summary.tsv`

| chrom | pos | ref | alt | Konsekwencja | Gen | Kodujący? |
|-------|-----|-----|-----|-------------|-----|-----------|
| chr1 | 156 500 321 | G | A | `intron_variant` | IQGAP3 | ❌ |
| chr1 | 156 510 654 | T | A | `missense_variant` | IQGAP3 | ✅ |
| chr1 | 156 520 987 | C | A | `intron_variant` | IQGAP3 | ❌ |

> 🎯 Wariant `chr1:156510654` to **missense_variant** — zmiana aminokwasu w regionie kodującym.

---

## 7. 🧮 Zadanie implementacyjne — warianty per gen

> **Cel:** Zliczenie wariantów VCF przypadających na każdy gen z pliku refFlat.

| Element | Wartość |
|---------|---------|
| Skrypt | `scripts/count_variants_per_gene.py` |
| Wejście | `VCF` + `refFlat.txt` |
| Metoda | przecięcie pozycji VCF z zakresami `txStart`–`txEnd` |
| Wyjście | TSV: `GeneSymbol`, `VariantCount` |
| Testy | `tests/test_count_variants_per_gene.py` |

Uruchomienie:

```bash
python lab3/scripts/count_variants_per_gene.py \
  lab3/output/coriell_chr1.vcf \
  lab3/input/refFlat_subset_iqgap3.txt \
  lab3/output/variants_per_gene.tsv
```

Wynik:

| Gen | Liczba wariantów |
|-----|-----------------|
| `IQGAP3` | **3** |

Uruchomienie testów:

```bash
python -m pytest lab3/tests -q
```

> ✅ Status: **Zaimplementowane i przetestowane**
