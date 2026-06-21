# Source Data README Draft

Nature source data should let reviewers and readers reproduce the plotted values in statistical figures without parsing image files.

Suggested final deliverable:

- one Excel workbook named `Source_Data.xlsx`, or
- one ZIP archive containing one CSV/XLSX per figure

Recommended structure:

- one sheet per main figure panel or compact panel group
- columns for plotted values, grouping variables, sample/event identifiers, and summary statistics
- a README sheet mapping sheets/files to figure panels
- no image-only data

For this manuscript, prioritize source data for main figures and statistical Extended Data figures:

- Fig. 1: coalescence similarity coordinates, class labels, richness labels, representative time-course abundance data
- Fig. 2: simulation outcome coordinates, assembly-filtering interaction summaries, pairwise selection correlation values
- Fig. 3: simulated outcome fractions and PDI distributions across interaction-strength parameter values
- Fig. 4: failed invasion frequencies, nutrient-condition coalescence outcomes, PDI distributions
- Fig. 5: dominant-species abundance, dominant-species competition metric, PDI, regression/statistics values
- Fig. 6: natural sample-derived coalescence outcomes and taxonomic/richness summaries
- Extended Data Figs. 2--8: plotted values for metric sensitivity, null models, robustness simulations, pH analysis, and pairwise selection correlations

The manifest in `SOURCE_DATA_MANIFEST.csv` lists likely local source files to use as inputs.

