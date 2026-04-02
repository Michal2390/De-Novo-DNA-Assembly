# 🧬 MBI Bioinformatics Labs

> Academic bioinformatics coursework spanning MBI Labs 1–4: de novo assembly, DNA annotation, human resequencing, and CNV analysis with CODEX and DGV-supported interpretation.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![R](https://img.shields.io/badge/R-CODEX-276DC3?logo=r&logoColor=white)
![License](https://img.shields.io/badge/license-academic-lightgrey)
![Labs](https://img.shields.io/badge/labs-1--4-success)

---

## 📌 What This Project Is

This repository covers the full MBI laboratory path (Lab 1 to Lab 4). It combines practical workflows, small implementation tasks in Python, and written reports for each exercise.

At a high level, the project includes:

| # | Topic | Key Output |
|---|-------|-----------|
| 1 | 🔬 De Novo Assembly | Contigs, QUAST report, GC-content script |
| 2 | 🧩 DNA Annotation | Masked scaffold, Maker GFF, AA→RNA script |
| 3 | 🧪 Human Resequencing | BAM/VCF, VEP annotation, variants-per-gene |
| 4 | 📊 CNV Analysis | CODEX summary, DGV overlap annotation |

---

## 🎯 Why This Project Exists

The goal is to practice end-to-end bioinformatics analysis across multiple related topics and to document both tooling and interpretation. Each lab adds a different skill layer:

- 🛠️ data preparation and command-line genomics workflows,
- 🔍 quality control and biological interpretation of outputs,
- 💻 implementation of task-specific scripts (with tests),
- 📝 reproducible reporting of methods and results.

---

## 🔬 Lab Objectives

### 🧬 Lab 1 — De Novo DNA Assembly

> **Main task:** build and evaluate a short-read assembly workflow.

- simulate paired-end reads from a reference sequence,
- assemble reads into contigs,
- assess assembly quality (N50, genome fraction, misassemblies, mismatches/indels),
- implement and test a custom GC-content script.

---

### 🧩 Lab 2 — DNA Annotation

> **Main task:** annotate a selected genomic scaffold and interpret annotation signals.

- select scaffold assigned to the student index,
- run repeat masking and summarize masked sequence statistics,
- inspect Maker GFF annotations and count selected feature types,
- perform functional context checks (including sequence search),
- implement and test amino-acid to RNA conversion.

---

### 🧪 Lab 3 — Human Resequencing

> **Main task:** process resequencing reads and interpret variant calls in gene context.

- map reads to reference genome and process alignments,
- call and filter variants,
- annotate functional consequences of detected variants,
- focus interpretation on the IQGAP3 region,
- implement and test variant counting per gene using VCF + refFlat.

---

### 📊 Lab 4 — CNV Analysis (CODEX + DGV)

> **Main task:** analyze copy-number changes and annotate them with structural-variant databases.

- inspect coverage patterns across exonic targets,
- summarize CODEX CNV calls (total events, deletions, duplications, copy number states),
- implement CNV overlap annotation against DGV entries,
- report overlap-based evidence for deletion/duplication support,
- document reproducible outputs and interpretation in a final report.

---

## 📁 Repository Contents

```
MBI/
├── lab1/   🔬 De Novo Assembly
│   ├── scripts/gc_content.py
│   ├── tests/test_gc_content.py
│   ├── output/quast_results/
│   └── sprawozdanie_lab1_draft.md
├── lab2/   🧩 DNA Annotation
│   ├── scripts/  (select_scaffold, masked_stats, gff_stats, aa_to_rna)
│   ├── tests/
│   ├── output/   (GFF, BLAST query/results, summaries)
│   └── sprawozdanie_lab2_draft.md
├── lab3/   🧪 Human Resequencing
│   ├── scripts/count_variants_per_gene.py
│   ├── tests/
│   ├── output/   (BAM, VCF, VEP annotation, variants-per-gene)
│   └── sprawozdanie_lab3_draft.md
└── lab4/   📊 CNV Analysis
    ├── scripts/  (coverage_stats, codex_summary, cnv_dgv_annotation)
    ├── tests/
    ├── output/   (coverage medians, CODEX summary, DGV annotation)
    └── sprawozdanie_lab4_draft.md
```

---

## 🚀 Quick Start

Detailed run instructions and parameters are available in each lab subfolder:

| Lab | README |
|-----|--------|
| 🔬 Lab 1 | [`lab1/README.md`](lab1/README.md) |
| 🧩 Lab 2 | [`lab2/README.md`](lab2/README.md) |
| 🧪 Lab 3 | [`lab3/README.md`](lab3/README.md) |
| 📊 Lab 4 | [`lab4/README.md`](lab4/README.md) |

---

## 📎 Notes

> The repository stores lightweight artifacts (source code and text reports).  
> Large generated data files are intentionally excluded via `.gitignore`.
