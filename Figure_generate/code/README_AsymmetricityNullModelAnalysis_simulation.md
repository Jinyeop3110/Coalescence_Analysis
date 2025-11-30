# AsymmetricityNullModelAnalysis_simulation.py

## Overview

This script performs asymmetricity null model analysis on simulation data, similar to the analysis done on experimental data in `AsymmetricityNullModelAnalysis.py`.

## What it Does

1. **Loads simulation data** from JSON files (e.g., `Simulation_Data/48species_100reps_final/Community_100reps_final.json`)
2. **Generates null models**:
   - Neutral Mixing: Tests if asymmetricity arises from random mixing (Offspring = α×Parent1 + (1-α)×Parent2)
   - Random Selection: Tests if diversity asymmetricity is due to random species retention (p=0.5)
3. **Calculates asymmetricity metrics**:
   - Similarity-based (Bray-Curtis, Jensen-Shannon)
   - Vector-based (magnitude decomposition)
   - Diversity-based Type 1 and Type 2
   - Retention-based Type 1 and Type 2
4. **Generates comparison plots** comparing experimental vs null model distributions
5. **Performs statistical tests** (Mann-Whitney U tests) to assess significance

## Current Status

### ✅ Working Components:
- Data loading from simulation JSON files with correct structure
- Null model generation (neutral mixing and random selection)
- Plot generation framework
- Output directory creation (`Figure/AsymmetricityNullModelAnalysis_simulation/`)

### ⚠️ Known Issues:
The script currently has dependency issues with the `AsymmetricityAnalysis` and `VariousMetrics` modules:
- `VariousMetrics` module is missing `get_similarity_function()` and `coalescence_vector_decomposition()` functions
- `AsymmetricityAnalysis.analyze_single_coalescence_asymmetricity()` relies on these missing functions
- This causes all asymmetricity calculations to return `NaN`, resulting in blank plots

## Data Structure

The simulation JSON files have this structure:
```json
{
  "0.3": {  // Interaction strength (float key)
    "rep_000": {  // Replicate
      "sc_list": {  // Single communities
        "0": [array],  // Community 0
        "1": [array],  // Community 1
        ...
      },
      "cc_list": {  // Coalescence communities
        "0_1": [array],  // Coalescence of communities 0 and 1
        "0_2": [array],
        ...
      },
      "parameters": {...}
    },
    ...
  },
  ...
}
```

## Usage

```python
from AsymmetricityNullModelAnalysis_simulation import run_simulation_null_model_analysis

results = run_simulation_null_model_analysis(
    simulation_dir="Simulation_Data/48species_100reps_final",
    interaction_strengths=None,  # Auto-detect all available strengths
    n_permutations=1000,
    save_plots=True,
    save_dir="Figure/AsymmetricityNullModelAnalysis_simulation"
)
```

## Fixes Needed

To make the script fully functional, you need to either:

### Option 1: Fix the dependencies
1. Update `VariousMetrics.py` to include the missing functions
2. Or update `AsymmetricityAnalysis.py` to use the correct function names

### Option 2: Implement calculations directly
Replace the `analyze_experimental_asymmetricity()` function with direct implementations of:
- Bray-Curtis and Jensen-Shannon similarity calculations
- Vector decomposition for asymmetricity
- Diversity-based asymmetricity (Type 1 and Type 2)
- Retention-based asymmetricity (Type 1 and Type 2)

## Output

When working correctly, the script generates:

1. **Plots** (PNG and SVG formats):
   - `diversity_asymmetricity_vs_random_selection.png`
   - `vector_asymmetricity_vs_neutral_mixing.png`
   - `similarity_asymmetricity_vs_neutral_mixing.png`

2. **Console output**:
   - Summary statistics for each interaction strength
   - Mann-Whitney U test results
   - Mean values for experimental vs null models

## Comparison with Experimental Analysis

This simulation analysis script follows the same structure as `AsymmetricityNullModelAnalysis.py` but:
- Uses simulation data instead of experimental coalescence data
- Groups by interaction strength instead of nutrient conditions
- Uses uniform retention probability (0.5) for null models instead of empirical probabilities
- Processes multiple coalescence pairs per replicate (e.g., all combinations like 0_1, 0_2, 1_2, etc.)

## Example Output Directory Structure

```
Figure/AsymmetricityNullModelAnalysis_simulation/
├── diversity_asymmetricity_vs_random_selection.png
├── diversity_asymmetricity_vs_random_selection.svg
├── vector_asymmetricity_vs_neutral_mixing.png
├── vector_asymmetricity_vs_neutral_mixing.svg
├── similarity_asymmetricity_vs_neutral_mixing.png
└── similarity_asymmetricity_vs_neutral_mixing.svg
```

## Notes

- Successfully loaded 1738 coalescence events from `48species_100reps_final`:
  - mean_0.30: 600 events
  - mean_0.50: 600 events
  - mean_0.80: 538 events
- The data loading and null model generation work correctly
- Only the asymmetricity calculation step needs fixing
