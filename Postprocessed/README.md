# Interspecies interactions drive community-level selection in microbial coalescence

Dataset DOI: [10.5061/dryad.2z34tmq0z](https://doi.org/10.5061/dryad.2z34tmq0z)

## Description of the data and file structure

Data from: Interspecies Interactions Drive Community-Level Selection in Microbial Coalescence

### Files and variables

* **`coalescence_data.zip`** — 1.93 GB (primary data archive containing raw FASTQ files)
* **`Sample_Sheet.xlsx`** — consolidated sample sheet (Metadata for data in **`coalescence_data.zip`** )
* **`README.md`** — 2.02 KB (original Dryad README)

---

## What’s inside `coalescence_data.zip`

The archive contains:

* **Raw sequencing data in FASTQ format** (paired-end Illumina reads, one pair of files per sample).

### FASTQ naming convention

FASTQ files follow the pattern:

`<SampleID>_L<lane number>_R<read direction>_001.fastq.gz`

Where:

* `SampleID` = unique sample identifier — matches the `sample_id` column in the sample sheet (e.g. `P1-25`)
* `L` = lane number (e.g., `L001`)
* `R1` = forward read, `R2` = reverse read
* `001` = file part index (often `001`)

Example: `P1-25_L001_R1_001.fastq.gz` and `P1-25_L001_R2_001.fastq.gz`

---
## Sample sheet (`Sample_Sheet.xlsx`)

A three-sheet Excel workbook provided as a top-level file alongside `coalescence_data.zip`. Contains per-sample metadata, coalescence pairings, and ASV taxonomy. The `sample_id` column is the primary key linking this file to the FASTQ filename prefixes inside `coalescence_data.zip`.

### Sheet 1: `samples` — 588 rows, one per sequenced community

Per-sample metadata for all sequenced communities, including experimental design, coalescence parentage, and endpoint phenotypic measurements.

* `sample_id` = unique sample identifier (e.g., `P1-25`); matches the FASTQ filename prefix
* `community_origin` = `Synthetic` (12-species defined pool) or `Natural` (environmental community)
* `medium` = nitrogen level: `Nutr-` (low N), `Base` (medium N), or `Nutr+` (high N)
* `sample_type` = `Subcommunity` (single-ancestor) or `Coalescence` (mixture of two subcommunities)
* `replicate` = biological replicate index (1 or 2)
* `community_idx` = community number within its (origin, medium, sample_type, replicate) group
* `timepoint` = `Final` (endpoint of the assembly experiment; only timepoint included)
* `parent_1_community_idx`, `parent_2_community_idx` = for `Coalescence` rows only, the `community_idx` of the two parent subcommunities (resolved via `coalescence_recipe`); empty for `Subcommunity` rows
* `parent_1_sample_id`, `parent_2_sample_id` = for `Coalescence` rows only, the `sample_id` of the two parent subcommunities (same medium and replicate)
* `OD_final_mean`, `OD_final_std` = mean and standard deviation of seven OD600 endpoint readings (`fieldOD1`…`fieldOD7`)
* `pH_final_mean`, `pH_final_std` = mean and standard deviation of seven endpoint pH readings (`fieldPH1`…`fieldPH7`)
* `growth_curve_AUC_mean` = mean of three growth-curve area-under-curve measurements (`fieldGC1`…`fieldGC3`)
* `fieldOD1`…`fieldOD7` = raw endpoint OD600 readings (technical replicates)
* `fieldPH1`…`fieldPH7` = raw endpoint pH readings (technical replicates)
* `fieldGC1`…`fieldGC3` = raw growth-curve AUC measurements (technical replicates)
* `notes` = reason for data-quality flag (empty if none); possible values: `no reads in coalescence result`, `no file`, `MN E7 missing`, `MN24 CC, excess unwanted ASVs (likely mislabel)`, `ASV not in subcommunities at >0.3 abundance`. Flagged samples are excluded from downstream analyses in the accompanying paper.

### Sheet 2: `coalescence_recipe` — 62 rows

Mapping of coalescence events to their parent subcommunities. Each row defines one mixing event.

* `event_id` = sequential index across both origins (1–62)
* `community_origin` = `Synthetic` (47 events) or `Natural` (15 events)
* `coalescence_community_idx` = the `community_idx` of the resulting coalescence community
* `parent_1_community_idx`, `parent_2_community_idx` = the `community_idx` values of the two parent subcommunities that were mixed; resolved to specific `sample_id`s in the `samples` sheet via the (origin, medium, replicate, community_idx) tuple

### Sheet 3: `asv_taxonomy` — 167 rows (43 synthetic + 124 natural)

Taxonomic assignments and representative sequences for all ASVs detected across the two experiments.

* `community_origin` = `Synthetic` or `Natural`; indicates which experiment this ASV is part of
* `asv_id` = ASV label (e.g., `ASV1`); numbering is independent between origins (synthetic ASV1 ≠ natural ASV1)
* `kingdom`, `phylum`, `class`, `order`, `family`, `genus` = taxonomic assignment from GreenGenes (16S rRNA gene)
* `unique_sequence` = representative 16S V4 amplicon nucleotide sequence for the ASV (~253 bp)

---

## Access information

The files will be available for public download after the dataset has been approved and published by Dryad.
