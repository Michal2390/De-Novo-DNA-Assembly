# MBI - Lab 2 (Adnotacja DNA)

Ten folder zawiera komplet plikow startowych i skryptow do realizacji laboratorium 2,
przygotowany dla numeru albumu `307340`.

## Dane przypisania sekwencji

- numer albumu: `307340`
- wzor: `album mod 150`
- wyliczenie: `307340 mod 150 = 140`
- wybrany identyfikator: `HDID_scaffold0000126`
- zrodlo mapowania: `docs/lab2_sequences_id.txt`

Te dane zapisane sa tez w `input/assignment.txt`.

## Struktura katalogu

- `input/` - pliki wejsciowe (single scaffold, dane referencyjne)
- `output/` - wyniki uruchomien narzedzi
- `scripts/` - skrypty pomocnicze do krokow lab2
- `tests/` - testy jednostkowe skryptow
- `tmp/` - pliki tymczasowe
- `sprawozdanie_lab2_draft.md` - szkic sprawozdania
- `sprawozdanie_lab2_wspolne_local.md` - lokalna wersja wspolna

## Skrypty

1. `scripts/select_scaffold.py`
   - wybiera sekwencje po identyfikatorze wyliczonym z numeru albumu
   - tworzy `input/single_scaffold.fa`

2. `scripts/masked_stats.py`
   - liczy liczbe nukleotydow zamaskowanych po RepeatMasker

3. `scripts/gff_stats.py`
   - liczy zdarzenia `expressed_sequence_match` i `protein_match` z pliku GFF

4. `scripts/aa_to_rna.py`
   - zadanie implementacyjne: konwersja FASTA aminokwasow do FASTA RNA

## Minimalny workflow (PowerShell, start z katalogu `MBI`)

1. Umiesc pobrane FASTA (genom, bialka, mRNA) w `input/`.
2. Wyodrebnij scaffold:

```powershell
python lab2/scripts/select_scaffold.py --album 307340 --mapping docs/lab2_sequences_id.txt --input-fasta lab2/input/scaffolds.fa --output-fasta lab2/input/single_scaffold.fa
```

3. Uruchom RepeatMasker i zapisz wynik jako `input/single_scaffold.fa.masked`.
4. Policz statystyki maskowania:

```powershell
python lab2/scripts/masked_stats.py lab2/input/single_scaffold.fa lab2/input/single_scaffold.fa.masked
```

5. Uruchom Maker i wskaz wygenerowany `.gff`.
6. Policz statystyki GFF:

```powershell
python lab2/scripts/gff_stats.py lab2/input/your_maker_output.gff
```

7. Zadanie implementacyjne (AA -> RNA):

```powershell
python lab2/scripts/aa_to_rna.py lab2/input/amino_acids.fa lab2/output/rna.fa
```

Zweryfikowany przyklad na `lab2/input/example_amino_acids.fa` tworzy plik
`lab2/output/example_rna.fa` z rekordami:
- `example_seq_1 -> AUGUCUACUAAUCAA`
- `example_seq_2 -> UUUUGGUAU`

## Testy

```powershell
python -m pytest lab2/tests -q
```

## Wyniki wykonania dla 307340

- RepeatMasker:
  - `lab2/input/single_scaffold.fa.masked`
  - `sequence_length=118160`, `masked_positions=759`, `masked_percent=0.6423`
- Maker:
  - glowny GFF: `lab2/output/HDID_scaffold0000126.maker.gff`
  - pelny output: `lab2/output/single_scaffold.fa.maker.output`
  - liczebnosci cech: `expressed_sequence_match=8`, `protein_match=17`
- BLASTX:
  - zapytanie: `lab2/output/blastx_query.fa`
  - wynik XML: `lab2/output/blastx_result.xml`
  - top 5 organizmow: `Hymenolepis diminuta` (3 trafienia), `Hymenolepis weldensis`, `Hymenolepis microstoma`



