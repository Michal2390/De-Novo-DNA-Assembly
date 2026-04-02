# 📊 Sprawozdanie — Lab 4: Analiza CNV (CODEX + DGV)

> **Cel:** Analiza głębokości pokrycia eksonów, podsumowanie zmian liczby kopii DNA wykrytych przez CODEX oraz adnotacja CNV z użyciem bazy wariantów strukturalnych DGV.

![Lab](https://img.shields.io/badge/Lab-4-purple)
![Tool](https://img.shields.io/badge/tools-CODEX%20%7C%20DGV%20%7C%20Python-informational)
![Status](https://img.shields.io/badge/status-complete-success)
![Genome](https://img.shields.io/badge/reference-hg19%20chr20-lightgrey)
![Samples](https://img.shields.io/badge/samples-99%20×%201000%20Genomes-9cf)

---

## 📋 Dane i narzędzia

| Element | Wartość |
|---------|---------|
| Instrukcja | `docs/mbi_lab_4.pdf` |
| Dane pokrycia | `coverage/` — 99 próbek z 1000 Genomes (chr20) |
| Wyniki CODEX | `codex_output_all/TGP99_20_4_CODEX_frac.txt` |
| Regiony WES | `bed/20130108.exome.targets.bed` |
| Baza DGV | `dgvMerged.txt.gz` (UCSC hg19) |
| Implementacja | Python 3.12, skrypty w `lab4/scripts/` |

Źródła danych:

```
https://github.com/NGSchoolEU/2017/raw/master/CNV_detection/data/bed.tar.gz
https://github.com/NGSchoolEU/2017/raw/master/CNV_detection/data/coverage.tar.gz
https://github.com/NGSchoolEU/2017/raw/master/CNV_detection/data/codex_output_all.tar.gz
https://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/dgvMerged.txt.gz
```

---

## 3. 📈 Liczenie pokrycia

Skrypt `scripts/coverage_stats.py` oblicza dla każdej próbki medianę znormalizowanej głębokości:

```
MedianDepthNorm = median(100 × ReadCount / (Stop − Start))
```

Wyniki → `output/coverage_medians_chr20.tsv`, `output/coverage_summary.txt`

| Próbka | Mediana głębokości |
|--------|-------------------|
| Najmniejsza — `NA12003` | **22.9630** |
| Największa — `NA18912` | **135.8333** |
| Łączna liczba próbek | **99** |

---

## 4. 🔬 Wykrywanie CNV (CODEX)

Plik wynikowy: `input/TGP99_20_4_CODEX_frac.txt`

| Statystyka | Wartość |
|-----------|---------|
| Wszystkie CNV | **73** |
| Delecje (`del`) | **44** |
| Duplikacje (`dup`) | **29** |
| Homozygotyczne delecje (`copy_no = 0`) | **0** |

> ℹ️ Kroki QC, normalizacji i segmentacji (R + pakiet CODEX) wykonano na gotowym wyniku z archiwum `codex_output_all`. Etap implementacyjny zrealizowano w Pythonie.

**Kolumny pliku wynikowego CODEX:**

| Kolumna | Opis |
|---------|------|
| `sample_name` | Identyfikator próbki |
| `chr` | Chromosom |
| `cnv` | Typ zmiany (`del` / `dup`) |
| `st_bp` / `ed_bp` | Pozycja start/end w bp |
| `copy_no` | Szacowana liczba kopii |
| `lratio` | Współczynnik wiarygodności |

---

## 5. 🧮 Zadanie implementacyjne — adnotacja CNV przez DGV

> **Cel:** Dla każdego wykrytego CNV: zliczenie nakładających się wariantów strukturalnych z bazy DGV.

| Element | Wartość |
|---------|---------|
| Skrypt | `scripts/cnv_dgv_annotation.py` |
| Wejście 1 | `input/TGP99_20_4_CODEX_frac.txt` |
| Wejście 2 | `dgvMerged.txt.gz` (UCSC hg19) |
| Wyjście | `output/cnv_dgv_annotation.tsv` |
| Testy | `tests/test_cnv_dgv_annotation.py` |

**Raportowane kolumny:**

| Kolumna | Opis |
|---------|------|
| `dgv_del_overlap_any` | Liczba delecji DGV z dowolnym nakładaniem |
| `dgv_dup_overlap_any` | Liczba duplikacji DGV z dowolnym nakładaniem |
| `dgv_any_overlap_80pct` | Liczba wariantów DGV z ≥ 80 % pokryciem długości CNV |

**Wyniki zbiorcze:**

| Metryka | Wartość |
|---------|---------|
| Zaadnotowane CNV | **73** |
| CNV z trafieniem ≥ 80 % | **33** |
| Max. nakładające się delecje DGV (1 CNV) | **73** |
| Max. nakładające się duplikacje DGV (1 CNV) | **18** |

**Fragment tabeli wynikowej** (`output/cnv_dgv_annotation_top5.tsv`):

| sample | chr | cnv | st_bp | ed_bp | del_any | dup_any | 80pct |
|--------|-----|-----|-------|-------|---------|---------|-------|
| NA07357 | chr20 | del | 1 638 233 | 1 896 162 | 32 | 8 | 0 |
| NA11829 | chr20 | del | 1 558 921 | 1 600 612 | 73 | 18 | 34 |
| NA11829 | chr20 | dup | 1 638 233 | 1 896 162 | 32 | 8 | 0 |
| NA11830 | chr20 | del | 1 558 921 | 1 600 612 | 73 | 18 | 34 |
| NA11831 | chr20 | del | 1 638 233 | 1 896 162 | 32 | 8 | 0 |

Uruchomienie:

```bash
python -m lab4.scripts.run_lab4_pipeline \
  --tmp-dir lab4_tmp_download \
  --lab4-dir lab4
```

---

## 6. ✅ Testy

| Plik testowy | Zakres |
|-------------|--------|
| `tests/test_cnv_dgv_annotation.py` | klasyfikacja typów DGV, nakładanie interwałów, adnotacja |
| `tests/test_coverage_stats.py` | obliczanie mediany znormalizowanego pokrycia |

```bash
python -m pytest lab4/tests -q
# 4 passed in 0.04s
```

> ✅ Status: **Zaimplementowane i przetestowane**
