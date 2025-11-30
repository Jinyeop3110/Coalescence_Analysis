# Assembly Effect Analysis - Complete Results

## Overview

This analysis identifies **ALL pairs** of communities for quantifying the "assembly effect" - comparing communities assembled directly from a larger species pool versus those formed through coalescence of smaller communities.

## Key Insight

The species composition overlap is a **DATA OUTCOME** to be measured, NOT a selection criterion for pairing communities. We compare ALL parent communities with ALL coalesced communities within the same medium condition.

## Total Pairs Identified: **5,264 pairs**

### Breakdown by Medium and Comparison Type

#### LN Medium (Low Nitrogen)
- **Pool 12 vs 6+6**: 396 pairs
  - 18 parent communities (pool size 12)
  - 28 coalesced communities (from 6+6)
  - 18 × 28 = 504 potential, 396 actual (some missing data)

- **Pool 24 vs 12+12**: 1,296 pairs
  - 24 parent communities (pool size 24)
  - 54 coalesced communities (from 12+12)
  - 24 × 54 = 1,296 pairs

**LN Total: 1,692 pairs**

#### MN Medium (Medium Nitrogen)
- **Pool 12 vs 6+6**: 476 pairs
  - 18 parent communities (pool size 12)
  - 28 coalesced communities (from 6+6)

- **Pool 24 vs 12+12**: 1,296 pairs
  - 24 parent communities (pool size 24)
  - 54 coalesced communities (from 12+12)

**MN Total: 1,772 pairs**

#### HN Medium (High Nitrogen)
- **Pool 12 vs 6+6**: 504 pairs
  - 18 parent communities (pool size 12)
  - 28 coalesced communities (from 6+6)
  - All 18 × 28 = 504 pairs present

- **Pool 24 vs 12+12**: 1,296 pairs
  - 24 parent communities (pool size 24)
  - 54 coalesced communities (from 12+12)

**HN Total: 1,800 pairs**

## Comparison Design

### Pool 12 (Parent) vs 6+6 (Coalesced)

Each pair consists of:
- **Parent**: A directly assembled community with 12-species initial pool
  - Community IDs: 10-18
  - Single communities grown from 12 species

- **Coalesced**: A community formed by merging two 6-species communities
  - Community IDs: 1-14
  - Formed from two sub-communities (Sub1 + Sub2), each with 6-species pool

### Pool 24 (Parent) vs 12+12 (Coalesced)

Each pair consists of:
- **Parent**: A directly assembled community with 24-species initial pool
  - Community IDs: 19-30
  - Single communities grown from 24 species

- **Coalesced**: A community formed by merging two 12-species communities
  - Community IDs: 15-41
  - Formed from two sub-communities (Sub1 + Sub2), each with 12-species pool

## Community Structure

### Parent Communities by Pool Size

#### Pool Size 6
- Community IDs: 1-9
- Used as sub-communities for 6+6 coalescence

#### Pool Size 12
- Community IDs: 10-18
- Used as:
  1. Parent communities for 12 vs 6+6 comparison
  2. Sub-communities for 12+12 coalescence

#### Pool Size 24
- Community IDs: 19-30
- Used as parent communities for 24 vs 12+12 comparison

### Coalesced Communities

#### From 6+6 (total pool ~12)
- Community IDs: 1-14
- Formed from pool-6 sub-communities (IDs 1-9)
- ~2 replicates per coalesced community

#### From 12+12 (total pool ~24)
- Community IDs: 15-41
- Formed from pool-12 sub-communities (IDs 10-18)
- ~2 replicates per coalesced community

## Data Files

### Generated Files

1. **all_assembly_pairs.pkl** (Primary data file)
   - Location: `Figure/Assembly_effect/all_assembly_pairs.pkl`
   - Contains all 5,264 pairs with complete information
   - Includes species composition for parent, coalesced, and sub-communities
   - Includes overlap fractions for reference

2. **comparable_pairs.pkl** (Filtered version - DEPRECATED)
   - Old version with 80% overlap threshold
   - Only 3 unique pairs identified
   - Not recommended for use

### Analysis Scripts

1. **identify_assembly_effect_pairs_corrected.py** (RECOMMENDED)
   - Identifies ALL assembly effect pairs
   - No filtering by species overlap
   - Saves to `all_assembly_pairs.pkl`

