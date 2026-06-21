# Reference Reporting Summaries

This folder contains downloaded reference materials from nearby Gore-lab Nature Ecology & Evolution papers, plus text conversions for quick inspection.

Use these as reference examples only. They should not replace the manuscript-specific answers in `../REPORTING_SUMMARY_COPYPASTE_DRAFT.md`.

Verification status: checked against the rendered PDF pages on 2026-06-16. The cleaned summaries below are consistent with the PDFs. The Hu 2025 `.txt` file is raw OCR and still contains visual/OCR artifacts; use the cleaned sections below or the PDF for authoritative reading.

## Files

- `Hu2025_NatEcoEvo_reporting_summary.pdf`
  - Nature Portfolio Reporting Summary for Hu, Barbier, Bunin & Gore, 2025.
  - DOI: `10.1038/s41559-024-02618-y`
  - Source PDF: `https://static-content.springer.com/esm/art%3A10.1038%2Fs41559-024-02618-y/MediaObjects/41559_2024_2618_MOESM2_ESM.pdf`
- `Hu2025_NatEcoEvo_reporting_summary_ocr.txt`
  - OCR conversion. The PDF is image-based, so ordinary PDF text extraction returns almost no text.
- `Ratzke2020_NatEcoEvo_reporting_summary.pdf`
  - Nature Research Reporting Summary for Ratzke, Barrere & Gore, 2020.
  - DOI: `10.1038/s41559-020-1099-4`
  - Source PDF: `https://static-content.springer.com/esm/art%3A10.1038%2Fs41559-020-1099-4/MediaObjects/41559_2020_1099_MOESM2_ESM.pdf`
- `Ratzke2020_NatEcoEvo_reporting_summary.txt`
  - Direct `pdftotext` conversion.
- `Friedman2017_NatEcoEvo_supplementary_information_no_reporting_summary_found.pdf`
  - Supplementary Information for Friedman, Higgins & Gore, 2017.
  - DOI: `10.1038/s41559-017-0109`
  - Nature did not expose a separate Reporting Summary link on the article page.
- `Friedman2017_NatEcoEvo_supplementary_information.txt`
  - Direct `pdftotext` conversion of the Supplementary Information.

## High-Level Takeaways

- Both available Nature Reporting Summary examples selected **Life sciences**, not **Ecological, evolutionary & environmental sciences**.
- Both examples use the Life sciences study design fields: sample size, data exclusions, replication, randomization and blinding.
- The 2025 Hu example says no data were excluded.
- The 2020 Ratzke example reports one contaminated co-culture exclusion and failed sequencing reactions.
- The 2017 Friedman paper appears to have Supplementary Information only, not a separate Reporting Summary file on Nature's page.

## Hu 2025 Example

Paper:

Hu, Jiliang; Barbier, Matthieu; Bunin, Guy; Gore, Jeff. "Collective dynamical regimes predict invasion success and impacts in microbial communities." Nature Ecology & Evolution, 2025.

Metadata:

- Corresponding author: Jeff Gore.
- Last updated by author: October 24, 2024.
- Field-specific reporting selection: Life sciences.
- Human participants section: present in the newer form, but the PDF shows only the form's template text in those fields.

Software and code:

- Simulations were run in MATLAB 2024.
- Amplicon processing used DADA2 in R to infer ASVs.
- Taxonomy assignment used SILVA v132.

Data availability:

- Data are stated to be available in the supplementary materials.
- Raw sequencing data are deposited in Dryad: `10.5061/dryad.8gtht76xz`.

Life sciences study design fields:

```text
Sample size
The example justifies sample size using prior literature and feasibility. It reports 17 synthetic microbial communities per condition, built from an 80-isolate library, with 7-9 invasion tests per community.

Data exclusions
No data were excluded.

Replication
All replication attempts were successful.

Randomization
Samples and isolates were randomly assigned to experimental groups. Invader species were randomly chosen for each invasion test.

Blinding
Blinding was treated as not relevant because resident species and invaders were randomly chosen for each experiment.
```

Materials, systems and methods:

- Antibodies: n/a.
- Eukaryotic cell lines: n/a.
- Palaeontology and archaeology: n/a.
- Animals and other organisms: n/a.
- Clinical data: n/a.
- Dual use research of concern: n/a.
- Plants: n/a.
- ChIP-seq: n/a.
- Flow cytometry: n/a.
- MRI-based neuroimaging: n/a.

Notes for our draft:

- This is the closest precedent to our current coalescence manuscript because it is another Jiliang/Jeff bacterial microcosm paper.
- It chose Life sciences despite being in Nature Ecology & Evolution.
- It gives a useful precedent for treating blinding as not relevant when species assignments and invaders are randomized.
- It does not support saying ecological track is required; it supports either Life sciences or whichever track the portal requests.

