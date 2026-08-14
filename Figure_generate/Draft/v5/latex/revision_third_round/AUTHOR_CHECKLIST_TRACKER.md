# Third-round author checklist tracker

Manuscript number: **NATECOLEVOL-26010384A**

Source: the author-checklist text supplied by the author on 2026-08-14, verified
against the original checklist `.docx` at
`../../revision_submission/00_submit_new/NATECOLEVOL-26010384A_Gore_Author_Guidance_1784820076_1 copy.docx`.
This file is a working parse, not the completed checklist that will ultimately be
returned to the journal.

## Status vocabulary

- **Open**: manuscript or submission work remains to be audited or completed.
- **Author confirmation**: requires information or approval from the authors.
- **External**: requires a repository, manuscript-tracking-system, Adobe PDF, or
  Word form action outside the LaTeX source.
- **Conditional**: required only if the stated condition applies.
- **Done**: verified in both the core and submission trees and ready for the
  checklist response.

Each final response should state what was checked or changed, identify the
relevant manuscript section or file, and avoid claiming completion until the
submission-facing artifact has also been verified.

### AC-50 — Review additional marked-up manuscript edits

**Status:** Open

**Required action:** Obtain and inspect any editor-supplied marked-up manuscript
file in addition to completing the checklist rows. Reconcile every marked edit
with the core manuscript, clean submission source, compiled PDF, and checklist
response. If no marked-up file was supplied, state that explicitly in the
working record rather than silently treating the instruction as complete.

**Checklist response:** This is a global instruction rather than a separate
response-table row; evidence remains pending.

## A. Abstract and editor's summary

### AC-01 — Replace the manuscript title

**Status:** Done

**Required title:**

> Interspecies interaction strength affects community-level selection in microbial coalescence

**Required action:** Replace the title in the core manuscript, submission source,
compiled manuscript PDFs, and any submission metadata or response documents that
repeat the title.

**Checklist response:** _Pending._

### AC-02 — Replace the abstract

**Status:** Done

**Required abstract:**

> Whether communities behave as cohesive units or as loose collections of independent species is a fundamental question in ecology. Here, we study this question in the context of community coalescence, the mixing of previously isolated communities, using synthetic bacterial microcosm experiments combined with Lotka–Volterra modelling. Our results demonstrate that effective interaction intensity and environmental feedbacks determine whether communities or species are the units of selection during coalescence. When effective interactions are moderate to strong, one parental community consistently outcompetes the other, indicating community-level selection. In contrast, under weak interactions, species fates are uncorrelated and the two communities contribute equally to the coalesced outcome, indicating the absence of community-level selection. A similar nutrient-dependent shift toward single-community dominance also appears in taxonomically richer communities derived from natural environmental samples. Furthermore, we identify two distinct regimes underlying community-level selection in experiments with different media conditions: an emergent regime in which collective dynamics shape outcomes that cannot be predicted from species traits alone, and a top-down regime where dominant species determine the winning community. Together, these results reconcile conflicting observations on community-level selection during community coalescence by demonstrating that communities behave as cohesive units only when effective interactions and feedbacks are sufficiently strong.

**Required action:** Replace the abstract in the core manuscript and submission
source exactly as requested, then rebuild and verify both PDFs. Check any cover
letter, summary, or response document that quotes the old abstract.

**Author decision (2026-08-14):** the manuscript abstract in both trees
(`latex/sections/title_abstract.tex` and
`revision_submission/00_submit_new/Main_Manuscript_Revised_LaTeX_Source/sections/title_abstract.tex`,
identical) was checked word-for-word against the required text above. Two
deviations were found and the author confirmed both are intentional and
acceptable rather than oversights: "modeling" (US spelling) is kept instead of
the editor's "modelling", and the natural-community sentence reads "shift toward
dominance of one parental community" instead of "shift toward single-community
dominance" (this wording was itself a deliberate second-round edit, marked
`\rev{}` in the source). No further text change requested; closing this item as
Done on the author's approval of the current wording.