2. **identify_assembly_effect_pairs.py** (DEPRECATED)
   - Old version with 80% overlap filter
   - Not recommended

## Data Structure

Each pair contains:

```python
{
    'parent_community_idx': int,           # Community index
    'parent_pool_size': int,                # Initial pool size (12 or 24)
    'parent_sample': str,                   # Sample ID
    'parent_species': list,                 # Species present (ASV indices)
    'parent_num_species': int,              # Number of species present

    'coalesced_community_idx': int,         # Community index
    'coalesced_pool_size': int,             # Each parent pool size (6 or 12)
    'coalesced_sample': str,                # Sample ID
    'coalesced_species': list,              # Species present in coalesced
    'coalesced_num_species': int,           # Number of species present

    'sub1_community_idx': int,              # First parent community
    'sub2_community_idx': int,              # Second parent community
    'sub1_sample': str,                     # Sample ID
    'sub2_sample': str,                     # Sample ID
    'sub1_species': list,                   # Species in sub1
    'sub1_num_species': int,                # Number of species
    'sub2_species': list,                   # Species in sub2
    'sub2_num_species': int,                # Number of species

    'combined_sub_species': list,           # Union of sub1 and sub2 species
    'combined_sub_num_species': int,        # Total unique species
    'species_pool_overlap': list,           # Overlap between parent and combined
    'overlap_fraction': float               # Jaccard similarity
}
```

## Analysis Possibilities

With these 5,264 pairs, you can now:

### 1. Diversity Comparisons
- How does species richness differ between parent and coalesced communities?
- Does the assembly pathway affect final diversity?
- Are there systematic differences by medium?

### 2. Compositional Analysis
- Which species survive in parent vs coalesced communities?
- Are certain species more likely to persist in one pathway?
- Calculate compositional dissimilarity (Bray-Curtis, Jaccard)

### 3. Abundance Patterns
- Do species abundances differ between pathways?
- Is there evenness/dominance structure difference?
- Community stability metrics

### 4. Assembly Effect Quantification
- Define metrics capturing "assembly history effect"
- Statistical testing: are differences significant?
- Medium-dependent effects
- Pool size-dependent effects

### 5. Predictive Analysis
- Can we predict coalesced community from sub-communities?
- Do parent and coalesced converge to similar states?
- Role of priority effects

## Example Usage

```python
import pickle

# Load the pairs
with open('Figure/Assembly_effect/all_assembly_pairs.pkl', 'rb') as f:
    data = pickle.load(f)

# Access pairs for LN medium, pool 24 vs 12+12
ln_24_pairs = data['pairs']['LN']['24_vs_12+12']

# Example: Calculate average diversity difference
parent_diversity = [p['parent_num_species'] for p in ln_24_pairs]
coalesced_diversity = [p['coalesced_num_species'] for p in ln_24_pairs]

# Statistical comparison, visualization, etc.
```

## Key Differences from Previous Version

| Aspect | Old Version | New Version |
|--------|------------|-------------|
| **Filtering** | 80% species overlap required | No filtering |
| **Total pairs** | 3 unique pairs | 5,264 pairs |
| **Approach** | Match by species composition | Compare all within medium |
| **Philosophy** | Overlap is criterion | Overlap is outcome |
| **Coverage** | Very limited | Complete |

## Next Steps

1. **Aggregate analysis across all pairs**
   - Average differences in diversity, composition
   - Distribution of assembly effects

2. **Medium-specific patterns**
   - Does assembly effect vary with nutrient level?

3. **Pool size-specific patterns**
   - Stronger effects for larger pools?

4. **Visualization**
   - Scatter plots: parent vs coalesced diversity
   - Heatmaps: species retention patterns
   - Box plots: assembly effect by condition

5. **Statistical modeling**
   - Mixed-effects models
   - Account for replicate structure
   - Identify significant predictors

## Files Location

- **Main data**: `/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/Assembly_effect/all_assembly_pairs.pkl`
- **Script**: `/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/identify_assembly_effect_pairs_corrected.py`
- **Documentation**: This file

## Citation

When using this analysis, please note:
- Assembly effect quantifies the difference between direct assembly and coalescence
- All comparisons are within-medium to control for environmental conditions
- Species overlap is reported as a measured outcome, not a selection criterion
