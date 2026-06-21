# PNAS Submission Guidelines and Conversion Plan

## Part 1: Summary of PNAS Submission Guidelines

### Article Type: Research Article (Direct Submission)
Based on the manuscript content, this should be submitted as a **Research Article** via Direct Submission.

**Classification**: Biological Sciences > Microbiology (or Ecology/Evolution)
- PNAS requires selecting a major category (Physical, Social, or Biological Sciences) and minor category
- Dual classifications are permitted between major categories

---

### Word Limits and Length

| Element | PNAS Requirement | Current Status |
|---------|------------------|----------------|
| **Total length** | Standard 6 pages (~4,000 words, 50 refs, 4 figures); max 12 pages | ~4,161 words main text - OK |
| **Abstract** | ≤250 words, single paragraph | ~150 words - OK |
| **Significance Statement** | **50-120 words (REQUIRED)** | **MISSING - MUST ADD** |
| **Keywords** | **3-5 keywords (REQUIRED)** | **MISSING - MUST ADD** |
| **References** | ~50 for 6-page article | Currently ~50 - OK |
| **Figures/Tables** | ~4 medium-size for 6-page; more allowed for longer | 5 main figures - OK |

**Key difference from Nature E&E**: PNAS is more flexible on word count (up to ~8,000 words for 12-page article) but **requires a Significance Statement and Keywords**.

---

### Required Sections (PNAS order)

| Section | Required? | Format/Notes |
|---------|-----------|--------------|
| **Title** | Yes | Concise, informative |
| **Authors & Affiliations** | Yes | Numbered affiliations; ORCID required for corresponding author |
| **Keywords** | **Yes** | 3-5 keywords, separated by pipe `\|` |
| **Abstract** | Yes | ≤250 words, single paragraph; references must be cited in full if included |
| **Significance Statement** | **Yes** | 50-120 words, NO citations, avoid numbers/measurements/acronyms, undergraduate-level accessibility |
| **Introduction** | Yes | **No explicit "Introduction" heading** (text starts directly); exception: math articles in Physical Sciences may use heading |
| **Results** | Yes | With subheadings |
| **Discussion** | Yes | With or without subheadings |
| **Materials and Methods** | Yes | Placed **AFTER Discussion** (methods-last format) |
| **Acknowledgments** | Yes | Brief; include funding sources |
| **Author Contributions** | Yes | Describe each author's role |
| **Competing Interest Statement** | Yes | Must disclose or state "none" |
| **Data Availability** | Yes | With repository accessions/DOIs; datasets must be cited in references |
| **References** | Yes | Numbered, sequential; include full article titles |

**Note on section order**: PNAS states "Many authors find it useful to organize their manuscripts with the following order of sections: introduction, results, discussion, materials and methods, acknowledgments, and references. Other orders and headings are permitted."

**Page numbering**: Number all manuscript pages starting with the title page as page 1.

---

### Reference Format

- **Citation style**: Numbered in parentheses, sequential order of appearance
- **In-text format**: `(1)`, `(1, 2)`, `(1–3)` (use en-dash for ranges)
- **Bibliography format**:
  ```
  1. Author AB, Author CD, Author EF (Year) Article title. Journal Abbrev Volume:Pages.
  ```
- **Article titles**: **REQUIRED** (include full title for each cited article)
- **Journal names**: Must use official abbreviations
- **BibTeX style**: `pnas-new` (use `\bibliographystyle{pnas-new}`)
- **Important**: For final submission, PNAS does not support separate .bbl files; references must be embedded in .tex file

**Example reference format**:
```
1. Rillig MC, et al. (2015) Interchange of entire communities: Microbial community coalescence. Trends Ecol Evol 30:470–476.
```

**Note**: Use "et al." when there are more than 5 authors. Use MEDLINE/PubMed abbreviations for journal titles; use full title for journals not indexed in MEDLINE.

---

### Figure Requirements

