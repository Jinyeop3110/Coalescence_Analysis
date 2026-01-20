# BibTeX Verification Report

**File:** `latex/references.bib`
**Date:** 2025-01-18
**Method:** CrossRef API verification

---

## Summary

| Category | Count |
|----------|-------|
| Total entries | 70 |
| Verified (no issues) | 54 |
| Minor discrepancies (OK) | 7 |
| **Critical issues to fix** | **3** |
| No DOI (cannot verify) | 3 |
| API error | 1 |

---

## Critical Issues (Must Fix)

### 1. Lu2022 - WRONG DOI

**Problem:** The DOI points to a completely different paper.

| Field | Current (WRONG) | Correct |
|-------|-----------------|---------|
| DOI | `10.1101/2022.06.21.496987` | `10.1101/282723` |
| Title at wrong DOI | "Global epistasis and the emergence of ecological function" | - |
| Your intended title | "Cohesiveness in Microbial Community Coalescence" | ✓ |

**Note:** This bioRxiv preprint (2018) was later published as a peer-reviewed paper: "Top-down and bottom-up cohesiveness in microbial community coalescence" in PNAS (DOI: `10.1073/pnas.2111261119`) - which you already have as `DiazColunga2022`.

**Recommended fix:**
```bibtex
@article{Lu2022,
  author    = {Lu, Nanxi and Sanchez-Gorostiaga, Alicia and Tikhonov, Mikhail and Sanchez, Alvaro},
  title     = {Cohesiveness in Microbial Community Coalescence},
  journal   = {bioRxiv},
  year      = {2018},
  doi       = {10.1101/282723}
}
```

---

### 2. Amor2024 - WRONG DOI

**Problem:** The DOI `10.1038/s41467-024-53001-7` returns a 404 error.

**Correct DOI found:** `10.1038/s41467-024-48521-9`

| Field | Current | Correct |
|-------|---------|---------|
| DOI | `10.1038/s41467-024-53001-7` | `10.1038/s41467-024-48521-9` |
| Volume | - | 15 |
| Pages | 8793 | 4709 |

**Recommended fix:**
```bibtex
@article{Amor2024,
  author    = {Lopes, William and Amor, Daniel R. and Gore, Jeff},
  title     = {Cooperative Growth in Microbial Communities Is a Driver of Multistability},
  journal   = {Nature Communications},
  volume    = {15},
  pages     = {4709},
  year      = {2024},
  doi       = {10.1038/s41467-024-48521-9}
}
```

---

### 3. Quast2013 - YEAR DISCREPANCY

**Problem:** The paper was published online in **2012**, but in print in 2013.

| Field | Your BibTeX | CrossRef |
|-------|-------------|----------|
| Year | 2013 | 2012 (online), 2013 (print) |

**Verdict:** Your year of **2013** is acceptable (print publication date). The paper appeared in the January 2013 issue (Volume 41, Issue D1). No change needed, but you may optionally use 2012 if you prefer the online publication date.

---

## Minor Discrepancies (OK - No Action Needed)

These are HTML encoding differences (`&` vs `&amp;`) - your BibTeX is correct:

| Entry | Field | Your BibTeX | CrossRef |
|-------|-------|-------------|----------|
| McGill2006 | journal | Trends in Ecology & Evolution | Trends in Ecology &amp;amp; Evolution |
| Hu2025 | journal | Nature Ecology & Evolution | Nature Ecology &amp;amp; Evolution |
| Ratzke2020 | journal | Nature Ecology & Evolution | Nature Ecology &amp;amp; Evolution |
| Rillig2015 | journal | Trends in Ecology & Evolution | Trends in Ecology &amp;amp; Evolution |
| Smillie2018 | journal | Cell Host & Microbe | Cell Host &amp;amp; Microbe |
| Louca2018 | journal | Nature Ecology & Evolution | Nature Ecology &amp;amp; Evolution |
| Tropini2017 | journal | Cell Host & Microbe | Cell Host &amp;amp; Microbe |

---

## Minor Journal Name Variations (OK)

| Entry | Your BibTeX | CrossRef |
|-------|-------------|----------|
| Gleason1939 | The American Midland Naturalist | American Midland Naturalist |
| Clements1936 | Journal of Ecology | The Journal of Ecology |

---

## Entries Without DOI (Cannot Verify)

These entries have no DOI and cannot be automatically verified:

1. **Shapiro1998** - "Thinking about bacterial populations as multicellular organisms"
2. **Clements1916** - "Plant Succession: An Analysis of the Development of Vegetation"
3. **Lovelock1979** - "Gaia: A New Look at Life on Earth" (book)

---

## Verified Entries (54 total)

The following entries passed CrossRef verification with no issues:

- Amor2020, Castledine2020, DiazColunga2022, Goldman2025, Keddy1992
- Hu2022, Huet2023, Lechon2021, Liu2024, Ratzke2018
- Rillig2017, Rocca2020, Tikhonov2016, West2006, Xiao2020
- Goldford2018, May1972, Allison2008, Zmora2018, Sanchez2021
- Marsland2020, Zelezniak2015, Coyte2021, Ianiro2022, Calderon2023
- Dunne2002, Gilpin1994, Vermeij1991, BentonEmerson2007, VanderGucht2007
- Gupta2021, WilsonSober1989, Walton2025, Kehe2021, Nadell2016
- Custer2024, Fukami2015, Callahan2016, Madeira2022, Debray2022
- Robinson2024, Zheng2021, Niehaus2021, OrozcoFuentes2024, Huet2025
- DiniAndreote2025, Cain1947, Mason1947, Whittaker1967, Tansley1935
- Odum1969, Sierocinski2017, RilligMansour2017, Leibold2004

---

## Recommended Actions

1. **Fix Lu2022 DOI** - Change from `10.1101/2022.06.21.496987` to `10.1101/282723`
2. **Fix Amor2024 DOI** - Change from `10.1038/s41467-024-53001-7` to `10.1038/s41467-024-48521-9`
3. **Update Amor2024 pages** - Change from `8793` to `4709`
4. **(Optional)** Consider if Lu2022 is redundant with DiazColunga2022 (same work, preprint vs published)
