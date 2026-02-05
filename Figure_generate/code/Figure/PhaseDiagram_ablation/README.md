# Phase Diagram Ablation Study Figures

## Overview

This folder contains phase diagrams from ablation studies testing the robustness of coalescence simulation results to different parameter choices.

## Figure Types

### Standard Phase Diagrams (`*_superfine.pdf/svg/png`)
- Standard stacked area plots showing coalescence outcome fractions
- X-axis: Interaction strength μ (0.05 to 1.21, step 0.02)
- Y-axis: Coalescence outcome fraction (0 to 1)
- Colors: Red (Dominance), Purple (Mixing), Green (Restructuring)

### Annotated Phase Diagrams (`*_annotated.pdf/svg/png`)
- Same as standard but with vertical dashed lines at μ = 0.3, 0.6, 0.8
- Percentage annotations showing outcome fractions at each marked position
- μ labels displayed above the plot at each marked position

## Ablation Studies

### 1. Interaction Distribution (`ablation_gaussian`, `ablation_gamma`)
- **Gaussian**: N(μ, (μ/√3)²), CV = 0.577
- **Gamma**: Γ(k=3, θ=μ/3), CV = 0.577
- Both distributions have the same mean (μ) and coefficient of variation as the uniform distribution

### 2. Growth Rate Heterogeneity (`ablation_growth_std01`, `ablation_growth_std02`)
- **std=0.1**: Growth rates sampled from N(1, 0.1²)
- **std=0.2**: Growth rates sampled from N(1, 0.2²)
- Tests robustness to intrinsic growth rate variation among species

### 3. Carrying Capacity Heterogeneity (`ablation_k_std01`, `ablation_k_std02`)
- **std=0.1**: Carrying capacities sampled from N(1, 0.1²)
- **std=0.2**: Carrying capacities sampled from N(1, 0.2²)
- Tests robustness to carrying capacity variation among species

### 4. Species Number (`ablation_Xpercomm`)
- Tests different numbers of species per community: 4, 6, 9, 12, 24, 48
- Total species pool = 4 × species_per_community

## Simulation Parameters

- **Repetitions**: 400 per interaction strength
- **Interaction strengths**: 59 values from 0.05 to 1.21 (step 0.02)
- **Total simulations per ablation**: 23,600
- **Communities**: 4 communities per simulation
- **Coalescence events**: 6 pairwise coalescence events per simulation

## Data Processing

1. Load JSON simulation data containing:
   - `sc_list`: Single community compositions after assembly
   - `cc_list`: Coalesced community compositions

2. Apply vector decomposition analysis:
   - Decompose coalesced community as linear combination of parents
   - Calculate coefficients (u, v, k) representing parent contributions

3. Classify outcomes using asymmetricity-based boundaries:
   - **Dominance (CLS)**: One parent community dominates
   - **Mixing**: Balanced contribution from both parents
   - **Restructuring**: Significant novel composition

## Annotation Details

For annotated figures, vertical lines are placed at μ values closest to 0.3, 0.6, 0.8:
- Since data uses step 0.02 starting from 0.05, actual values are 0.31, 0.61, 0.81
- Labels display rounded values (μ=0.3, μ=0.6, μ=0.8) for clarity
- Percentages show outcome fractions at those specific interaction strengths

## Usage

```bash
# Generate standard phase diagrams
python plot_phase_diagram_ablation_superfine.py

# Generate annotated phase diagrams
python plot_phase_diagram_ablation_annotated.py

# Custom annotation positions
python plot_phase_diagram_ablation_annotated.py --mu 0.31,0.61,0.81
```

## File Naming Convention

- `Fig_phase_diagram_ablation_<type>.pdf` - Standard version (for supplementary)
- `Fig_phase_diagram_ablation_<type>_superfine.pdf` - Superfine resolution version
- `Fig_phase_diagram_ablation_<type>_annotated.pdf` - Annotated version with μ markers
