# Lotka-Volterra Simulation Framework - Detailed Documentation

## Overview

This documentation describes the generalized Lotka-Volterra (gLV) simulation framework used to model microbial community dynamics and coalescence events. The framework simulates competitive interactions between multiple species and predicts community assembly outcomes.

## Mathematical Model

### Generalized Lotka-Volterra Equations

The dynamics of species abundance are governed by the generalized Lotka-Volterra equations:

```
dN_i/dt = g_i * N_i * (1 - Σ_j(I_ij * N_j) / k_i)
```

Where:
- `N_i(t)`: Abundance of species i at time t
- `g_i`: Growth rate of species i
- `k_i`: Carrying capacity of species i
- `I_ij`: Interaction coefficient between species i and j
  - `I_ii = 1`: Intraspecific competition
  - `I_ij > 0`: Competition (species j inhibits species i)
  - `I_ij < 0`: Facilitation (species j helps species i)

## Implementation Details

### Core Functions

#### 1. `gLV(y, t, I_simul, g_simul, k_simul)` - LV.py
Implements the differential equations for the gLV model.

**Parameters:**
- `y`: Current species abundances (array)
- `t`: Time point
- `I_simul`: Interaction matrix (NxN array)
- `g_simul`: Growth rates (array)
- `k_simul`: Carrying capacities (array)

**Returns:**
- `dydt`: Rate of change of species abundances

#### 2. `run_lotka_volterra(y0, t, s_idx, I, g, k)` - LV.py
Runs simulation to steady state using scipy's solve_ivp with RK23 method.

**Parameters:**
- `y0`: Initial species abundances
- `t`: Time interval [t_start, t_end]
- `s_idx`: Boolean array indicating which species are present
- `I, g, k`: Full interaction matrix, growth rates, and carrying capacities

**Returns:**
- Final species abundances at steady state

#### 3. `run_lotka_volterra_dynamics(y0, t, s_idx, I, g, k, t_eval)` - LV.py
Runs simulation with time series output for dynamics analysis.

### Species Pool Initialization

#### `InitializeSpeciesPool(N, f_interaction, f_g, f_k, is_diagonal_one, save_path)`

Generates random parameters for the species pool:

**Interaction Matrix Generation:**
- Diagonal elements: Set to 1 (self-competition)
- Off-diagonal elements: Drawn from distribution defined by `f_interaction`
- Typical distribution: Uniform on [-o, 2u+o] where u is mean interaction strength

**Growth Rates:**
- Default: All species have g_i = 1
- Can be customized via `f_g` function

**Carrying Capacities:**
- Constant: `f_k = lambda: 1`
- Gaussian: `f_k = lambda: max(np.random.normal(1, σ), 0.1)`
- Gamma: `f_k = lambda: max(np.random.gamma(shape=1/var_k, scale=var_k), 0.1)`

### Community Assembly

#### `InitializeRandomCommunityPool(N, num_C, num_S, I, g, k, save_path)`

Creates random communities by selecting species subsets:
- `N`: Total species pool size
- `num_C`: Number of communities
- `num_S`: Species per community
- Random selection without replacement within each community

## Simulation Workflow

### 1. Single Community Dynamics

For each community:
```python
# Initialize with small random abundances
y = np.random.rand(N) * 0.1

# Run to steady state (t=5000 is typical)
y_final = run_lotka_volterra(y, [0, 5000], community_mask, I, g, k)

# Apply extinction threshold
y_final[y_final < threshold] = 0
```

### 2. Coalescence Simulation

Simulates mixing two communities:
```python
# Get steady states of individual communities
y1 = run_lotka_volterra(y, t, community1_mask, I, g, k)
y2 = run_lotka_volterra(y, t, community2_mask, I, g, k)

# Mix communities (equal proportions)
y3 = (y1 + y2) / 2

# Run to new steady state
survived = y3 > threshold
y3_final = run_lotka_volterra(y3, t, survived, I, g, k)
```

