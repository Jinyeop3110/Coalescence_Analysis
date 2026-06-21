# Nature Ecology & Evolution Submission Guidelines and Conversion Plan

## Part 1: Summary of Nature Ecology & Evolution Submission Guidelines

### Article Type: Research Article
Based on the manuscript content, this should be submitted as an **Article** (substantial novel research study).

### Word Limits
| Section | Limit | Current Status |
|---------|-------|----------------|
| Main text (intro + results + discussion) | **3,500 words** (excluding abstract, Methods, references, figure legends) | ~4,161 words (LaTeX count, includes formatting) - **NEEDS REDUCTION** |
| Abstract | **200 words**, unreferenced | Current abstract: ~150 words - OK |
| Methods | No strict limit (appears online) | ~2,151 words - OK |
| Figure legends | **<300 words each**; if Methods section present, keep legends minimal (<100 words each, <500 total) | Need to check |

**Note**: Figure legends are EXCLUDED from the 3,500 word main text limit.

### Display Items
- **Maximum 6 figures/tables** in main text
- Current: 5 main figures (Fig 1-5) - **OK**
- **Extended Data**: Up to 10 items (figures/tables) - linked from main text in HTML version

### Reference Guidelines
- Typically **up to 50 references** recommended
- **Numbered citation style** (superscript numbers)
- **Article titles ARE required** for Articles
- Format: `Author1, A. B. & Author2, C. D. Article title. Journal Name Vol, pages (year).`
- Use `naturemag` bibliography style (already in use)

### Structure Requirements
| Element | Nature E&E Format |
|---------|------------------|
| Title | Concise, informative |
| Abstract | Up to 200 words, NO references, single paragraph |
| Main text | No section numbering; Results and Methods have topical subheadings; Discussion has NO subheadings |
| Methods | "Online Methods" - appears after figure legends (see Part 8 for full order); divided by subheadings |
| References | Numbered, sequential, superscript citations |

**Note on document order**: The formal Nature order is: Main text → References → Tables → Figure legends → Methods. However, for LaTeX submission, figures can be embedded in text or grouped at end. The key is that Methods appears AFTER the main narrative sections.

**IMPORTANT CLARIFICATION on Introduction**:
- Nature E&E Articles use section headings (Introduction, Results, Discussion)
- This differs from Nature main journal which uses a "bold first paragraph" without Introduction heading
- Current manuscript format with `\section{Introduction}` is CORRECT for Nature E&E

### Figure Requirements
- Cite as "Fig. 1", "Fig. 2" etc. (already correct)
- Minimum 300 dpi resolution
- Maximum width 180 mm
- Font: 5-7 pt sans serif for labels; Symbol font for Greek characters
- Use scale bars, not magnification factors
- Use verbal cues for keys (e.g., "open red triangles"), NOT visual symbols
- Error bars must be described in legends
- **Figure legends MUST include**:
  - Brief title
  - Description of center values (median or average)
  - Definition of ALL error bars and how calculated
  - EXACT sample size (n number) - not ranges
  - Statistical test used
  - P values
- Avoid methodological detail in legends (keep in Methods)

### Additional Required Sections
1. **Author Contributions** - specify each author's role
2. **Competing Interests** - declare or state "none"
3. **Data Availability Statement** - required, with repository links/DOIs
4. **Code Availability Statement** - required for computational work
5. **Acknowledgements** - brief, no anonymous referees/editors

### Supplementary Information Format
- Designate as: Supplementary Figure, Table, Video, Data, etc.
- Number sequentially (separate from main figures)
- Each Supplementary Figure fits on single PDF page with legend
- Submit as single combined PDF (or Excel for complex tables)

---

## Part 2: Current Manuscript Analysis

### Current Structure
```
main.tex
├── title_abstract.tex (title, authors, abstract)
├── introduction.tex (~743 words)
├── results.tex (~2,809 words) - includes 5 figures
├── discussion.tex (~609 words)
├── references.bib
└── methods.tex (~2,151 words)
```

### Issues to Address

#### 1. Word Count (HIGH PRIORITY)
- **Current main text**: ~4,161 words (intro + results + discussion)
- **Target**: 3,500 words
- **Need to cut**: ~661 words (16% reduction)