**Checklist response:** We have edited the abstract in the manuscript to match
the proposed text, retaining two minor author-preferred wording choices
("modeling" for "modelling"; "dominance of one parental community" for
"single-community dominance") that convey the same meaning as the proposed
abstract.

## B. Author information

| ID | Status | Parsed requirement | Required evidence or deliverable | Checklist response |
|---|---|---|---|---|
| AC-03 | Author confirmation | All authors must confirm that names, affiliations, and titles are correct. Adding or removing authors later requires approval documentation. | Written coauthor confirmation; manuscript author and affiliation block checked against submission metadata. | Pending. |

## C. Article structure

| ID | Status | Parsed requirement | Required evidence or deliverable | Checklist response |
|---|---|---|---|---|
| AC-04 | Done | Main article may contain no more than 6 display items; Extended Data may contain no more than 10. Each item must fit easily on A4 (210 × 297 mm). | Verified: 6 main display items and 8 Extended Data figures; the prior artwork audit confirmed that all submitted display items fit A4. | Ready: manuscript contains six main display items and eight Extended Data figures, all fitting A4. |
| AC-05 | Done | Extended Data items must be cited in numerical order in the main text. | Verified citation sequence in the final main-manuscript source: 1, 1, 2, 3, 4, 5, 6, 7, 7, 8. | Ready: Extended Data figures are cited in numerical order. |
| AC-06 | Open | Shorten the manuscript toward 3,500 words, with the Introduction suggested as a target. | Reproducible word count using the journal-relevant scope; record before/after totals and any exclusions. | Pending. |
| AC-07 | Done | Main manuscript sections must appear in this order: title; author list; affiliations; abstract; main text; Methods; Data Availability; Code Availability if relevant; Acknowledgements; Funding Statement; Author Contributions; Competing Interests; tables; main figure legends; references. | Verified source include order and the compiled main-manuscript PDF; no tables are present. | Ready: all applicable required sections are in the requested order. |
| AC-08 | Done | Main text must be divided into Introduction, Results with at least one subheading, and Discussion. | Verified in the final source and compiled main-manuscript PDF. | Ready: Main text is divided into Introduction, Results with six subheadings, and Discussion. |

## D. Main text language and cross-references

| ID | Status | Parsed requirement | Required evidence or deliverable | Checklist response |
|---|---|---|---|---|
| AC-09 | Open | Do not describe the scientific findings as “new,” “novel,” or “first.” | Context-sensitive search of manuscript and Supplementary Information; revise prohibited novelty claims while preserving unrelated uses. | Pending. |
| AC-10 | Done | Cite specific Supplementary Information items, such as “Supplementary Fig. 3,” rather than referring only to “Supplementary Information.” | Verified that scientific cross-references name specific Supplementary Figures, Methods, or Notes; the remaining generic sentence is the standard availability statement. | Ready: scientific Supplementary citations are specific. |

## E. Figures, tables, and statistics

The journal artwork guide cited by the checklist is:
<https://www.nature.com/documents/NRJs-guide-to-preparing-final-artwork.pdf>