| Aspect | Requirement |
|--------|-------------|
| **Format** | TIFF, EPS, or high-resolution PDF **only** for main text figures |
| **Resolution - Line art** | 1000-1200 dpi |
| **Resolution - Halftones (photos)** | ≥300 dpi |
| **Resolution - Combination** | 600-900 dpi |
| **Color mode** | RGB (not CMYK) |
| **Font** | Arial, Helvetica, Times, Symbol (consistent across all figures) |
| **Font size** | ≥6 points after reduction |
| **TIFF compression** | LZW only (no JPEG compression) |
| **Width** | 8.7 cm (1 column), 11.4 cm or 17.8 cm (wider) |
| **Legends** | Include in manuscript after first reference to figure |

**Important**: Images must be final size. Color images must be in RGB mode.

---

### Supporting Information (SI Appendix)

| Aspect | Requirement |
|--------|-------------|
| **Format** | **Single combined PDF** (all text, figures, tables, legends) |
| **Maximum files** | 10 SI files (excluding movies) |
| **Numbering** | Fig. S1, Table S1 (not "Supplementary Figure S1") |
| **Main text reference** | "SI Appendix, Fig. S1" or "SI Appendix, Materials and Methods" |
| **References** | **Separate from main text**; number SI refs independently; do NOT cross-cite |
| **Figure placement** | Separate pages with legends below each figure |
| **Table placement** | Titles above tables |
| **Datasets** | XLSX, RTF, PDF, CSV, GZ, or TXT files |
| **Movies** | AVI, MOV, WMV, GIF, or MPEG; ≤10 MB each |

**Critical notes**:
- SI is published **as-is** (not copyedited) - must be provided in final form
- Main text must stand on its own without SI
- If methods are in SI, main text must have sufficient detail to follow logic

---

### Data and Code Availability

**Data Availability Statement** (REQUIRED):
- Must specify public repository
- Must include persistent identifiers (DOIs, accession numbers)
- Must be accessible upon publication
- **Research datasets must be cited in the references**

**Code/Software Availability**:
- Source code or scripts must be provided in native file types
- GitHub + Zenodo DOI recommended for archival

**Disclosure at submission**: Authors must provide data sharing plans at submission time.

---

### Competing Interests Disclosure

- Authors must disclose **at submission** any association that poses a financial or personal competing interest
- Must acknowledge **all funding sources**
- Disclosures must be entered directly into submission system (not just linked)
- Financial interests from past 48 months must be disclosed (including spouse/dependent children)
- PNAS policy is designed to **manage, not eliminate**, competing interests

---

## Part 2: Current Manuscript Analysis

### Current Structure (Nature E&E format)
```
main.tex
├── title_abstract.tex (title, authors, abstract)
├── introduction.tex (~743 words) - HAS "Introduction" heading
├── results.tex (~2,809 words) - 5 figures
├── discussion.tex (~609 words)
├── references.bib (naturemag style)
└── methods.tex (~2,151 words)
```

### Changes Needed for PNAS Format

| Current | PNAS Requirement | Action |
|---------|------------------|--------|
| No Significance Statement | **Required (50-120 words)** | **ADD** |
| No Keywords | **Required (3-5)** | **ADD** |
| Has "Introduction" heading | No heading allowed | **REMOVE** |
| `naturemag` bibliography style | `pnas` style | **CHANGE** |
| Superscript citations | Parenthetical numbers | **CHANGE natbib options** |
| No ORCID | Required for corresponding author | **ADD** |
| Author Contributions missing | Required | **ADD** |
| Data Availability missing | Required | **ADD** |
| Competing Interests missing | Required | **ADD** |
| Methods at end | Methods after Discussion | **OK (verify order)** |
| SI refs mixed with main | SI refs must be separate | **SEPARATE** |

---

## Part 3: Detailed Conversion Plan

### Phase 1: Document Structure Changes

#### Step 1.1: Update main.tex preamble

**Current**:
```latex
\documentclass[11pt,a4paper]{article}
\usepackage[numbers,super,sort&compress]{natbib}
```

**Change to**:
```latex
\documentclass[11pt,a4paper]{article}
\usepackage[numbers,sort&compress]{natbib}  % Remove 'super' for parenthetical citations
```

**Note**: PNAS is format-neutral at initial submission. Use official PNAS template for revision if accepted.

#### Step 1.2: Add Keywords (after abstract)
```latex
\textbf{Keywords:} community coalescence | microbial ecology | interspecies interactions | community-level selection | Lotka-Volterra model
```

