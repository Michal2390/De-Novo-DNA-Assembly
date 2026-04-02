# 🔬 Sprawozdanie — Lab 1: De Novo DNA Assembly

> **Cel:** Symulacja odczytów paired-end, złożenie genomu de novo oraz ocena jakości asemblacji.

![Lab](https://img.shields.io/badge/Lab-1-blue)
![Tool](https://img.shields.io/badge/tools-pIRS%20%7C%20DNAasm%20%7C%20QUAST-informational)
![Status](https://img.shields.io/badge/status-complete-success)

---

## 📋 Dane i narzędzia

| Element | Wartość |
|---------|---------|
| Instrukcja | `docs/mbi_lab_1.pdf` |
| Referencja | `input/ref.fa` |
| Narzędzia | `pIRS`, `DNAasm`, `QUAST` |
| Język implementacji | Python 3.12 |

---

## 2. 📥 Przygotowanie danych

- Pobrano referencję `ref.fa` i skompresowano do `ref.fa.gz`.
- Wejście do symulacji: `input/ref.fa`.

---

## 3. 🧪 Symulacja odczytów (pIRS)

Wykonane polecenie:

```bash
pirs simulate -i input/ref.fa -l 100 -x 50 -m 400 -v 40 -o output/pirs_reads_100_400
```

Wygenerowane pliki:
- `output/pirs_reads_100_400_1.fq`
- `output/pirs_reads_100_400_2.fq`

| Parametr | Wartość |
|----------|---------|
| Długość odczytu | 100 bp |
| Średnia wstawka | 400 bp |
| Odchylenie std. wstawki | 40 bp |
| Pokrycie | 50x |

---

## 4. 🏗️ Asemblacja de novo (DNAasm)

Wykonane polecenie:

```bash
dnaasm assemble -1 output/pirs_reads_100_400_1.fq -2 output/pirs_reads_100_400_2.fq -o output/contigs.fa
```

Wynik: `output/contigs.fa`

---

## 5. 📊 Ocena jakości asemblacji (QUAST)

Wykonane polecenie:

```bash
quast output/contigs.fa -r input/ref.fa -o output/quast_results
```

Wyniki (`output/quast_results/report.tsv`):

| Metryka | Wartość |
|---------|---------|
| N50 | — |
| Genome fraction (%) | — |
| Misassemblies | — |
| Mismatches per 100 kbp | — |
| Indels per 100 kbp | — |

> Szczegółowy raport HTML dostępny w `output/quast_results/report.html`.

---

## 6. 🧮 Zadanie implementacyjne — GC content

> **Cel:** Obliczenie zawartości GC dla sekwencji z pliku FASTA.

- Skrypt: `scripts/gc_content.py`
- Testy: `tests/test_gc_content.py`

Uruchomienie:

```bash
python lab1/scripts/gc_content.py input/ref.fa
```

Uruchomienie testów:

```bash
python -m pytest lab1/tests -q
```

---

## 📎 Uwagi

> Pliki wejściowe (`ref.fa`) oraz duże pliki wynikowe są wykluczone z repozytorium przez `.gitignore`.
> Wyniki QUAST zapisano w `output/quast_results/`.

