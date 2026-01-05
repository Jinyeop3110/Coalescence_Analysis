# Retention-Based Asymmetricity Analysis - Implementation Summary

## ✅ **What Was Implemented**

### **Core Functions Added to `AsymmetricityAnalysis.py`:**

1. **`calculate_retention_asymmetricity_base()`** - Base function with version control
2. **`calculate_retention_asymmetricity_type1()`** - Exclude overlap species (like diversity type 1)
3. **`calculate_retention_asymmetricity_type2()`** - Include overlap species (like diversity type 2)

### **Integration with Existing Pipeline:**

- **Updated `analyze_single_coalescence_asymmetricity()`** to include retention analysis
- **Updated `analyze_multiple_coalescence_asymmetricity()`** to collect retention results
- **Added retention asymmetricity to results structure** with both type1 and type2

### **New Plotting Functions:**

1. **`plot_retention_asymmetricity()`** - Plot single type across conditions
2. **`plot_retention_asymmetricity_comparison()`** - Compare type1 vs type2 side-by-side  
3. **`plot_retention_vs_diversity_asymmetricity()`** - Compare retention vs diversity methods

## 🔬 **How the Method Works**

### **Version 1 (Type 1): Exclude Overlaps**
- **Focus:** Unique species from each parent
- **Calculation:** 
  - Parent 1 retention = (P1 unique species retained) / (P1 unique species total)
  - Parent 2 retention = (P2 unique species retained) / (P2 unique species total)
- **Asymmetricity:** |R1 - R2|

### **Version 2 (Type 2): Include Overlaps** 
- **Focus:** All species from both parents
- **Calculation:**
  - Parent 1 retention = (P1 species retained) / (P1 total species)
  - Parent 2 retention = (P2 species retained) / (P2 total species)
- **Asymmetricity:** |R1 - R2|

### **Statistical Significance Testing**
- **Permutation test:** Randomly reassign species retention to parents
- **Null hypothesis:** Both parents have equal retention probabilities
- **P-value:** Fraction of permutations with asymmetricity ≥ observed
- **Effect size:** Small (<0.1), Medium (0.1-0.3), Large (>0.3)

## 📊 **What Each Function Returns**

```python
{
    'asymmetricity': float,           # |R1 - R2|
    'retention_rates': {
        'parent1': float,             # Parent 1 retention rate
        'parent2': float              # Parent 2 retention rate  
    },
    'p_value': float,                 # Permutation test p-value
    'significant': bool,              # p < 0.05
    'effect_size': str,               # 'Small'/'Medium'/'Large'
    'species_breakdown': {            # Analysis by species type
        'overlap': {...},
        'parent1_unique': {...},
        'parent2_unique': {...}
    },
    'null_distribution': {            # Permutation test results
        'mean': float,
        'std': float,
        'values': list
    },
    'version': int,                   # 1 or 2
    'version_description': str        # Human-readable description
}
```

## 🎯 **Key Advantages Over Diversity-Based Measures**

### **Problems with Old Method:**
❌ **Baseline Diversity Bias:** Low-diversity communities appear artificially "more asymmetric"
❌ **No Statistical Testing:** Can't distinguish significant from random patterns  
❌ **Mathematical Artifacts:** Results confound diversity constraints with biology
❌ **No Cross-Study Comparison:** Results not comparable across different diversity levels

### **Solutions with New Method:**
✅ **Diversity-Controlled:** Retention rates are comparable across all diversity levels
✅ **Statistical Rigor:** P-values and effect sizes from permutation tests
✅ **Biological Focus:** Tests retention mechanisms rather than outcome counts
✅ **Species-Aware:** Distinguishes overlap vs unique species dynamics
✅ **Reproducible:** Standardized [0,1] asymmetricity scale with clear interpretation

## 🔬 **Biological Interpretation**

### **Type 1 (Unique Species):**
- **Question:** "Do the parents differ in retaining their unique species?"
- **High asymmetricity:** One parent's unique species are consistently lost
- **Low asymmetricity:** Both parents retain unique species at similar rates
- **Best for:** Detecting competitive exclusion between parent-specific species

### **Type 2 (All Species):**
- **Question:** "Do the parents differ in overall species retention?"
- **High asymmetricity:** One parent dominates community composition
- **Low asymmetricity:** Both parents contribute equally to final community
- **Best for:** Detecting overall community assembly asymmetricity

## 📈 **Integration with Existing Analysis**

The retention-based measures are fully integrated into the existing asymmetricity analysis pipeline:

```python
# Results structure now includes:
results = {
    'similarity_asymmetricity': {...},
    'vector_asymmetricity': {...}, 
    'diversity_asymmetricity_type1': {...},
    'diversity_asymmetricity_type2': {...},
    'retention_asymmetricity': {           # NEW!
        'type1': {...},                    # Exclude overlaps
        'type2': {...}                     # Include overlaps
    }
}
```

## 🎨 **Plotting Capabilities**

1. **Standard box plots** with significance markers (red = significant, gray = not significant)
2. **Side-by-side comparison** of type1 vs type2
3. **Retention vs diversity scatter plots** showing how the new method fixes bias
4. **Species pool size visualization** with color-coded points

## 📝 **Usage Example**

```python
# Import functions
from AsymmetricityAnalysis import (
    calculate_retention_asymmetricity_type1,
    plot_retention_asymmetricity
)

# Calculate retention asymmetricity
result = calculate_retention_asymmetricity_type1(parent1, parent2, mixed)

print(f"Asymmetricity: {result['asymmetricity']:.3f}")
print(f"P-value: {result['p_value']:.3f}")
print(f"Significant: {result['significant']}")

# Plot results across conditions
plot_retention_asymmetricity(results, asymm_type='type1', 
                            save_path='retention_asymmetricity_type1.png')
```

## 🏆 **Scientific Impact**

This implementation transforms asymmetricity analysis from a **descriptive measure** into a **rigorous statistical test** of biological mechanisms. It enables researchers to:

1. **Make valid comparisons** across different diversity levels
2. **Test statistical significance** of observed asymmetricity 
3. **Focus on mechanisms** rather than mathematical artifacts
4. **Publish robust results** with proper statistical controls
5. **Understand biology** behind community coalescence dynamics

The retention-based approach addresses fundamental statistical issues in the field and provides a more scientifically sound framework for analyzing microbial community coalescence.