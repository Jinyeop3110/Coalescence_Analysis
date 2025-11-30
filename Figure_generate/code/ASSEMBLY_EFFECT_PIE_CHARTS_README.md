# Assembly Effect Pie Chart Visualizations

## Overview

Pie chart visualizations comparing parent communities (start all) with their matched coalesced communities (assembly effect).

## Pipeline

The visualization pipeline follows the same structure as the `Figure/PieCharts/Subcommunities/` pipeline:
- Uses the same taxonomic colormap and sorting
- Similar plot structure and layout
- Consistent pie chart rendering

## Generated Files

### 6 Visualization Files (PNG + SVG for each):

**Low Nitrogen (LN):**
- `assembly_effect_LN_12_vs_6+6.png/svg` - 9 pairs comparing parent pool-12 vs coalesced from 6+6
- `assembly_effect_LN_24_vs_12+12.png/svg` - 12 pairs comparing parent pool-24 vs coalesced from 12+12

**Medium Nitrogen (MN):**
- `assembly_effect_MN_12_vs_6+6.png/svg` - 9 pairs comparing parent pool-12 vs coalesced from 6+6
- `assembly_effect_MN_24_vs_12+12.png/svg` - 12 pairs comparing parent pool-24 vs coalesced from 12+12

**High Nitrogen (HN):**
- `assembly_effect_HN_12_vs_6+6.png/svg` - 9 pairs comparing parent pool-12 vs coalesced from 6+6
- `assembly_effect_HN_24_vs_12+12.png/svg` - 12 pairs comparing parent pool-24 vs coalesced from 12+12

## Figure Layout

Each figure shows:
- **Left column**: Parent communities (Start All) - directly assembled from initial pool
- **Right column**: Coalesced communities (Assembly Effect) - formed by merging two smaller communities
- **One row per designed pair**: Each row compares one parent with its matched coalesced community
- **Title shows**: Community index, sample ID, and final diversity (n=X species)

## Key Features

1. **Taxonomic colors**: Species are colored by phylogeny using the inferno colormap
2. **Threshold filtering**: Only ASVs >0.1% relative abundance are shown
3. **Normalized abundances**: All pie charts show relative proportions
4. **Sample information**: Each pie shows the sample ID and species count

## Interpretation

Compare left vs right columns to see:
- **Species composition differences**: Which species are present/absent
- **Abundance distribution**: How evenly/unevenly species are distributed
- **Diversity changes**: Species count differences (shown in titles)
- **Community structure**: Overall patterns between direct assembly vs coalescence

## Usage Example

```python
# To regenerate all pie charts
python plot_assembly_effect_pies.py

# To load and analyze the data
import pickle
with open('Figure/Assembly_effect/assembly_pairs_CORRECT.pkl', 'rb') as f:
    data = pickle.load(f)

# Access specific pairs
ln_pairs = data['pairs']['LN']['12_vs_6+6']
```

## Files

**Script**: `plot_assembly_effect_pies.py`
**Output directory**: `Figure/Assembly_effect/`
**Data source**: `Figure/Assembly_effect/assembly_pairs_CORRECT.pkl`

## Technical Notes

- Uses same colormap as subcommunity plots for consistency
- Handles both replicates (shows first replicate in visualization)
- Automatically creates output directory if it doesn't exist
- Saves both PNG (for viewing) and SVG (for editing) formats

## Date: 2025-01-04