## Parameter Ranges

### Standard Simulation Parameters

- **Species pool size (N)**: 48 species
- **Communities (num_C)**: 9 communities
- **Species per community (num_S)**: 12 species
- **Time span**: [0, 5000]
- **Extinction threshold**: 1e-3
- **Initial abundance**: Random [0, 0.1]

### Interaction Strength Variation

- **u_list**: [0, 0.1, 0.2, ..., 1.1] (mean interaction strength)
- **o**: 0 (offset parameter, typically 0)
- **Distribution**: Uniform on [0, 2u]

### Carrying Capacity Variation

- **var_k = 0**: Constant k=1 (no variation)
- **var_k > 0**: Gamma distribution with:
  - Shape = 1/var_k
  - Scale = var_k
  - Mean = 1
  - Variance = var_k

## Data Output Structure

### Community.json Format

```json
{
  "interaction_strength_value": {
    "community_0": {
      "sc_list": {
        "0": [abundance_array],  // Community 0 alone
        "1": [abundance_array],  // Community 1 alone
        ...
      },
      "cc_list": {
        "0_1": [abundance_array],  // Coalescence of 0 & 1
        "0_2": [abundance_array],  // Coalescence of 0 & 2
        ...
      }
    },
    ...
  }
}
```

### Additional Output Files

1. **parameter.xlsx**: Contains I, g, k matrices
2. **communityLibrary.xlsx**: Community composition (species membership)
3. **results_dominance_fractions.json**: Analysis of coalescence outcomes
4. **results_intensity_X.json**: Results for specific interaction strengths

## Metrics and Analysis

### Coalescence Outcomes Classification

1. **Dominance**: One community completely excludes the other
2. **Mixing**: Both communities coexist with minimal change
3. **Restructuring**: New community structure emerges

### Vector Decomposition Analysis

Decomposes final community into contributions from:
- Community 1 species
- Community 2 species
- Emergent structure

### Similarity Metrics

- **Bray-Curtis similarity**: Measures compositional similarity
- **Jaccard index**: Measures species overlap
- **SimilarityTo1**: Asymmetric measure of outcome bias

## Numerical Considerations

### Solver Settings
- **Method**: RK23 (Explicit Runge-Kutta of order 3(2))
- **Tolerances**: Default scipy values
- **Max time**: 5000 time units (ensures steady state)

### Extinction Threshold
- Species with abundance < 1e-3 are considered extinct
- Prevents numerical issues with very small populations
- Applied after each simulation step

### Normalization
- Community mixing uses equal proportions (0.5 each)
- Alternative: Weight by total biomass
- Results normalized for analysis (sum to 1)

## Performance Optimization

### Parallelization
- Uses `pathos.multiprocessing.ProcessingPool`
- Typically 8 processes for parameter sweeps
- Each replicate runs independently

### Memory Management
- Sparse species interactions (only present species simulated)
- Results aggregated and saved periodically
- JSON format for flexibility and readability

## Validation and Testing

### Equilibrium Checks
- Verify steady state reached (dy/dt ≈ 0)
- Check for oscillations or chaos
- Validate conservation laws

### Parameter Sensitivity
- Test different initial conditions
- Verify robustness to numerical parameters
- Check boundary conditions (k→0, large I)

## Extensions and Modifications

### Alternative Interaction Distributions
- Exponential: Mostly weak interactions
- Normal: Symmetric positive/negative interactions
- Structured: Block matrices for functional groups

### Dynamic Parameters
- Time-varying carrying capacities
- Environmental fluctuations
- Adaptive evolution of interaction strengths

### Spatial Structure
- Metacommunity dynamics
- Migration between patches
- Local vs. global competition

## References

1. Generalized Lotka-Volterra equations for community dynamics
2. Numerical methods for stiff ODEs in ecology
3. Community assembly theory and coalescence
4. Microbial interaction networks

---

*This documentation describes the simulation framework as implemented in the Gore Lab coalescence analysis pipeline.*