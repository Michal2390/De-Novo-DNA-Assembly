# 🧩 Sprawozdanie — Lab 2: Adnotacja DNA

> **Cel:** Wybór, maskowanie i adnotacja wybranego scaffoldu genomowego *Hymenolepis diminuta*, oraz implementacja konwersji aminokwasów do RNA.

![Lab](https://img.shields.io/badge/Lab-2-orange)
![Tool](https://img.shields.io/badge/tools-RepeatMasker%20%7C%20Maker%20%7C%20BLAST-informational)
![Status](https://img.shields.io/badge/status-complete-success)
![Organism](https://img.shields.io/badge/organism-Hymenolepis%20diminuta-9cf)

---

## 📋 Dane wejściowe

| Element | Wartość |
|---------|---------|
| Numer albumu | `307340` |
| Wyliczenie indeksu | `307340 mod 150 = 140` |
| Wybrany scaffold | `HDID_scaffold0000126` |
| Źródło mapowania | `docs/lab2_sequences_id.txt` |
| Instrukcja | `docs/mbi_lab_2.pdf` |

---

## 2.2 📥 Przygotowanie danych

- Wybrany identyfikator: `HDID_scaffold0000126`
- Plik wyjściowy po ekstrakcji: `input/single_scaffold.fa`

```bash
python lab2/scripts/select_scaffold.py \
  --album 307340 \
  --mapping docs/lab2_sequences_id.txt \
  --input-fasta lab2/input/hymenolepis_diminuta.PRJEB507.WBPS10.genomic.fa \
  --output-fasta lab2/input/single_scaffold.fa
```

---

## 2.3 🧹 Maskowanie genomu (RepeatMasker)

| Parametr | Wartość |
|----------|---------|
| Plik wejściowy | `input/single_scaffold.fa` |
| Plik zamaskowany | `input/single_scaffold.fa.masked` |
| Długość sekwencji | `118 160 bp` |
| Zamaskowane pozycje | `759` |
| Procent maskowania | `0.6423 %` |

**Odpowiedzi na pytania:**

> 1️⃣ **Ile nukleotydów zostało zamaskowanych?**
> Zamaskowano `759` nukleotydów.

> 2️⃣ **Czy to pojedyncze nukleotydy czy ciągi?**
> To ciągi: wykryto `17` ciągów, `singletons = 0`, najdłuższy ciąg `82 bp`, średnia długość `44.65 bp`.

> 3️⃣ **Jak maskowanie wpływa na mapowanie?**
> Ogranicza fałszywe dopasowania w regionach repetytywnych i poprawia specyficzność mapowania mRNA/białek.

---

## 2.4 🗺️ Mapowanie i adnotacja strukturalna (Maker)

- Plik GFF: `output/HDID_scaffold0000126.maker.gff`

| Typ cechy | Liczba |
|-----------|--------|
| `expressed_sequence_match` | **8** |
| `protein_match` | **17** |

Fragment pliku GFF:

```text
##gff-version 3
HDID_scaffold0000126  .  contig  1  118160  .  .  .  ID=HDID_scaffold0000126
HDID_scaffold0000126  repeatmasker  match  4417  5012  891  +  .  ID=...Mariner-9_HSal
HDID_scaffold0000126  repeatmasker  match  10784  10833  236  +  .  ID=...Arnold4
```

**Odpowiedzi na pytania:**

> 1️⃣ **Jakie informacje są w GFF?**
> Położenia cech genomowych (start/stop), typ cechy, źródło adnotacji, strand, atrybuty ID/Name.

> 2️⃣ **Znaczenie typów:**
> - `expressed_sequence_match` — dopasowanie do transkryptu (mRNA/EST),
> - `protein_match` — dopasowanie do sekwencji białka.

---

## 2.5 🔍 Adnotacja funkcjonalna (BLASTX)

Wybrany rekord `expressed_sequence_match`:

```text
HDID_scaffold0000126  blastn  expressed_sequence_match  53705  57114  224  -  .
ID=HDID_scaffold0000126:hit:7:3.2.0.0;Name=HDID_0000794201-mRNA-1
```

Wyodrębniona sekwencja DNA (53705–57114) zapisana w `output/blastx_query.fa`.

**Top 5 organizmów z BLAST:**

| # | Organizm | Identity | E-value |
|---|----------|----------|---------|
| 1 | *Hymenolepis diminuta* | 87.69 % | 2.01 × 10⁻¹¹⁷ |
| 2 | *Hymenolepis diminuta* | 86.89 % | 7.72 × 10⁻¹¹³ |
| 3 | *Hymenolepis diminuta* | 97.92 % | 3.97 × 10⁻⁸³ |
| 4 | *Hymenolepis weldensis* | 93.06 % | 1.42 × 10⁻⁷⁸ |
| 5 | *Hymenolepis microstoma* | 89.47 % | 7.03 × 10⁻⁶⁸ |

**Odpowiedzi na pytania:**

> 1️⃣ **Co oznacza E-value?**
> Oczekiwana liczba przypadkowych trafień o podobnym lub lepszym wyniku; im mniejsza, tym bardziej istotne dopasowanie.

> 2️⃣ **Interpretacja listy organizmów:**
> Dominujące trafienia dla *Hymenolepis diminuta* są zgodne z gatunkiem analizowanego genomu. Obecność *H. weldensis* i *H. microstoma* wskazuje na bliskie pokrewieństwo ewolucyjne.

---

## 3. 🧮 Zadanie implementacyjne — AA → RNA

> **Cel:** Konwersja sekwencji aminokwasów (FASTA) do sekwencji RNA.

| Element | Wartość |
|---------|---------|
| Skrypt | `scripts/aa_to_rna.py` |
| Wejście | FASTA z aminokwasami |
| Wyjście | FASTA z sekwencjami RNA |
| Testy | `tests/test_aa_to_rna.py` |

Uruchomienie:

```bash
python lab2/scripts/aa_to_rna.py lab2/input/example_amino_acids.fa lab2/output/example_rna.fa
```

Zweryfikowany wynik:

| Sekwencja | RNA |
|-----------|-----|
| `example_seq_1` | `AUGUCUACUAAUCAA` |
| `example_seq_2` | `UUUUGGUAU` |

Uruchomienie testów:

```bash
python -m pytest lab2/tests -q
```

> ✅ Status: **Zaimplementowane i przetestowane**