#### 2. Abstract Format (MINOR)
- Current: 150 words - within limit
- Check: Ensure no references in abstract (appears OK)

#### 3. Section Formatting (MODERATE)
- Discussion currently has no subheadings (CORRECT for Nature E&E)
- Results has subheadings (CORRECT)
- Methods has subheadings (CORRECT)
- Need to verify no section numbering (already set: `\setcounter{secnumdepth}{0}`)

#### 4. Figure Legends (MODERATE)
- Need to verify: center values, error bars, n, statistical tests, P values described
- Current legends need review for completeness

#### 5. Missing Sections (HIGH PRIORITY)
Need to add:
- [ ] Author Contributions statement
- [ ] Competing Interests statement
- [ ] Data Availability statement
- [ ] Code Availability statement
- [ ] Acknowledgements section

#### 6. Reference Format (LOW)
- Already using `naturemag` style - OK
- Verify article titles are included

#### 7. Supplementary Information (MODERATE)
- Current: Multiple supplementary sections
- Need: Consolidate into Nature E&E format (Supplementary Figures S1, S2... etc.)
- Extended Data figures (up to 10) can be moved from supplementary if essential

---

## Part 3: Conversion Plan - Step by Step

### Phase 1: Document Structure Reorganization

#### Step 1.1: Add Required Sections to main.tex

**Within Methods section** (as subsections at the end):
```latex
% At the END of Methods section, add:
\subsection*{Data Availability}
Raw sequencing data are available in NCBI SRA under BioProject accession PRJNAXXXXXX.
Processed data are available at [repository] with DOI: [XXX].

\subsection*{Code Availability}
Custom analysis scripts are available at [GitHub URL] with DOI: [Zenodo DOI].
```

**After Methods section** (as separate sections):
```latex
% Acknowledgements
\section*{Acknowledgements}
[Grant numbers, facility acknowledgements - brief]

% Author Contributions
\section*{Author Contributions}
J.S. designed and performed experiments, analyzed data, and wrote the manuscript.
J.H. contributed to experimental design and data analysis.
J.G. supervised the project and edited the manuscript.

% Competing Interests
\section*{Competing Interests}
The authors declare no competing interests.
```

#### Step 1.2: Reorganize Document Order
Nature E&E order (see Part 8 for full details):
1. Title
2. Authors & Affiliations
3. Abstract
4. Main text (Introduction, Results, Discussion)
5. References
6. Tables
7. Figure legends
8. Methods (Online Methods) - **including Data Availability and Code Availability as subsections**
9. Methods References (if any)
10. Acknowledgements
11. Author Contributions
12. Competing Interests
13. Additional Information
14. Extended Data legends (if any)
15. Supplementary Information (separate file)

### Phase 2: Word Count Reduction (~661 words to cut)

#### Step 2.1: Introduction (~743 words → ~600 words, cut ~143 words)
Target cuts:
- Condense historical background (Clements/Gleason paragraph)
- Tighten literature review
- Remove redundant phrases

#### Step 2.2: Results (~2,809 words → ~2,300 words, cut ~509 words)
Target cuts:
- Condense methodological descriptions (move details to Methods)
- Shorten figure legends (remove redundancy with caption)
- Tighten statistical reporting
- Move detailed simulation parameters to Methods

#### Step 2.3: Discussion (~609 words → ~600 words)
- Minor tightening only (already concise)

### Phase 3: Figure Legend Updates

#### Step 3.1: Ensure each legend includes:
- [ ] Brief title (bold)
- [ ] Description of what is shown
- [ ] Definition of center values (mean/median)
- [ ] Definition of error bars (s.d., s.e.m., 95% CI)
- [ ] Sample size (n = X)
- [ ] Statistical test used
- [ ] P values where relevant

### Phase 4: Supplementary Information Reorganization

#### Step 4.1: Rename/Reorganize Supplementary Figures
- Current: Multiple .tex files with various content
- Target: Single `supplementary_information.tex` or PDF with:
  - Supplementary Methods (if needed beyond main Methods)
  - Supplementary Figures (S1, S2, ..., each on one page)
  - Supplementary Tables
  - Supplementary Discussion (if any)