#### Step 1.3: Add Significance Statement (after keywords, before main text)
```latex
\section*{Significance}
Understanding when ecological communities behave as cohesive units versus loose species assemblages is fundamental to ecology. We demonstrate that interspecies interaction strength determines whether community-level selection occurs during coalescence—the mixing of previously isolated communities. Weak interactions produce species mixtures; strong interactions cause one community to dominate. Experiments manipulating nutrient concentration confirm these predictions. Our findings reconcile conflicting observations from prior studies and provide a predictive framework for microbial community outcomes relevant to microbiome engineering, fecal transplantation, and ecosystem management.
```
(~90 words - within 50-120 limit, no citations)

#### Step 1.4: Remove explicit "Introduction" heading

**Current** (introduction.tex):
```latex
\section{Introduction}
\label{sec:introduction}

In nature, species coexist...
```

**Change to**:
```latex
% Introduction (no heading per PNAS style)
\label{sec:introduction}

In nature, species coexist...
```

#### Step 1.5: Change bibliography style

**Current**:
```latex
\bibliographystyle{naturemag}
```

**Change to**:
```latex
\bibliographystyle{pnas-new}
```

**Note**: Use `pnas-new.bst` (current PNAS bibliography style) from the official PNAS LaTeX template. Download from PNAS Overleaf template or CTAN.

#### Step 1.6: Add ORCID for corresponding author
```latex
\author[1,*]{Jinyeop Song}
% In footnote or after affiliations:
*Corresponding author. Email: xxx@mit.edu. ORCID: 0000-0000-0000-0000
```

---

### Phase 2: Add Required Sections

#### Step 2.1: Add Author Contributions (after Acknowledgments)
```latex
\section*{Author Contributions}
J.S. designed research, performed research, analyzed data, and wrote the paper. J.H. contributed to experimental design and data analysis. J.G. designed research, supervised the project, and edited the paper.
```

#### Step 2.2: Add Competing Interest Statement
```latex
\section*{Competing Interest Statement}
The authors declare no competing interest.
```

#### Step 2.3: Add Data Availability (with dataset citation)
```latex
\section*{Data Availability}
Raw 16S rRNA amplicon sequencing data have been deposited in the NCBI Sequence Read Archive under BioProject accession PRJNA[XXXXXX] (XX). Processed community composition data and simulation results are available at Zenodo (DOI: 10.5281/zenodo.[XXXXXX]) (XX). All data needed to evaluate the conclusions are present in the paper and/or the SI Appendix.
```

**Important**: The datasets must also be cited in the References section:
```bibtex
@misc{Song2025data,
  author = {Song, Jinyeop and Hu, Jiliang and Gore, Jeff},
  title = {Data for: Interspecies Interactions Drive Community-Level Selection in Microbial Coalescence},
  year = {2025},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.XXXXXXX}
}
```

#### Step 2.4: Update Acknowledgments (include funding)
```latex
\section*{Acknowledgments}
We thank [names] for helpful discussions. This work was supported by [funding agency] grant [number] (to J.G.), [fellowship] (to J.S.), and [other funding].
```

---

### Phase 3: Reference Format Changes

#### Step 3.1: Update references.bib
Key requirements:
- Include full article titles (PNAS requires titles)
- Use journal abbreviations
- Include DOIs where available
- Format: Author AB, Author CD (Year) Title. Journal Vol:Pages.

#### Step 3.2: Citation format in text
**PNAS style** (parenthetical, not superscript):
```latex
Previous work showed this effect (1).
Multiple studies support this (1, 2, 15).
Studies (1–5) demonstrated...  % use en-dash for ranges
As shown by Smith et al. (3)...
```

#### Step 3.3: For final submission, embed references
PNAS does not accept separate .bbl files. Copy compiled bibliography into .tex:
```latex
\begin{thebibliography}{50}
\bibitem{Rillig2015}
Rillig MC, et al. (2015) Interchange of entire communities: Microbial community coalescence. \textit{Trends Ecol Evol} 30:470–476.
% ... continue for all references
\end{thebibliography}
```

---

### Phase 4: Supporting Information Conversion

#### Step 4.1: Create SI Appendix as single PDF
Combine all supplementary materials:
1. SI Text (supplementary methods)
2. SI Figures (Fig. S1–S31)
3. SI Tables (Table S1–S5)
4. SI References (separate from main text)