## Ratzke 2020 Example

Paper:

Ratzke, Christoph; Barrere, Julien; Gore, Jeff. "Strength of species interactions determines biodiversity and stability in microbial communities." Nature Ecology & Evolution, 2020.

Metadata:

- Corresponding authors: Christoph Ratzke and Jeff Gore.
- Last updated by authors: November 5, 2019.
- Field-specific reporting selection: Life sciences.

Software and code:

- 16S amplicon sequencing data were processed with DADA2 in R.
- Analysis used Python 3 with SciPy and NumPy.
- Plotting used matplotlib.
- Simulations used SciPy `odeint`.

Data availability:

- The Reporting Summary says sequencing raw data would be made accessible in a repository after publication.
- Outside the Reporting Summary PDF, the article page now points to Dryad and a GitHub code repository.

Life sciences study design fields:

```text
Sample size
The example justifies sample size with pilot/test runs and expected large effects. It used all combinations of 8 species for pairwise competition and 3 sampling sites with 3 technical replicates for complex communities.

Data exclusions
One high-nutrient/high-buffer co-culture was removed because of cross-contamination. Some failed 16S sequencing reactions were excluded and shown in the supplementary figures.

Replication
Pairwise interaction experiments were repeated at least twice successfully. Complex-community experiments were also tested without sequencing using OD, pH and agar plating, and the reported sequencing design used 3 sites with 3 technical replicates each.

Randomization
The same species and soil samples were used while environmental growth conditions were varied.

Blinding
Pairwise interaction experiments were not blinded. Complex-community sequencing and analysis were done by a different person from the experimenter, so those experiments were treated as blinded.
```

Materials, systems and methods:

- Antibodies: n/a.
- Eukaryotic cell lines: n/a.
- Palaeontology: n/a.
- Animals and other organisms: n/a.
- Human research participants: n/a.
- Clinical data: n/a.
- ChIP-seq: n/a.
- Flow cytometry: n/a.
- MRI-based neuroimaging: n/a.

Notes for our draft:

- This is a strong precedent for explicitly reporting known exclusions, including contamination and failed sequencing.
- It also gives a useful model for partial blinding: not blinded for colony-count experiments, but blinded for sequencing/analysis when different people handled experiment and analysis.

## Friedman 2017 Example

Paper:

Friedman, Jonathan; Higgins, Logan M.; Gore, Jeff. "Community structure follows simple assembly rules in microbial microcosms." Nature Ecology & Evolution, 2017.

What is available:

- Nature's page lists only Supplementary Information under the supplementary information section.
- I did not find a separate Reporting Summary link on the Nature page.
- The downloaded Supplementary Information includes supplementary figures 1-8 and supplementary tables 1-3.

Notes for our draft:

- This paper is useful scientifically as a Gore-lab precedent for bottom-up prediction in microbial microcosms.
- It is not currently useful as a Reporting Summary template because the Nature page does not provide a separate Reporting Summary file.

## Practical Comparison for Our Form

Field-specific reporting:

- Our current draft recommends Ecological, evolutionary & environmental sciences.
- The two available Nature examples from this lab both used Life sciences.
- If the portal lets us choose freely, Life sciences has direct precedent from these papers.
- If the editor/portal asks for ecological reporting, keep the ecological track answers in the working draft.

Data exclusions:

- Hu 2025 precedent: "none excluded" is acceptable if true.
- Ratzke 2020 precedent: known contamination and failed sequencing exclusions should be stated explicitly.
- Our draft should keep `VERIFY` markers until we confirm whether any samples were removed because of contamination, failed sequencing, low read depth or quality-control thresholds.

Randomization:

- Hu 2025 precedent: random allocation of isolates/communities and invaders.
- Ratzke 2020 precedent: same source species/samples while environmental conditions vary.
- Our draft should say exactly what was randomized: community pairings, plate positions, parent-community labels, media assignments or invader/species selection, as applicable.

Blinding:

- Hu 2025 precedent: not relevant when assignments are random and species identities define the experimental design.
- Ratzke 2020 precedent: not blinded for colony morphology counting, partially blinded when sequencing and analysis were done by a different person.
- Our draft should avoid claiming blinding unless analysis/sample labels were actually masked.

Software:

- Both examples name core software and versions where relevant.
- Our draft should verify package versions for DADA2, QIIME/SILVA, Python/R/MATLAB, simulation and plotting libraries.

Data/code:

- Hu 2025 gives a strong precedent for Dryad raw sequencing data plus supplementary data.
- Ratzke 2020 gives a precedent for public sequencing data and GitHub simulation code after publication.
- Our draft should verify Dryad/SRA/GitHub accession or repository details before final submission.
