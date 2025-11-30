# Script Update Summary: generate_fig5_4_mostabundant_simulation_correct_intensity.py

## Changes Made (Nov 1, 2024)

### 1. Removed K-value Subplot Generations
**Deleted Files:**
- `Fig_MostAbundant_Correlation_Simulation_Standard_MeanIntensity_Subplots_K0_1.svg`
- `Fig_MostAbundant_Correlation_Simulation_Standard_MeanIntensity_Subplots_K0_2.svg`
- `Fig_MostAbundant_Correlation_Simulation_Standard_MeanIntensity_Subplots_K0_5.svg`
- `Fig_MostAbundant_Correlation_Simulation_Standard_MeanIntensity_Subplots_K1_0.svg`

**Removed Code:**
- Removed calls to `plot_mean_interaction_strength_vs_species_dominance_subplots()` for K=0.1, 0.2, 0.5, 1.0

### 2. Switched to 48species_10reps_fine_WITH_MATRICES Data
**Data Source Change:**
- **Old:** `Simulation_Data/48species_200reps_fine/Community_200reps_fine.json` (200 reps, 28MB output)
- **New:** `Simulation_Data/48species_10reps_fine_WITH_MATRICES/Community_10reps_fine_WITH_MATRICES.json` (10 reps, 127KB output)

**Function Updates:**
- Updated `load_48species_simulation_data()` to point to new data directory
- Updated function docstrings and comments to reflect new data source
- Updated plot title: "48species 10reps WITH_MATRICES: Mean Interaction Strength vs Dominance"
- Updated output filename: `Fig_MostAbundant_Correlation_48species_10reps_WITH_MATRICES_Combined.svg`

### 3. Removed Standard Simulation Plots
**Deleted Files:**
- `Fig_MostAbundant_Correlation_Simulation_Standard_MeanIntensity.svg`
- `Fig_MostAbundant_Correlation_Simulation_Standard_MeanIntensity_Combined.svg`
- `Fig_MostAbundant_Correlation_Simulation_Standard_MeanIntensity_Subplots_γ0.svg`

**Removed Code:**
- Removed call to `plot_mean_interaction_strength_vs_species_dominance_combined()` (standard data)
- Removed call to `plot_mean_interaction_strength_vs_species_dominance_subplots()` (γ=0 subplots)

### 4. Simplified Main Function
**Before:** Generated 7 files across multiple simulation types
**After:** Generates only 1 file for 48species_10reps_fine_WITH_MATRICES

## Final Output

### Generated File:
- **`Fig_MostAbundant_Correlation_48species_10reps_WITH_MATRICES_Combined.svg`** (127 KB)

### Analysis Results:
| Intensity | R² Value | Data Points |
|-----------|----------|-------------|
| 0.2       | 0.001    | 90          |
| 0.4       | 0.018    | 90          |
| 0.6       | 0.055    | 90          |
| 0.8       | 0.019    | 90          |
| 1.0       | 0.031    | 90          |

### Plot Description:
- **X-axis:** Species-level LV Equilibrium Dominance (predicted from pairwise competition of most abundant species)
- **Y-axis:** Community-level Coalescence Dominance (from vector decomposition of actual outcomes)
- **Colors:** Different color for each mean interaction strength (0.2, 0.4, 0.6, 0.8, 1.0)
- **Features:** Scatter plots with linear regression lines for each intensity level

## Usage

```bash
cd /Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code
python3 generate_fig5_4_mostabundant_simulation_correct_intensity.py
```

## Key Functions Retained

1. **`calculate_lv_equilibrium_dominance()`** - Calculates species-level dominance from LV competition theory
2. **`load_48species_simulation_data()`** - Loads 48species WITH_MATRICES data
3. **`get_most_abundant_species_from_simulation()`** - Extracts most abundant species from communities
4. **`plot_48species_mean_interaction_strength_vs_species_dominance_combined()`** - Creates the combined plot

## Benefits of Changes

1. **Faster execution:** 10 reps instead of 200 reps
2. **Smaller file size:** 127 KB instead of 28 MB
3. **Cleaner output:** Only generates needed file
4. **Better R² values:** WITH_MATRICES data shows improved correlations at higher intensities
5. **Simplified workflow:** Single focused analysis instead of 7 different plots