#### Step 4.2: Update SI numbering format
- Use "Fig. S1" (not "Supplementary Figure S1" or "Figure S1")
- Use "Table S1" (not "Supplementary Table S1")
- Main text references: "SI Appendix, Fig. S1" or "(SI Appendix, Fig. S1)"

#### Step 4.3: Separate SI references
- Create independent reference list for SI Appendix
- Number SI references starting from 1
- Do NOT cite main-text references in SI or vice versa
- If same source needed in both, list it in both reference lists

#### Step 4.4: SI figure format
- Each figure on separate page
- Legend immediately below figure on same page
- Resolution requirements same as main figures

---

### Phase 5: Submission System Requirements

#### Step 5.1: Required information at submission
- Title, authors, affiliations
- Classification (major + minor category)
- Keywords (3-5)
- Abstract
- Significance Statement
- Data sharing plans
- Funding information
- Competing interest disclosures for ALL authors
- ORCID for corresponding author
- Suggested reviewers (minimum 3 qualified experts)
- Suggested Editorial Board members (minimum 3)

#### Step 5.2: File uploads
1. Main manuscript (PDF + source files)
2. Figures (separate high-res files: TIFF, EPS, or PDF)
3. SI Appendix (single PDF)
4. Cover letter
5. Dataset files (if separate from SI)

---

## Part 4: Section-by-Section Checklist

### Title Page
- [ ] Title: concise, informative
- [ ] Authors: full names with affiliation superscripts
- [ ] Affiliations: numbered, with full addresses
- [ ] Corresponding author: email and **ORCID** (required)
- [ ] Keywords: 3-5, **pipe-separated** (`|`)

### Abstract
- [ ] ≤250 words (currently ~150 - OK)
- [ ] Single paragraph
- [ ] References cited in full if included (or avoid refs)
- [ ] Explains major contributions to general reader

### Significance Statement
- [ ] **CREATE NEW** (50-120 words)
- [ ] **NO citations/references allowed**
- [ ] **Avoid numbers, measurements, and acronyms** unless necessary
- [ ] Understandable to undergraduate-level scientist outside field
- [ ] Explains broader impact and significance

### Main Text - Introduction
- [ ] **Remove "Introduction" heading**
- [ ] Text starts directly after Significance
- [ ] Citation format: parenthetical (1), not superscript
- [ ] Check all refs numbered sequentially

### Results
- [ ] Subheadings for each subsection
- [ ] Figures referenced in order (Fig. 1, Fig. 2...)
- [ ] Statistics reported properly
- [ ] SI references: "SI Appendix, Fig. S1"

### Discussion
- [ ] Can have subheadings
- [ ] Concise conclusions
- [ ] No new results

### Materials and Methods
- [ ] Placed **after Discussion** (methods-last)
- [ ] Sufficient detail for reproducibility
- [ ] Reference SI for extended methods
- [ ] Subheadings for organization
- [ ] **AI Disclosure**: If AI/LLM used (e.g., ChatGPT, Claude), must disclose in Materials and Methods with specific model/version

### Acknowledgments
- [ ] Brief
- [ ] **Funding sources with grant numbers** (required)
- [ ] Thank specific individuals by name
- [ ] Spell out ALL abbreviations
- [ ] Dedications rarely allowed
- [ ] No anonymous reviewer thanks

### Author Contributions
- [ ] **CREATE NEW**
- [ ] Describe each author's specific contributions
- [ ] Use initials (J.S., J.H., J.G.)

### Competing Interest Statement
- [ ] **CREATE NEW**
- [ ] "The authors declare no competing interest." or disclose specifics

### Data Availability
- [ ] **CREATE NEW**
- [ ] Repository name (NCBI SRA, Zenodo, etc.)
- [ ] Accession numbers/DOIs
- [ ] **Cite datasets in References**

### References
- [ ] Change to `pnas-new` bibliography style
- [ ] Numbered sequentially in order of appearance
- [ ] Parenthetical citations: (1), (1, 2), (1–5)
- [ ] Journal abbreviations
- [ ] **Full article titles included**
- [ ] DOIs included where available
- [ ] Dataset citations included