#### Step 4.2: Consider Extended Data
- Move 1-2 essential supplementary figures to Extended Data (max 10)
- Extended Data appears in HTML version linked from main text

### Phase 5: Technical LaTeX Updates

#### Step 5.1: Update main.tex preamble
```latex
% Ensure no section numbers (already done)
\setcounter{secnumdepth}{0}

% Use Nature-style figure citations
\newcommand{\figref}[1]{Fig.~\ref{#1}}  % Already present
```

#### Step 5.2: Verify bibliography
- Ensure `naturemag.bst` produces correct output
- Article titles should be included
- Check DOIs are included where available

### Phase 6: Final Checks

#### Step 6.1: Pre-submission checklist
- [ ] Main text ≤ 3,500 words
- [ ] Abstract ≤ 200 words, no references
- [ ] ≤ 6 display items in main text
- [ ] All figures cited in order (Fig. 1, Fig. 2, ...)
- [ ] Figure legends complete (n, error bars, stats)
- [ ] Author Contributions included
- [ ] Competing Interests declared
- [ ] Data Availability statement with accessions
- [ ] Code Availability statement
- [ ] Acknowledgements (brief)
- [ ] References in Nature format
- [ ] Supplementary Information properly formatted

#### Step 6.2: File preparation
- Main manuscript: Word or LaTeX (compile to single .tex with embedded .bbl)
- Figures: High-resolution (300 dpi), separate files
- Supplementary: Single PDF

---

## Part 4: Priority Action Items

### Immediate (Before submission)
1. **Reduce word count by ~661 words** - most critical
2. **Add required sections** (Author Contributions, Data Availability, etc.)
3. **Update figure legends** with required statistical details

### Secondary
4. Reorganize supplementary materials
5. Verify reference format
6. Final word count verification

### File Deliverables
1. `main.tex` - reformatted main manuscript
2. `supplementary_information.pdf` - consolidated supplementary
3. Individual figure files (PDF/EPS, 300 dpi)
4. Cover letter (separate)

---

---

## Part 5: Supplementary Information & Extended Data Format

### Current Supplementary Structure (31 figures)
```
supplementary_main.tex
├── supplementary_methods.tex
├── materials_protocols.tex
├── sequencing.tex
├── skewness_null_model.tex
├── assembly_effect.tex
├── simulations.tex
├── pairwise_selection_correlation.tex
├── invasion.tex
├── predictability.tex
├── natural_communities.tex
├── discussion.tex
└── figures.tex (31 supplementary figures S1-S31)
```

### Nature E&E Supplementary Information Rules

| Item Type | Format | Requirements |
|-----------|--------|--------------|
| **Extended Data** | Up to 10 figures/tables | Essential background; linked from main text HTML; NOT copy-edited; can be multi-panel; must fit single PDF page |
| **Supplementary Figures** | Single PDF page each | Use ONLY when Extended Data not appropriate; include legend on same page |
| **Supplementary Tables** | PDF or Excel | Complex tables as Excel; simple as PDF (none included in this submission) |
| **Supplementary Notes** | PDF | For algorithms, protocols, step-by-step methods |
| **Supplementary Data** | Repository preferred | Large datasets should go to repositories, NOT supplementary |

**IMPORTANT**:
- Extended Data figures must be referred to as discrete items in main text (e.g., "Extended Data Fig. 1")
- Supplementary Information is published AS SUPPLIED - ensure clear presentation
- Cite supplementary items in sequence, always include word "Supplementary"

### Issues with Current Supplementary

1. **Too many figures (31)** - Consider moving 8-10 most essential to Extended Data
2. **Missing figures** - S4, S9, S10, S20, S22, S23, S24, S26, S27 are placeholders (SVG or MISSING)
3. **Format issues** - Need to ensure each figure fits on single page with legend

