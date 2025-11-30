# Color Usage Guidelines for Coalescence Analysis Scripts

## Overview
This document outlines the standardized color usage rules for all scripts in the coalescence analysis project. Colors are centralized in `COLORMAP.py` to ensure consistency across all visualizations.

## Core Color Scheme

### Primary Colors (Nutrient Conditions)
- **LN (Low Nitrogen)**: `#A7216A` - Rich magenta-purple
- **MN (Medium Nitrogen)**: `#802000` - Dark brown-red  
- **HN (High Nitrogen)**: `#E24912` - Deep orange-red

These colors provide good contrast, are colorblind-friendly, and represent the nutrient gradient from low to high.

## Usage Rules

### 1. Import and Usage Pattern
```python
# Recommended import pattern
from COLORMAP import get_medium_colors, map_medium_to_index, get_medium_color

# For scripts using color arrays
colors = get_medium_colors()  # Returns [LN, MN, HN] colors
c_i = map_medium_to_index(medium)  # Convert 'L'/'LN' to index 0, etc.

# For scripts needing single colors
color = get_medium_color('L')  # Returns '#A7216A'

# For scripts using dictionary access
from COLORMAP import MEDIUM_COLORS
color = MEDIUM_COLORS['LN']
```

### 2. Mandatory Updates
When creating or modifying scripts, **ALWAYS**:
- Replace hardcoded color values with COLORMAP imports
- Use consistent medium-to-color mapping (L/LN→0, M/MN→1, H/HN→2)
- Import COLORMAP at the function level to avoid global imports

### 3. Script-Specific Guidelines

#### Vector Decomposition Scripts
- Use `get_medium_colors()` for the main color array
- Maintain existing plot structure but replace color definitions

#### Abundance/Correlation Scripts  
- Replace `sns.color_palette("tab10")` indices with COLORMAP equivalents
- Use `map_medium_to_index()` for medium-to-index conversion

#### Asymmetricity Analysis Scripts
- Replace condition-specific color dictionaries with MEDIUM_COLORS
- Maintain condition-based color mapping structure

## File-by-File Status

### ✅ Updated Files
- `COLORMAP.py` - Central color definitions
- `vector_decomp_experimental.py` - Updated to use COLORMAP
- `vector_decomp_simulation.py` - Updated to use COLORMAP  
- `vector_decomp_natural.py` - Updated to use COLORMAP
- `generate_fig5_4_mostabundant_experimental.py` - Updated to use COLORMAP
- `AsymmetricityNullModelAnalysis.py` - Updated to use COLORMAP

### ⏭️ Files Not Updated (Different Color Schemes)
- `generate_fig5_4_mostabundant_simulation.py` - Uses different colors (skyblue, gray, etc.)
- `AsymmetricityNullModelAnalysis_prev.py` - No colors found needing update

## Color Mapping Reference

### Old vs New Color Mapping
```python
# OLD (inconsistent across scripts)
colors = [sns.color_palette("tab10")[2], sns.color_palette("tab10")[0], sns.color_palette("tab10")[3]]
# OR
colors = ['#A7216A', '#802000', '#E24912']
# OR  
condition_colors = {'LN': '#28a745', 'MN': '#007bff', 'HN': '#dc3545'}

# NEW (consistent)
from COLORMAP import get_medium_colors, MEDIUM_COLORS
colors = get_medium_colors()  # [LN, MN, HN] order
condition_colors = {'LN': MEDIUM_COLORS['LN'], 'MN': MEDIUM_COLORS['MN'], 'HN': MEDIUM_COLORS['HN']}
```

### Index Mapping
- Index 0: L/LN (Low Nitrogen) → `#A7216A`
- Index 1: M/MN (Medium Nitrogen) → `#802000`  
- Index 2: H/HN (High Nitrogen) → `#E24912`

## Best Practices

### DO:
- ✅ Import COLORMAP functions at the function level  
- ✅ Use descriptive variable names (`medium_colors`, `condition_colors`)
- ✅ Test color mapping with different medium inputs ('L', 'LN', 'M', 'MN', 'H', 'HN')
- ✅ Document any script-specific color usage in comments

### DON'T:
- ❌ Hardcode hex color values directly in scripts
- ❌ Use different color schemes for the same nutrient conditions
- ❌ Modify COLORMAP.py without updating this documentation
- ❌ Import COLORMAP globally if only used in specific functions

## Future Extensions

### Adding New Color Schemes
If additional color schemes are needed:
1. Add them to `COLORMAP.py` as new dictionaries/functions
2. Update this documentation with usage examples
3. Maintain backward compatibility with existing scripts

### Validation
Before committing changes:
1. Run all updated scripts to ensure colors display correctly
2. Verify consistency across different plot types
3. Check that all medium identifiers ('L', 'LN', etc.) work properly

## Quick Migration Checklist

When updating a script:
- [ ] Identify all hardcoded color definitions
- [ ] Replace with appropriate COLORMAP imports  
- [ ] Update medium-to-index mapping logic
- [ ] Test with all nutrient conditions (L, M, H)
- [ ] Verify visual consistency with other scripts
- [ ] Update script documentation if needed

---

**Last Updated**: August 2025  
**Maintainer**: Coalescence Analysis Team