### Figures
- [ ] Format: TIFF, EPS, or high-res PDF only
- [ ] Resolution: ≥300 dpi (photos), ≥1000 dpi (line art)
- [ ] Consistent fonts (Arial/Helvetica)
- [ ] ≥6 pt text after reduction
- [ ] RGB color mode
- [ ] Legends in manuscript text

### SI Appendix
- [ ] Single combined PDF
- [ ] "Fig. S1", "Table S1" format
- [ ] Figures on separate pages with legends below
- [ ] **Separate reference list from main text**
- [ ] All elements numbered S1, S2...

---

## Part 5: File Deliverables for Submission

### Required Files
1. **Main manuscript** (PDF + .tex source)
   - All text, figure legends, embedded references
2. **Figures** (separate high-res files)
   - TIFF, EPS, or PDF format
   - One file per figure
   - Final size, ≥300 dpi
3. **SI Appendix** (single PDF)
   - All supplementary text, figures, tables, SI references
4. **Cover letter** (separate file)

### Information Required in Submission System
- Data sharing plans (all data, documentation, code)
- Funding information
- Open access license selection (if applicable)
- Competing interests for ALL authors
- Suggested reviewers (≥3)
- Suggested Editorial Board members (≥3)

### Optional Files
- Dataset files (Excel, CSV) - if not in SI
- Movie files (≤10 MB each)

---

## Part 6: Comparison: PNAS vs Nature E&E

| Feature | PNAS | Nature E&E |
|---------|------|------------|
| Word limit | ~4,000-8,000 (flexible) | 3,500 strict |
| Abstract | ≤250 words | ≤200 words |
| **Significance Statement** | **Required (50-120 words)** | Not required |
| **Keywords** | **Required (3-5)** | Not required |
| Introduction heading | **No heading** | **HAS heading** (Nature E&E uses section headings) |
| Methods position | After Discussion | After References |
| Extended Data | Not available | Up to 10 items |
| SI files limit | 10 files max | No strict limit |
| SI references | **Must be separate** | Can share with main |
| Citation style | Parenthetical (1, 2) | Superscript^1,2 |
| Figure limit | Flexible (~4-8) | 6 max strict |
| ORCID | **Required** (corresponding) | Recommended |
| Dataset citation | **Required in refs** | Recommended |
| AI disclosure | **Required** in Methods | Required |

---

## Part 7: Priority Action Items

### HIGH PRIORITY (Required for submission)
1. [ ] **Add Significance Statement** (50-120 words, no citations)
2. [ ] **Add Keywords** (3-5 terms, pipe-separated)
3. [ ] **Remove "Introduction" heading** from introduction.tex
4. [ ] **Change bibliography style** to `pnas-new`
5. [ ] **Change citation format** from superscript to parenthetical
6. [ ] **Add Author Contributions**
7. [ ] **Add Competing Interest Statement**
8. [ ] **Add Data Availability** with repository info
9. [ ] **Add ORCID** for corresponding author

### MEDIUM PRIORITY (Before submission)
10. [ ] Verify all references have full article titles
11. [ ] Update SI references to "Fig. S1" format
12. [ ] Create separate SI reference list
13. [ ] Compile SI Appendix as single PDF
14. [ ] Verify figure resolution meets requirements
15. [ ] Prepare suggested reviewers list (≥3)

### DATA/CODE TASKS
16. [ ] Deposit raw sequencing data to NCBI SRA
17. [ ] Deposit processed data to Zenodo
18. [ ] Archive code on Zenodo (with DOI)
19. [ ] Add dataset citations to references.bib
20. [ ] Get all accession numbers/DOIs

---

## Part 8: Proposed Document Order (PNAS Format)

