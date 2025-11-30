# Assembly Effect Pie Chart Visualizations

## Overview

Pie chart visualizations comparing parent communities (Start All) with their matched coalesced communities (Assembly Effect), showing both replicates.

## Files Generated (6 SVG files)

**Low Nitrogen (LN):**
- `assembly_effect_LN_12_vs_6+6.svg` - 9 designed pairs
- `assembly_effect_LN_24_vs_12+12.svg` - 12 designed pairs

**Medium Nitrogen (MN):**
- `assembly_effect_MN_12_vs_6+6.svg` - 9 designed pairs
- `assembly_effect_MN_24_vs_12+12.svg` - 12 designed pairs

**High Nitrogen (HN):**
- `assembly_effect_HN_12_vs_6+6.svg` - 9 designed pairs
- `assembly_effect_HN_24_vs_12+12.svg` - 12 designed pairs

## Figure Layout

Each figure shows:
- **4 columns**:
  - Columns 1-2: Parent communities (Start All) - Replicate 1 and 2
  - Columns 3-4: Coalesced communities (Assembly Effect) - Replicate 1 and 2
- **One row per designed pair**: Each row compares one parent community with its matched coalesced community
- **Labels**: Community index, sample ID, and final diversity (n=X species)

### Column Organization:
```
| Parent Rep 1 | Parent Rep 2 | Coalesced Rep 1 | Coalesced Rep 2 |
|--------------|--------------|-----------------|-----------------|
| Start All                   | Assembly Effect                   |
```

## Key Features

1. **Both replicates shown**: Each designed pair shows both experimental replicates
2. **Taxonomic colors**: Species colored by phylogeny using the inferno colormap (same as subcommunity plots)
3. **Threshold filtering**: Only ASVs >0.1% relative abundance shown
4. **Normalized abundances**: All pie charts show relative proportions
5. **SVG format only**: Vector graphics for publication quality

## Interpretation

**Horizontal comparison** (left vs right):
- Parent (Start All) vs Coalesced (Assembly Effect)
- Shows compositional differences between direct assembly and coalescence pathway

**Vertical comparison** (within columns):
- Replicate-to-replicate variation
- Reproducibility of community outcomes

## Generation

**Script**: `plot_assembly_effect_pies.py` (in parent directory)
**Data source**: `assembly_pairs_CORRECT.pkl`
**Command**: `python plot_assembly_effect_pies.py`

## Date: 2025-01-04
