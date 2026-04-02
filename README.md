# De Novo DNA Assembly

This repository contains coursework materials for the MBI laboratory on de novo DNA assembly.

## What This Project Is

This repository now covers the full MBI laboratory path (Lab 1 to Lab 4), not only the initial de novo assembly task. It combines practical workflows, small implementation tasks in Python, and written reports for each exercise.

At a high level, the project includes:

- assembly and quality assessment of short-read sequencing data,
- DNA annotation workflow on a selected scaffold,
- human resequencing analysis with variant calling and annotation,
- copy-number variation (CNV) interpretation with external structural-variant resources.

## Why This Project Exists

The goal is to practice end-to-end bioinformatics analysis across multiple related topics and to document both tooling and interpretation. Each lab adds a different skill layer:

- data preparation and command-line genomics workflows,
- quality control and biological interpretation of outputs,
- implementation of task-specific scripts (with tests),
- reproducible reporting of methods and results.

## Lab Objectives

### Lab 1 - De Novo DNA Assembly

Main task: build and evaluate a short-read assembly workflow.

- simulate paired-end reads from a reference sequence,
- assemble reads into contigs,
- assess assembly quality (e.g. N50, genome fraction, misassemblies, mismatches/indels),
- implement and test a custom GC-content script.

### Lab 2 - DNA Annotation

Main task: annotate a selected genomic scaffold and interpret annotation signals.

- select scaffold assigned to the student index,
- run repeat masking and summarize masked sequence statistics,
- inspect Maker GFF annotations and count selected feature types,
- perform functional context checks (including sequence search),
- implement and test amino-acid to RNA conversion.

### Lab 3 - Human Resequencing

Main task: process resequencing reads and interpret variant calls in gene context.

- map reads to reference genome and process alignments,
- call and filter variants,
- annotate functional consequences of detected variants,
- focus interpretation on the IQGAP3 region,
- implement and test variant counting per gene using VCF + refFlat.

### Lab 4 - CNV Analysis (CODEX + DGV)

Main task: analyze copy-number changes and annotate them with structural-variant databases.

- inspect coverage patterns across exonic targets,
- summarize CODEX CNV calls (total events, deletions, duplications, copy number states),
- implement CNV overlap annotation against DGV entries,
- report overlap-based evidence for deletion/duplication support,
- document reproducible outputs and interpretation in a final report.

## Repository Contents

- `lab1/` - complete Lab 1 materials:
  - GC-content script (`lab1/scripts/gc_content.py`)
  - script test (`lab1/tests/test_gc_content.py`)
  - working report (`lab1/sprawozdanie_lab1_draft.md`)
  - QUAST outputs (`lab1/output/quast_results/`)

- `lab2/` - complete Lab 2 materials (DNA annotation):
  - scaffold selection, masking, and GFF stats scripts
  - amino acid to RNA conversion task with tests
  - completed lab report (`lab2/sprawozdanie_lab2_draft.md`)
  - selected lightweight outputs (GFF, BLAST query/results, summaries)

- `lab3/` - complete Lab 3 materials (human resequencing):
  - mapping + variant calling outputs (BAM/VCF and summaries)
  - variant annotation summary for IQGAP3 region
  - implementation task script: variants-per-gene from refFlat + VCF
  - completed lab report (`lab3/sprawozdanie_lab3_draft.md`)

- `lab4/` - complete Lab 4 materials (CNV analysis with CODEX and DGV annotation):
  - coverage median statistics for chromosome 20 samples
  - CODEX CNV summary (total calls, deletions, duplications, copy number 0 checks)
  - implementation task script: CNV annotation against DGV overlaps
  - completed lab report (`lab4/sprawozdanie_lab4_draft.md`)

## Quick Start

Detailed run instructions and parameters are available in:

- `lab1/README.md`
- `lab2/README.md`
- `lab3/README.md`
- `lab4/README.md`

## Notes

The repository stores lightweight artifacts (source code and text reports). Large generated data files are intentionally excluded via `.gitignore`.


