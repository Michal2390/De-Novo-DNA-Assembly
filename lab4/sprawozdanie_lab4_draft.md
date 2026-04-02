## Dane i narzedzia

- Instrukcja: `docs/mbi_lab_4.pdf`
- Dane wejsciowe:
  - `data/coverage` (pokrycie dla 99 probek)
  - `data/codex_output_all` (wyniki CODEX)
  - `data/bed` (regiony WES)
  - DGV: `dgvMerged.txt.gz` (UCSC hg19)
- Implementacja lokalna: Python 3.12, skrypty w `lab4/scripts`

## 2. Instalacja i pobranie danych

Pobrano i wykorzystano:
- `https://github.com/NGSchoolEU/2017/raw/master/CNV_detection/data/bed.tar.gz`
- `https://github.com/NGSchoolEU/2017/raw/master/CNV_detection/data/coverage.tar.gz`
- `https://github.com/NGSchoolEU/2017/raw/master/CNV_detection/data/codex_output_all.tar.gz`
- `https://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/dgvMerged.txt.gz`

Do folderu `lab4/input` skopiowano plik:
- `TGP99_20_4_CODEX_frac.txt`

## 3. Liczenie pokrycia

Zaimplementowano skrypt `scripts/coverage_stats.py`, ktory dla kazdej probki liczy mediane:
- `MedianDepthNorm = median(100 * ReadCount / (Stop - Start))`

Wyniki zapisano do:
- `output/coverage_medians_chr20.tsv`
- `output/coverage_summary.txt`

Odpowiedz na pytanie z instrukcji (najmniejsza / najwieksza mediana):
- najmniejsza mediana: `NA12003`, `22.9630`
- najwieksza mediana: `NA18912`, `135.8333`

## 4. Wykrywanie zmian liczby kopii (CODEX)

Do podsumowania wykorzystano gotowy plik CODEX dla chromosomu 20:
- `input/TGP99_20_4_CODEX_frac.txt`

Podsumowanie (`output/codex_summary.txt`):
- liczba wszystkich CNV: `73`
- delecje: `44`
- duplikacje: `29`
- homozygotyczne delecje (`copy_no == 0`): `0`

Uwagi:
- W tym repozytorium wykonano kompletny etap implementacyjny (zadanie 5) w Python.
- Krok QC/normalizacji z instrukcji (R + pakiet CODEX) opiera sie tutaj na gotowym wyniku
  `TGP99_20_4_CODEX_frac.txt` z archiwum `codex_output_all`.

## 5. Zadanie implementacyjne - adnotacja CNV przez DGV

Zaimplementowano skrypt:
- `scripts/cnv_dgv_annotation.py`

Wejscia:
- wykryte CNV z CODEX: `input/TGP99_20_4_CODEX_frac.txt`
- baza DGV: `lab4_tmp_download/dgvMerged2.txt.gz`

Wyjscie:
- `output/cnv_dgv_annotation.tsv`

Dla kazdego CNV raportowane sa kolumny:
- `dgv_del_overlap_any` - liczba delecji DGV z dowolna czescia wspolna,
- `dgv_dup_overlap_any` - liczba duplikacji DGV z dowolna czescia wspolna,
- `dgv_any_overlap_80pct` - liczba dowolnych wariantow DGV z co najmniej 80% pokryciem dlugosci CNV.

Wynik zbiorczy:
- liczba zaadnotowanych CNV: `73`
- CNV z przynajmniej jednym trafieniem `>=80%`: `33`
- maksymalna liczba nakladajacych sie delecji DGV dla pojedynczego CNV: `73`
- maksymalna liczba nakladajacych sie duplikacji DGV dla pojedynczego CNV: `18`

Fragment tabeli (`output/cnv_dgv_annotation_top5.tsv`):

```text
sample_name chr   cnv st_bp   ed_bp   dgv_del_overlap_any dgv_dup_overlap_any dgv_any_overlap_80pct
NA07357     chr20 del 1638233 1896162 32                  8                   0
NA11829     chr20 del 1558921 1600612 73                  18                  34
NA11829     chr20 dup 1638233 1896162 32                  8                   0
NA11830     chr20 del 1558921 1600612 73                  18                  34
NA11831     chr20 del 1638233 1896162 32                  8                   0
```

## 6. Testy

Wykonano testy jednostkowe dla implementacji Python:
- `tests/test_cnv_dgv_annotation.py`
- `tests/test_coverage_stats.py`

Komenda:

```text
python -m pytest lab4/tests -q
```

