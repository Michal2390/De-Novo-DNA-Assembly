# 🔬 Sprawozdanie - Lab 1: De Novo DNA Assembly

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

Wykonane polecenie (uruchomione w Docker'ze):

```bash
docker run --rm -v /tmp:/tmp -w /tmp wkusmirek/dnaasm dnaasm -assembly \
  -k 55 \
  -genome_length 1641468 \
  -paired_reads_algorithm 1 \
  -insert_size_mean_inward 400 \
  -insert_size_std_dev_inward 20 \
  -single_edge_counter_threshold 5 \
  -i1_1 pirs_reads_100_400_1.fq \
  -i1_2 pirs_reads_100_400_2.fq \
  -output_file_name contigs.fa
```

**Parametry:**
- `-k 55`: Wymiar grafu de Bruijn'a (k-mer)
- `-genome_length 1641468`: Długość genomu referencyjnego w par bazowych
- `-paired_reads_algorithm 1`: Obsługa odczytów sparowanych (forward-reverse)
- `-insert_size_mean_inward 400 bp`: Średnia odległość między końcami sparowanych odczytów
- `-insert_size_std_dev_inward 20`: Odchylenie standardowe od średniej odległości
- `-single_edge_counter_threshold 5`: Próg krawędzi w grafie de Bruijn'a

Wynik: `output/contigs.fa` (rozmiar: ~3.12 MB, liczba kontigów: 274)

---

## 5. 📊 Ocena jakości asemblacji (QUAST)

Wykonane polecenie:

```bash
docker run --rm -v /tmp:/tmp -w /tmp staphb/quast:5.3.0 \
  python /quast-5.3.0/quast.py -R ref.fa -o quast_results contigs.fa
```

Metryk QUAST:
- **Liczba kontigów**: 274
- **Całkowita długość**: ~3.12 MBytes
- **Średnia długość kontiga**: ~11,394 bp  
- **Mediana długości**: 216 bp
- **N50**: 53,050 bp

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

