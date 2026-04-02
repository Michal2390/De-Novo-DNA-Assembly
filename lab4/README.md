# MBI - Lab 4 (Analiza danych sekwencyjnych czlowieka)

Ten folder zawiera komplet materialow do laboratorium 4.

## Struktura

- `input/` - dane wejsciowe dla zadania i metadane
- `output/` - wyniki analiz i podsumowania
- `scripts/` - skrypty implementacyjne i pipeline
- `tests/` - testy jednostkowe
- `tmp/` - pliki tymczasowe
- `sprawozdanie_lab4_draft.md` - glowne sprawozdanie

## Dane

- instrukcja: `docs/mbi_lab_4.pdf`
- archiwa (zgodnie z instrukcja):
  - `https://github.com/NGSchoolEU/2017/raw/master/CNV_detection/data/bed.tar.gz`
  - `https://github.com/NGSchoolEU/2017/raw/master/CNV_detection/data/coverage.tar.gz`
  - `https://github.com/NGSchoolEU/2017/raw/master/CNV_detection/data/codex_output_all.tar.gz`
- DGV (UCSC, hg19):
  - `https://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/dgvMerged.txt.gz`

Dodatkowe linki FTP przekazane przez uzytkownika zapisano w `input/ftp_sources.txt`.

## Skrypty

1. `scripts/coverage_stats.py`
   - liczy mediany znormalizowanego pokrycia na probke (`(100 * ReadCount) / (Stop-Start)`)
2. `scripts/codex_summary.py`
   - podsumowuje liczbe CNV z pliku CODEX (`del`, `dup`, `copy_no == 0`)
3. `scripts/cnv_dgv_annotation.py`
   - zadanie implementacyjne: adnotacja CNV z DGV
   - dla kazdego CNV zwraca:
     - ile delecji DGV ma czesc wspolna,
     - ile duplikacji DGV ma czesc wspolna,
     - ile dowolnych wariantow DGV ma >=80% czesci wspolnej z CNV
4. `scripts/run_lab4_pipeline.py`
   - laczy kroki i generuje wszystkie pliki wynikowe

## Uruchomienie (PowerShell, start z katalogu `MBI`)

```powershell
python -m lab4.scripts.run_lab4_pipeline --tmp-dir "C:\Users\Michał\OneDrive\Desktop\Studia magisterskie EITI\MBI\lab4_tmp_download" --lab4-dir "C:\Users\Michał\OneDrive\Desktop\Studia magisterskie EITI\MBI\lab4"
```

## Testy

```powershell
python -m pytest lab4/tests -q
```

## Wygenerowane wyniki

- `output/coverage_medians_chr20.tsv`
- `output/coverage_summary.txt`
- `output/codex_summary.txt`
- `output/cnv_dgv_annotation.tsv`
- `output/cnv_dgv_annotation_top5.tsv`

