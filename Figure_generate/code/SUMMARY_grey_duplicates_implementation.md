# Implementation Summary: Grey Duplicated Points

## Goal:
Show duplicated points (reflected across diagonal) as **grey transparent dots** while keeping them in regression calculations.

## Status:

### ✅ COMPLETED:
1. **`plot_species_vs_community_dominance_combined()`** (L, M, H individual plots)
   - Lines 319-350 updated
   - Original points: Colored with alpha=0.5
   - Duplicated points: Grey with alpha=0.2
   - Regression uses ALL points (original + duplicated)

### ⏳ TODO - Experimental Plots:
2. **`plot_species_vs_community_dominance_M_H_combined()`** - NOT YET UPDATED
3. **`plot_species_vs_community_dominance_M_H_combined_remove_abundant()`** - NOT YET UPDATED
4. **`plot_species_vs_dominant_fraction_M_H_combined()`** - NOT YET UPDATED

### ⏳ TODO - Simulation Plots:
5. **`plot_20reps_correlation.py`** - NOT YET UPDATED
6. **`plot_narrow_uniform_correlation.py`** - NOT YET UPDATED

## Implementation Pattern:

### For Single-Medium Functions (L, M, H):

```python
# Store original before duplication
x_original = x.copy()
y_original = y.copy()

# Duplicate for symmetry
x = np.concatenate((x, 1-x))
y = np.concatenate((y, 1-y))

# Calculate regression with ALL points
slope, intercept = np.polyfit(x, y, 1)
r_squared = ...

# Plot duplicated points first (grey, behind)
x_duplicated = 1 - x_original
y_duplicated = 1 - y_original
plt.scatter(x_duplicated, y_duplicated, color='grey', s=4, alpha=0.2, zorder=1)

# Plot original points on top (colored)
plt.scatter(x_original, y_original, color=colors[c_i], s=4, alpha=0.5, zorder=2)
```

### For M_H_Combined Functions:

```python
# Inside the loop for medium in ['M', 'H']:
# Store original before duplication
x_original = x.copy()
y_original = y.copy()

# Duplicate
x = np.concatenate((x, 1-x))
y = np.concatenate((y, 1-y))

# Store in dictionary with originals
data_by_medium[medium] = {
    'x': x, 'y': y,
    'x_original': x_original,
    'y_original': y_original
}

# Later in plotting section:
for medium in ['M', 'H']:
    x = data_by_medium[medium]['x']
    y = data_by_medium[medium]['y']
    x_original = data_by_medium[medium]['x_original']
    y_original = data_by_medium[medium]['y_original']

    # Calculate regression with ALL points
    slope, intercept = np.polyfit(x, y, 1)

    # Plot duplicated (grey)
    x_dup = 1 - x_original
    y_dup = 1 - y_original
    plt.scatter(x_dup, y_dup, color='grey', s=4, alpha=0.2, zorder=1)

    # Plot original (colored)
    plt.scatter(x_original, y_original, color=color, s=4, alpha=0.5, zorder=2)
```

### For Simulation Subplot Functions:

```python
# Store original before duplication
x_original = x.copy()
y_original = y.copy()

# Duplicate data points
x = np.concatenate((x, 1-x))
y = np.concatenate((y, 1-y))

# Calculate regression with ALL points
slope, intercept = np.polyfit(x, y, 1)

# Plot duplicated (grey)
x_dup = 1 - x_original
y_dup = 1 - y_original
ax.scatter(x_dup, y_dup, color='grey', s=10, alpha=0.2, zorder=1)

# Plot original (colored)
ax.scatter(x_original, y_original, color=colors[plot_idx], s=10, alpha=0.5, zorder=2)
```

## Key Points:

1. **Regression always uses ALL points** (original + duplicated) - no change to statistics
2. **Visual distinction**: Original=colored, Duplicated=grey
3. **Layering**: Duplicated behind (zorder=1), Original on top (zorder=2)
4. **Alpha values**: Duplicated=0.2 (more transparent), Original=0.5
5. **Symmetry preserved**: x_dup = 1 - x_orig, y_dup = 1 - y_orig

## Why This Matters:

- **Clarity**: Makes it obvious which points are real measurements vs reflections
- **Honesty**: Shows that half the points are mathematically derived, not independent data
- **Aesthetics**: Grey background points don't dominate the visualization
- **Statistics**: Regression still uses all points for consistency with previous analysis

## Files to Update:

- [x] `generate_fig5_4_mostabundant_experimental.py` - Function 1 done, 3 more to go
- [ ] `plot_20reps_correlation.py`
- [ ] `plot_narrow_uniform_correlation.py`