| ID | Status | Parsed requirement | Required evidence or deliverable | Checklist response |
|---|---|---|---|---|
| AC-11 | Open | Audit all artwork against the journal's final-artwork preparation guide. | File-format, dimensions, resolution, fonts, line weights, colour mode, and file-size audit. | Pending. |
| AC-12 | Open | Wherever statistics are derived, legends must define an exact numerical `n`, the unit of study, groups and controls, number and type of replicates, and the distinction between independent data and technical replicates. For microorganisms, the unit is the smallest object that could be randomly and independently assigned to an intervention; splitting one biological sample into multiple tubes or wells receiving the same treatment does not create independent replication. | Figure-by-figure legend audit, including sample-collection detail and rationale where no control group exists. | Pending. |
| AC-13 | Open | Statistics should not be derived from technical replicates or fewer than 3 biological replicates without explicit scientific justification. Technical and biological variability should not be conflated. | Analysis-unit audit and justification for any exception. | Pending. |
| AC-14 | Done | Extended Data Fig. 3b is specifically missing the sample, replicate, unit-of-study, comparison-group/control, and sampling-independence information required above. | Verified in the submitted Supplementary Information PDF and both source trees: the legend defines a coalescence event as one well, identifies paired null and observed values, states `n = 83` events from 46 pairings with two biological replicates, and names the one-sided paired Wilcoxon test with its exact P value. | Ready: the Extended Data Fig. 3b legend now supplies the requested sample, unit, replicate, comparison, and test information. |
| AC-15 | Open | Every legend with inferential statistics must name the test; specify one- or two-sidedness where applicable; state multiple-comparison adjustment or lack thereof where applicable; and, for null-hypothesis testing, report appropriate statistics, effect sizes, confidence intervals, degrees of freedom, and exact P values whenever possible. | Comprehensive main and Extended Data legend audit. | Pending. |
| AC-16 | Open | Name the statistical tests for Fig. 5c and Extended Data Figs. 6b–c and 7a–b; also give sidedness and multiple-comparison handling where applicable. | Targeted legend corrections and verification against analysis code/output. | Pending. |
| AC-17 | Open | Add whether tests were one- or two-sided, where appropriate, to the legends of Figs. 2c and 4d. | Targeted legend corrections verified against analysis code/output. | Pending. |
| AC-18 | Open | Give exact P values where possible for Fig. 5c and Extended Data Figs. 5a–c and 6b–c. | Exact values recovered from authoritative analysis output; legends/artwork updated consistently. | Pending. |
| AC-19 | Open | Define `*`, `**`, `***`, and `****` in Fig. 2d. If they encode P values, name the test, sidedness, multiple-comparison handling, and exact values in the legend. | Fig. 2d legend and artwork audit; exact value mapping documented. | Pending. |
| AC-20 | Open | Figures must be interpretable by readers with colour-vision deficiency; arbitrary green/red encodings should be recoloured. | Whole-figure colour audit, with particular attention to heatmaps, graphs, and schematics. | Pending. |
| AC-21 | Open | Every colour scale and intensity level must be defined in the figure or legend; colour bars need labels in a format such as “variable [unit].” | Whole-figure colour-scale audit and corrected labels/legends. | Pending. |

## F. Data and code

| ID | Status | Parsed requirement | Required evidence or deliverable | Checklist response |
|---|---|---|---|---|
| AC-22 | External | Deposit the data and code used in the paper in public repositories. If anything is available only on request, explain why both in the Data Availability statement and correspondence with the editor. Deposition is mandatory for some data types; any restrictions must be stated and discussed with the editor. | Public repository records, stable identifiers, and access verification. | Pending. |
| AC-23 | Open | Include a complete Data Availability section within Methods that transparently covers the minimum dataset needed to interpret, verify, and extend the work. Prefer public discipline-specific or general repositories over placing large datasets in Supplementary Information. | Final manuscript statement checked against actual repository contents and access conditions. | Pending. |
| AC-24 | Open | The Data Availability statement must reference Source Data published with the paper. | Explicit Source Data sentence, if Source Data are supplied. | Pending. |
| AC-25 | Conditional | Repository DOIs must also appear in the reference list with authors, title, repository/publisher, identifier, and year. | Bibliography entries and in-text/Data Availability citations for every DOI. | Pending applicability check. |
| AC-26 | Conditional | Clinical or third-party datasets must comply with Nature's data policy. | Dataset-specific compliance statement, if applicable. | Pending applicability check. |
| AC-27 | External | Include the final dynamic Reporting Summary PDF as a supplementary-information submission file; edit it in Adobe Reader rather than a browser. The form will be published alongside the paper. | Final completed smart PDF uploaded and readable. | Pending. |
| AC-28 | External | Deposit all DNA-sequencing or RNA-seq data in an approved public repository and state accession codes in Data Availability. | Public accession codes and verified manuscript statement. | Pending. |