```latex
\documentclass[11pt,a4paper]{article}
\usepackage[numbers,sort&compress]{natbib}  % parenthetical citations
% ... other packages ...

\begin{document}

% 1. Title
\title{Interspecies Interactions Drive Community-Level Selection in Microbial Coalescence}

% 2. Authors and Affiliations (with ORCID for corresponding author)
\author[1,*]{Jinyeop Song}
\author[1]{Jiliang Hu}
\author[1]{Jeff Gore}
\affil[1]{Department of Physics, Massachusetts Institute of Technology, Cambridge, MA, USA}
% *Corresponding author. Email: xxx@mit.edu. ORCID: 0000-0000-0000-0000

\maketitle

% 3. Abstract
\begin{abstract}
Whether communities behave as cohesive units or loose collections...
\end{abstract}

% 4. Keywords
\textbf{Keywords:} community coalescence | microbial ecology | interspecies interactions | community-level selection | Lotka-Volterra model

% 5. Significance Statement
\section*{Significance}
Understanding when ecological communities behave as cohesive units...

% 6. Main Text (NO Introduction heading)
In nature, species coexist and interact within complex communities...

% 7. Results
\section*{Results}
\subsection*{Community-level selection is prevalent in microbial coalescence}
...

% 8. Discussion
\section*{Discussion}
...

% 9. Materials and Methods
\section*{Materials and Methods}
\subsection*{Microbial Strain Library...}
...

% 10. Acknowledgments (with funding)
\section*{Acknowledgments}
We thank... This work was supported by...

% 11. Author Contributions
\section*{Author Contributions}
J.S. designed research...

% 12. Competing Interests
\section*{Competing Interest Statement}
The authors declare no competing interest.

% 13. Data Availability
\section*{Data Availability}
Raw sequencing data... (XX). Processed data... (XX).

% 14. References (including dataset citations)
\bibliographystyle{pnas-new}
\bibliography{references}

\end{document}
```

---

## Part 9: Example Text for New Sections

### Significance Statement (Draft)
```
Understanding when ecological communities behave as cohesive units versus
loose species assemblages is a fundamental question in ecology. We
demonstrate that interspecies interaction strength determines whether
community-level selection occurs during coalescence—the mixing of
previously isolated communities. Weak interactions produce symmetric
mixtures where both communities persist; strong interactions cause one
community to dominate. Experiments manipulating nutrient concentration
confirm these predictions and reveal two distinct mechanistic regimes.
Our findings reconcile conflicting observations from prior studies and
provide a predictive framework for microbial community mixing outcomes,
with implications for microbiome engineering, fecal transplantation,
and ecosystem management.
```
(~105 words)

### Keywords
```
community coalescence | microbial ecology | interspecies interactions |
community-level selection | Lotka-Volterra model
```

### Author Contributions (Draft)
```
J.S. conceived the study, designed and performed experiments, developed
the theoretical model, analyzed data, created figures, and wrote the
manuscript. J.H. contributed to experimental design, data analysis, and
manuscript editing. J.G. supervised the research, contributed to study
design and interpretation, and edited the manuscript.
```

### Competing Interest Statement
```
The authors declare no competing interest.
```

### Data Availability (Template)
```
Raw 16S rRNA amplicon sequencing data have been deposited in the NCBI
Sequence Read Archive (SRA) under BioProject accession PRJNA[XXXXXX]
(ref. XX). Processed community composition data, coalescence outcome
classifications, and simulation results are available at Zenodo with
DOI: 10.5281/zenodo.[XXXXXX] (ref. XX). Custom analysis code is
available at GitHub (https://github.com/[username]/coalescence-analysis)
and archived on Zenodo with DOI: 10.5281/zenodo.[XXXXXX] (ref. XX).
```

---

## Sources

- [PNAS Submission Guidelines](https://www.pnas.org/author-center/submitting-your-manuscript)
- [PNAS Author Center](https://www.pnas.org/author-center)
- [PNAS Editorial Policies](https://www.pnas.org/author-center/editorial-and-journal-policies)
- [PNAS LaTeX Template (Overleaf 2025)](https://www.overleaf.com/latex/templates/template-for-preparing-your-research-report-submission-to-pnas-using-overleaf-2023/whbdryzwztnd)
- [PNAS SI Template (Overleaf)](https://www.overleaf.com/latex/templates/pnas-template-for-supplementary-information/wqfsfqwyjtsd)
- [PNAS Citation Style - Paperpile](https://paperpile.com/s/proceedings-of-the-national-academy-of-sciences-of-the-united-states-of-america-citation-style/)
- [BibTeX PNAS Style](https://www.bibtex.com/s/bibliography-style-misc-pnas/)
- [PNAS Digital Art Guidelines](https://www.pnas.org/pb-assets/authors/digitalart-1675347574760.pdf)