### Recommended Extended Data Candidates (max 10)
Move these essential figures from Supplementary to Extended Data:
1. **S1** - Taxonomy color map (strain library reference)
2. **S2** - Phylogeny tree
3. **S8** - Skewness null model comparison (validates main result)
4. **S11** - Alternative interaction distributions (simulation robustness)
5. **S21** - Pairwise selection correlation across nutrients
6. **S25** - Assembly reduces interaction strength
7. **S28** - Natural communities coalescence (key validation)
8. **S29** - Selection correlation vs interaction strength

### Supplementary Figure Checklist
Each figure needs:
- [ ] Title (brief, informative)
- [ ] Legend with: what is shown, sample sizes (n), error bar definitions, statistical tests, P values
- [ ] Fits on single PDF page with legend
- [ ] High resolution (300 dpi minimum)
- [ ] Proper numbering: "Supplementary Fig. 1" (not "S1" or "Fig. S1")

---

## Part 6: Required Sections - Detailed Format

### 1. Author Contributions Statement

**Format**: Free text describing each author's role using initials.

**Example template**:
```
J.S. conceived and designed the study, performed experiments,
analyzed data, performed simulations, and wrote the manuscript.
J.H. contributed to experimental design, data analysis, and
edited the manuscript. J.G. supervised the research, provided
resources, and edited the manuscript.
```

**Equal contributions note** (if applicable):
```
*These authors contributed equally to this work.
```

### 2. Competing Interests Statement

**Format**: Brief declaration.

**Examples**:
```
The authors declare no competing interests.
```
OR if conflicts exist:
```
J.G. is a co-founder of [Company Name]. The other authors
declare no competing interests.
```

### 3. Data Availability Statement

**Format**: Must specify how to access data with persistent identifiers (DOIs, accession numbers).

**Template for your manuscript**:
```
Data Availability

Source data are provided with this paper. Raw 16S rRNA amplicon
sequencing data have been deposited in the NCBI Sequence Read
Archive under BioProject accession PRJNA[XXXXXX]
(https://www.ncbi.nlm.nih.gov/bioproject/PRJNA[XXXXXX]).
Processed community composition data and coalescence outcome
classifications are available in Figshare/Zenodo with the
identifier https://doi.org/10.xxxx/xxxxx. Source data for
Figures 1-5 and Extended Data Figures 1-X are provided as
Supplementary Data files.
```

**Key requirements**:
- Include repository name
- Include persistent identifier (DOI or accession number)
- Full URL to dataset
- Mention any restrictions

### 4. Code Availability Statement

**Format**: Must include DOI-minting repository (GitHub alone is NOT sufficient).

**Template for your manuscript**:
```
Code Availability

Custom Python scripts for gLV simulations, similarity calculations,
and statistical analyses are available at GitHub
(https://github.com/[username]/coalescence-analysis) and archived
on Zenodo with DOI: https://doi.org/10.5281/zenodo.[XXXXXX].
The code repository includes documentation for reproducing all
simulation results and figure generation.
```

**Key requirements**:
- GitHub link for browsing
- Zenodo DOI for permanent archival (GitHub integrates with Zenodo)
- Brief description of what code does
- License information (optional but recommended)

### 5. Acknowledgements

**Format**: Brief, no anonymous referees/editors.

**Template**:
```
Acknowledgements

We thank [specific names] for helpful discussions and [facility name]
for sequencing support. This work was supported by [grant agency]
grant [number] (to J.G.), [fellowship name] (to J.S.), and
[other funding]. [Optional: facility acknowledgements]
```

**Do NOT include**:
- Thanks to anonymous referees
- Thanks to editors
- Dedications (unless to someone directly involved who is not an author)

---

## Part 7: Action Items for Supplementary & Required Sections

### Immediate Actions

#### A. Supplementary Figures
1. [ ] Convert all SVG files to PDF (S4, S20, S26, S27)
2. [ ] Create missing figures (S9, S10, S22, S23, S24)
3. [ ] Verify each figure fits on single page with legend
4. [ ] Update figure numbering: "Supplementary Fig. X" format
5. [ ] Add complete statistical details to all legends

#### B. Extended Data (select ~8-10 from Supplementary)
1. [ ] Decide which figures to promote to Extended Data
2. [ ] Renumber remaining Supplementary figures
3. [ ] Update all main text references