## G. Methods and materials

| ID | Status | Parsed requirement | Required evidence or deliverable | Checklist response |
|---|---|---|---|---|
| AC-29 | Open | For all oligonucleotides, primers, RNAi/CRISPR reagents, and plasmids: describe generation, cite prior descriptions, or give company/catalogue information. Provide oligonucleotide sequences in Methods or in a separate Excel-format Supplementary Data file cited in Methods. | Reagent inventory reconciled with Methods and any cited Excel Supplementary Data file. | Pending. |
| AC-30 | Open | State how newly generated materials are available for reuse; give a sharing contact only if different from the corresponding author. | Materials-availability wording in Methods, plus a sharing contact if it differs from the corresponding author. | Pending. |

## H. End matter

| ID | Status | Parsed requirement | Required evidence or deliverable | Checklist response |
|---|---|---|---|---|
| AC-31 | Author confirmation | Review the full financial and non-financial Competing Interests policy. Include a detailed statement in the manuscript and an identical statement in the tracking system, with relevant author initials and patent numbers. If none exist, include a negative statement. | Author-approved CI wording; exact comparison with tracking-system entry. | Pending. |
| AC-32 | Author confirmation | Declare all relevant funding in a separate Funding Statement. | Author-approved funding statement reconciled with grants, funders, and submission metadata. | Pending. |

## I. Supplementary Figure checklist

These requirements apply to **every Supplementary Figure**, not only figures
named elsewhere in the checklist.

| ID | Status | Parsed requirement | Required evidence or deliverable | Checklist response |
|---|---|---|---|---|
| AC-33 | Conditional | Where data are presented as bar charts, show individual data points as overlaid dots. | Inventory of every Supplementary bar chart and confirmation that individual data points are overlaid, if any bar charts are present. | Pending applicability check. |
| AC-34 | Open | Provide a precise and defined sample size using wording such as `n=X samples/cells/independent experiments`, where applicable. | Caption-by-caption exact-`n` and unit audit. | Pending. |
| AC-35 | Open | Define axes, error bars, scale bars, molecular-weight markers, symbols, and colour scales. | Figure/caption definition audit. | Pending. |
| AC-36 | Open | Name every statistical test and give exact P values in the figure, legend, or Source Data file. | Statistics-to-source audit; document any justified threshold rather than exact value. | Pending. |
| AC-37 | Conditional | For representative data such as micrographs, state how many times the experiment was repeated with the same result. | Representative-data inventory and repetition statements where applicable. | Pending applicability check. |

## J. Manuscript-file preparation and rights

| ID | Status | Parsed requirement | Required evidence or deliverable | Checklist response |
|---|---|---|---|---|
| AC-38 | Done | Keep individual submission files near or below approximately 30 MB unless otherwise stated; use repositories for large datasets or Source Data. | Verified that no individual file in `revision_submission/00_submit_new` exceeds 30 MB. | Ready: all current submission files are below approximately 30 MB. |
| AC-39 | Open | Supply a third-person, broad-audience summary of the main findings, no more than 350 characters including spaces, in the cover letter. | Character-counted summary and updated cover letter. | Pending. |
| AC-40 | Author confirmation | Confirm copyright ownership or permission for reproduced/adapted figures, tables, images, movies, and text boxes, including material published previously, and provide proper creator attribution. | Rights audit and author confirmation. | Pending. |
| AC-41 | Conditional | If any included material is wholly or partly not copyrighted by the authors, complete and return the Third Party Rights Table with attribution. | Completed rights table and supporting permissions, if applicable. | Pending applicability check. |
| AC-42 | Conditional | If BioRender elements are present, obtain the correct publication licence, cite BioRender in the relevant legend, and upload the licence. | Licence, legend citation, and uploaded related-manuscript file, if applicable. | Pending applicability check. |
| AC-43 | Author confirmation | Check rights particularly carefully for illustrations in Figs. 1, 4, 5, and 6 and photographs in Fig. 6. | Figure-specific origin/licence record. | Pending. |

