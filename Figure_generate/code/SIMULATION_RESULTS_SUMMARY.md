# 48-Species Coalescence Simulation Results Summary

## Simulation Overview

**Completed**: Test simulation with 48 species, 10 repetitions per interaction strength
- **Species Pool**: 48 total species
- **Communities**: 4 communities of 12 species each per repetition
- **Interaction Strengths**: 0.3 (low), 0.5 (medium), 0.8 (high)
- **Repetitions**: 10 per interaction strength (30 total simulations)
- **Coalescence Pairs**: 6 pairs per repetition (C(4,2) = 6)
- **Total Data Points**: 180 coalescence events analyzed

## Key Findings

### 1. Interaction Strength Dramatically Affects Coalescence Outcomes

| Interaction Strength | Dominance | Mixing | Restructuring |
|---------------------|-----------|--------|---------------|
| **u = 0.3** (Low)   | 21.7%     | **60.0%** | 18.3% |
| **u = 0.5** (Medium)| **40.0%** | 28.3%     | 31.7% |
| **u = 0.8** (High)  | **70.0%** | 10.0%     | 20.0% |

### 2. Clear Pattern Emerges

- **Low Interaction (u=0.3)**: Communities tend to **mix evenly** (60% mixing outcomes)
- **Medium Interaction (u=0.5)**: Balanced distribution with slight dominance preference
- **High Interaction (u=0.8)**: Strong **competitive exclusion** - one community dominates (70% dominance)

### 3. Vector Decomposition Coordinates

The (u,v) coordinates from vector decomposition show distinct patterns:

**u = 0.3 (Low Interaction)**:
- More evenly distributed coordinates
- Higher concentration around the diagonal (u≈v)
- Mean coordinates: u=0.504, v=0.577

**u = 0.5 (Medium Interaction)**:
- Broader spread of coordinates
- More variance: u_std=0.279, v_std=0.291
- Some extreme values (0.0 to 1.0 range)

**u = 0.8 (High Interaction)**:
- Many points clustered at extremes (0,0) and (1,1)
- High variance: u_std=0.400, v_std=0.410
- Strong polarization - either complete dominance or competitive exclusion

## Biological Interpretation

### Low Interaction Strength (u=0.3)
- **Weak competition** between species
- **Coexistence** is more likely
- **Mixing outcomes** dominate (60%)
- Communities blend more harmoniously

### High Interaction Strength (u=0.8) 
- **Strong competition** between species
- **Competitive exclusion** is common
- **Dominance outcomes** prevail (70%)
- One community outcompetes the other

### Medium Interaction Strength (u=0.5)
- **Intermediate competition** level
- **Balanced outcomes** across all three categories
- **Transitional** behavior between low and high interaction regimes

## Technical Implementation

### Successfully Created:
1. ✅ **Simulation Engine** (`run_48species_test.py`)
   - Lotka-Volterra dynamics
   - Random species pool initialization per repetition
   - Non-overlapping community structure

2. ✅ **Vector Decomposition Analysis** (`analyze_test_data_simple.py`)
   - Calculates (u,v) coordinates for each coalescence event
   - Classifies outcomes into dominance/mixing/restructuring
   - Robust error handling for singular matrices

3. ✅ **Visualization System** (`create_heatmap_plots.py`)
   - ASCII heatmap representation
   - Statistical summaries
   - Cross-intensity comparisons

### Data Storage Format
```json
{
  "0.3": {
    "rep_000": {
      "sc_list": {...},      // Single community outcomes
      "cc_list": {...},      // Coalescence outcomes  
      "parameters": {...}    // Simulation metadata
    },
    ...
  }
}
```

## Next Steps for Full Implementation

### For 100 Repetitions:
1. **Scale up** the test simulation to 100 repetitions per intensity
2. **Parallelize** computation for faster execution
3. **Fix matplotlib** dependency for proper heatmap plots
4. **Add statistical tests** to quantify significance of differences

### For Publication-Quality Figures:
1. **2D Density Heatmaps** with smooth contours
2. **Statistical Error Bars** and confidence intervals  
3. **Phase Diagrams** showing transition boundaries
4. **Comparison with Experimental Data**

## Validation

The results show **biologically plausible patterns**:
- ✅ Higher competition → More exclusion (dominance)
- ✅ Lower competition → More coexistence (mixing)  
- ✅ Smooth transitions between regimes
- ✅ Consistent with Lotka-Volterra theory

## Files Generated

### Simulation Data:
- `Simulation_Data/48species_test/Community_test.json`

### Analysis Results:
- `Analysis_Results/processed_test_data.json`

### Code:
- `run_48species_test.py` - Simulation engine
- `analyze_test_data_simple.py` - Data analysis
- `create_heatmap_plots.py` - Visualization

---

**Status**: ✅ Test simulation and analysis pipeline completed successfully
**Next**: Scale to 100 repetitions and create publication-quality figures