#### C. Required Sections
1. [ ] Write Author Contributions
2. [ ] Write Competing Interests
3. [ ] Deposit data to NCBI SRA, get accession number
4. [ ] Deposit processed data to Figshare/Zenodo, get DOI
5. [ ] Archive code on Zenodo (link GitHub), get DOI
6. [ ] Write Data Availability statement with accessions/DOIs
7. [ ] Write Code Availability statement
8. [ ] Write Acknowledgements

---

## Part 8: Document Order (Final Format)

Nature E&E requires this order (based on Nature Portfolio formatting guide):

### Main Manuscript File
1. Title
2. Authors and affiliations (with present addresses if moved)
3. Abstract (≤200 words, no references) - called "bold first paragraph" in Nature main journal
4. Main text
   - Introduction (WITH heading - Nature E&E uses section headings)
   - Results (with topical subheadings)
   - Discussion (NO subheadings)
5. References (main text references)
6. Tables
7. Figure legends
8. **Methods/Online Methods** (with subheadings), containing:
   - Methodological subsections
   - **Data Availability** (as subsection within Methods)
   - **Code Availability** (as subsection within Methods)
9. Methods References (if additional references needed, numbered continuing from main refs)
10. Acknowledgements
11. Author Contributions
12. Competing Interests declaration
13. Additional Information (Supplementary Information line, corresponding author)
14. Extended Data figure/table legends (if any)

**IMPORTANT**: Data Availability and Code Availability appear as **subsections WITHIN the Methods section**, not as separate standalone sections. This is the Nature Portfolio standard.

### Separate Files
- Extended Data figures (PDF, each fits on single page; multi-panel allowed)
- Supplementary Information (single combined PDF)
- Individual main figure files (EPS/PDF, 300 dpi)
- Source Data files (Excel format, one per figure)

### Key Clarifications
- **Extended Data**: NOT copy-edited by journal; must follow journal style closely
- **Extended Data vs Supplementary**: Extended Data = essential background linked from main text; Supplementary = additional material not essential for understanding
- **Source Data**: Statistics source data in Excel; imaging data to repositories

---

## Part 9: Source Data Requirements

Nature E&E requires Source Data for figures:

### Statistics Source Data
- **Format**: Excel (.xlsx), one file per figure
- **Content**: Raw numerical data underlying statistical analyses
- **Naming**: Include linked figure number in filename (e.g., "Source_Data_Fig1.xlsx")

### Imaging Source Data
- Full-length unprocessed gels/blots as individual PDFs per figure
- Large imaging datasets: deposit to repository (not as supplementary)

### What to Include
- Data for main figures (Fig. 1-5)
- Data for Extended Data figures
- Should allow readers to verify statistical claims

---

## Part 10: Protocol Deposition (Optional but Encouraged)

Authors are encouraged to deposit step-by-step protocols to:
- **Protocol Exchange** (protocols.io) - open repository
- Deposited protocols will be linked from Online Methods upon publication

---

## Sources

- [Nature Ecology & Evolution Submission Guidelines](https://www.nature.com/natecolevol/submission-guidelines)
- [AIP and Formatting](https://www.nature.com/natecolevol/submission-guidelines/aip-and-formatting)
- [Preparing Your Submission](https://www.nature.com/natecolevol/submission-guidelines/preparing-your-submission)
- [Content Types](https://www.nature.com/natecolevol/content)
- [Reporting Standards](https://www.nature.com/natecolevol/editorial-policies/reporting-standards)
- [Data Availability Statements](https://www.springernature.com/gp/authors/research-data-policy/data-availability-statements)
- [Code Policy](https://www.springernature.com/gp/open-science/code-policy)
- [Author Contributions](https://www.nature.com/nature-portfolio/editorial-policies/authorship)
- [Nature Formatting Guide](https://www.nature.com/nature/for-authors/formatting-guide)
- [Extended Data Formatting](https://research-figure-guide.nature.com/figures/extended-data-formatting-guidelines/)
- [BibTeX naturemag style](https://www.bibtex.com/s/bibliography-style-nature-naturemag/)