## K. Forms and Reporting Summary

| ID | Status | Parsed requirement | Required evidence or deliverable | Checklist response |
|---|---|---|---|---|
| AC-44 | External | Revise and submit the current Nature Reporting Summary using the dynamic PDF form. | Final Adobe-completed Reporting Summary. | Pending. |
| AC-45 | External | Complete the Inventory of Supporting Information with all Supplementary Information, Extended Data, and Source Data files. | Completed inventory `.docx`. | Pending. |
| AC-46 | Open + External | List all data-collection and data-analysis software, tools, algorithms, and packages, including version numbers, in both manuscript and Reporting Summary. | Reconciled software/version inventory in both locations. | Pending. |
| AC-47 | Open + External | Provide the same complete Data Availability information in the manuscript and Reporting Summary. | Cross-document consistency check. | Pending. |
| AC-48 | Author confirmation | State how often every experiment was replicated or independently performed. | Study-design inventory and Reporting Summary entry reconciled with legends/Methods. | Pending. |
| AC-49 | Author confirmation | Describe allocation of samples to experimental groups. If allocation was not random, explain covariate control; if randomization is irrelevant, explain why. | Author-approved study-design statement in Reporting Summary and, where necessary, Methods. | Pending. |

## L. Required upload inventory

| ID | Status | Required upload | Notes |
|---|---|---|---|
| UP-01 | Conditional | Completed Third Party Rights Table | Only if included material is wholly or partly not copyrighted by the authors. |
| UP-02 | Open | Point-by-point response to reviewers | Final, internally consistent version. |
| UP-03 | Open | Completed author checklist in `.docx` | This Markdown tracker is not the final upload. |
| UP-04 | Open | Main article in LaTeX or Microsoft Word | For Word, provide tracked and accepted versions. |
| UP-05 | Open | Separate main figure files | One file per figure. |
| UP-06 | Open | Separate Extended Data figure files | One file per Extended Data figure. |
| UP-07 | External | Inventory of Supporting Information in `.docx` | Must enumerate Supplementary, Extended Data, and Source Data files. |
| UP-08 | Open | Supplementary Information PDF | Verify against its source and final packaging. |
| UP-09 | External | Reporting Summary | Final dynamic PDF. |

## M. URLs supplied by the journal

- Final artwork guide: <https://www.nature.com/documents/NRJs-guide-to-preparing-final-artwork.pdf>
- Data-deposition and reporting standards: <https://www.nature.com/nature-research/editorial-policies/reporting-standards#availability-of-data>
- Recommended data repositories: <https://www.nature.com/sdata/policies/repositories>
- Competing Interests policy: <https://www.nature.com/nature-research/editorial-policies/competing-interests>
- Funding guidance: <https://www.nature.com/nature-portfolio/editorial-policies/funding>
- Reporting Summary form: <https://www.nature.com/documents/nr-reporting-summary.pdf>
- Inventory of Supporting Information: <http://www.nature.com/documents/Inventory_of_Supporting_Information_2021.docx>
- BioRender publishing guidance: <https://help.biorender.com/hc/en-gb/articles/21283116932765-CC-BY-publishing-and-reader-permissions>
- Third Party Rights Table: <https://www.nature.com/documents/thirdpartyrights-origres.docx>

## N. Journal response-row crosswalk

The checklist contains **36 distinct logical guidance blocks**. The detailed
action IDs above intentionally split some multi-part blocks into separate
verifiable tasks. The crosswalk was checked against the original `.docx`; JR-29
and JR-30 are retained as separate logical rows for response drafting even if
they are presented together in a single Word-table response cell.

