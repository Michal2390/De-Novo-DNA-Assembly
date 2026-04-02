# MBI - Lab 3 (Resekwencjonowanie genomu czlowieka)

Ten folder zawiera komplet materialow do laboratorium 3.

## Uwagi o danych

Instrukcja wymaga pliku `coriell_chr1.fq.gz` z Teams. Ten plik nie byl publicznie dostepny,
dlatego pipeline wykonano na syntetycznym pliku `coriell_chr1.fq` wygenerowanym na referencji
`chr1.fa`, z zaszytymi wariantami w regionie genu `IQGAP3`.

## Struktura

- `input/` - lekkie pliki wejsciowe i metadane
- `output/` - wyniki mapowania i wariantow
- `scripts/` - skrypty pomocnicze i implementacyjne
- `tests/` - testy jednostkowe
- `sprawozdanie_lab3_draft.md` - kompletne sprawozdanie

## Skrypty

- `scripts/count_variants_per_gene.py` - zadanie implementacyjne (refFlat + VCF -> tabela genow)

## Uruchomienie zadania implementacyjnego

```powershell
python lab3/scripts/count_variants_per_gene.py lab3/output/coriell_chr1.vcf lab3/input/refFlat_subset_iqgap3.txt lab3/output/variants_per_gene.tsv
```

## Testy

```powershell
python -m pytest lab3/tests -q
```

