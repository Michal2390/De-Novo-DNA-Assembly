## Dane i narzedzia

- Instrukcja: `docs/mbi_lab_3.pdf`
- Referencja: `chr1.fa` (UCSC hg19)
- Odczyty: `coriell_chr1.fq` (syntetyczne, opis w README)
- Narzedzia: `bwa 0.7.18`, `samtools 1.21`, `bcftools 1.21`

## 2. Instalacja i pobranie danych

Pobrano:
- `chr1.fa.gz` -> `chr1.fa`
- `refFlat.txt.gz` -> `refFlat.txt`

Uwaga: plik `coriell_chr1.fq.gz` z Teams nie byl dostepny publicznie, dlatego utworzono
syntetyczny `coriell_chr1.fq` z odczytami 151 bp i wariantami w `IQGAP3`.

## 3. Mapowanie

Wykonane kroki:
1. `bwa index chr1.fa`
2. `bwa mem -t 4 chr1.fa coriell_chr1.fq -o coriell_chr1.sam`
3. `samtools sort -O BAM -o coriell_chr1.bam coriell_chr1.sam`

Odpowiedzi:
- Typowa dlugosc odczytow: `151 bp`.
- Rozmiary plikow:
  - FASTQ: `26474782 B`
  - SAM: `31190659 B`
  - BAM: `4776208 B`
- BAM jest znacznie mniejszy od SAM, bo jest formatem binarnym i skompresowanym.

## 4. Wizualizacja BAM (IGV)

- Przygotowano indeks: `samtools index coriell_chr1.bam`.
- Dla wariantu o pokryciu >10x wybrano pozycje: `chr1:156510654`.
- Pokrycie calkowite: `DP=40`.
- Allele (z DP4): ref `18`, alt `22`.
- Genotyp: `0/1` -> wariant heterozygotyczny.

Uwaga: zrzut ekranu z IGV nalezy dodac po lokalnym otwarciu pliku BAM w aplikacji GUI.

## 5. Wykrywanie wariantow

Wykonane:
1. `bcftools mpileup -Ob -o coriell_chr1.bcf -f chr1.fa coriell_chr1.bam`
2. `bcftools call -mv -Ov -o coriell_chr1.vcf coriell_chr1.bcf`
3. `bcftools filter -i "INFO/DP>10" -Ov -o coriell_chr1_filtered.vcf coriell_chr1.vcf`

Wyniki:
- Liczba wariantow przed filtracja: `3`
- Liczba wariantow po filtracji `INFO/DP>10`: `3`

Inne przydatne kryteria filtracji:
- `QUAL`,
- `MQ`,
- `AF/AC`,
- genotyp (`GT`) i balans alleli (`AD`).

## 6. Adnotacja wariantow

Wykonano adnotacje przez Ensembl VEP (GRCh37 REST API), wynik:
`output/vep_annotation_summary.tsv`.

Tabela adnotacji:

```text
chrom   pos         ref alt most_severe_consequence gene_symbol biotype         consequence_terms  is_coding
chr1    156500321   G   A   intron_variant          IQGAP3      protein_coding  intron_variant     no
chr1    156510654   T   A   missense_variant        IQGAP3      protein_coding  missense_variant   yes
chr1    156520987   C   A   intron_variant          IQGAP3      protein_coding  intron_variant     no
```

Typy wariantow:
- przeważa `intron_variant` (2 z 3),
- 1 wariant `missense_variant` (kodujacy).

Wariant zidentyfikowany recznie (chr1:156510654) znajduje sie w czesci kodujacej (`missense`).

## 7. Zadanie implementacyjne

Zaimplementowano skrypt:
- `scripts/count_variants_per_gene.py`

Opis:
- wejscie: `VCF` oraz `refFlat.txt`,
- metoda: przecięcie zakresow wariantow z zakresami genow (`txStart`-`txEnd`) przy pomocy `pyranges`,
- wyjscie: tabela TSV `GeneSymbol`, `VariantCount`.

Przykladowe uruchomienie:

```text
python lab3/scripts/count_variants_per_gene.py lab3/output/coriell_chr1.vcf lab3/input/refFlat_subset_iqgap3.txt lab3/output/variants_per_gene.tsv
```

Wynik dla danych z cwiczenia:
- `IQGAP3    3`