| Journal row | Checklist section and guidance | Detailed action ID(s) |
|---|---|---|
| JR-01 | Abstract and editor's summary — revised title | AC-01 |
| JR-02 | Abstract and editor's summary — revised abstract | AC-02 |
| JR-03 | Author information — names, affiliations, titles, and author-list changes | AC-03 |
| JR-04 | Article structure — display-item limits, ED citation order, and A4 fit | AC-04, AC-05 |
| JR-05 | Article structure — shorten toward 3,500 words | AC-06 |
| JR-06 | Article structure — required manuscript section order | AC-07 |
| JR-07 | Article structure — Introduction, Results subheading(s), and Discussion | AC-08 |
| JR-08 | Main text — avoid new/novel/first claims | AC-09 |
| JR-09 | Main text — cite specific Supplementary items | AC-10 |
| JR-10 | Figures and Tables — final-artwork guide | AC-11 |
| JR-11 | Figures and Tables — exact `n`, units, groups, controls, and replicate definitions | AC-12, AC-13 |
| JR-12 | Figures and Tables — missing information in Extended Data Fig. 3b | AC-14 |
| JR-13 | Figures and Tables — general statistical-reporting requirements | AC-15 |
| JR-14 | Figures and Tables — tests/sidedness/adjustment for Fig. 5c and ED Figs. 6b–c, 7a–b | AC-16 |
| JR-15 | Figures and Tables — sidedness for Figs. 2c and 4d | AC-17 |
| JR-16 | Figures and Tables — exact P values for Fig. 5c and ED Figs. 5a–c, 6b–c | AC-18 |
| JR-17 | Figures and Tables — significance-symbol definition for Fig. 2d | AC-19 |
| JR-18 | Figures and Tables — colour-vision accessibility | AC-20 |
| JR-19 | Figures and Tables — define colour scales and intensity levels | AC-21 |
| JR-20 | Data and Code — public availability, minimum dataset, Source Data, DOI references, and restricted/third-party data | AC-22–AC-26 |
| JR-21 | Data and Code — final dynamic Reporting Summary PDF | AC-27 |
| JR-22 | Data and Code — public sequencing repository and accessions | AC-28 |
| JR-23 | Methods — oligonucleotides, plasmids, sequences, commercial details, and reuse | AC-29, AC-30 |
| JR-24 | End matter — Competing Interests | AC-31 |
| JR-25 | End matter — separate Funding Statement | AC-32 |
| JR-26 | Additional Revisions — five-part Supplementary Figure checklist | AC-33–AC-37 |
| JR-27 | Preparing files — approximately 30 MB per file | AC-38 |
| JR-28 | Preparing files — ≤350-character broad-audience summary in cover letter | AC-39 |
| JR-29 | Preparing files — third-party rights and BioRender licensing | AC-40–AC-42 |
| JR-30 | Preparing files — particular rights check for Figs. 1, 4, 5, and 6 | AC-43 |
| JR-31 | Forms — revise and submit the Reporting Summary | AC-44 |
| JR-32 | Forms — complete Inventory of Supporting Information | AC-45 |
| JR-33 | Reporting Summary — software/tools/algorithms/packages and versions | AC-46 |
| JR-34 | Reporting Summary — complete Data Availability statement | AC-47 |
| JR-35 | Reporting Summary — replication/independent-performance frequency | AC-48 |
| JR-36 | Reporting Summary — sample allocation, randomization, or explanation of non-applicability | AC-49 |

The opening marked-up-edit instruction maps to AC-50 but does not appear to be a
separate “Your response” row. The final upload list maps to UP-01–UP-09 and
likewise does not appear to add response rows.

## O. Final response template

Use this structure for each row when completing the journal's checklist:

> We have [made the requested change / checked and confirmed the requested
> information]. Specifically, [state the exact edit or verification], in
> [section, figure legend, form, or submission file]. [If applicable, state
> the exact sample size, test, accession, DOI, version, or file name].

Do not use “done,” “addressed,” or “confirmed” alone; every response should say
what was changed or what evidence was checked.
