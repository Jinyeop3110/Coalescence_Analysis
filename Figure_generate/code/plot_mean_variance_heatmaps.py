"""
Generate 2D heatmaps for mean×variance grid showing coalescence outcome fractions

Creates three heatmaps:
1. Dominance fraction
2. Mixing fraction
3. Restructuring fraction

Each heatmap shows the fraction of coalescence events resulting in that outcome
as a function of mean interaction strength (x-axis) and std (y-axis).
"""

import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_setup import (
    metric_VectorDecomposition_onlyPositive,
    calculate_assymetricity,
    characterize_case
)

# Input file
data_dir = "Simulation_Data/mean_std_grid_100reps"
data_file = os.path.join(data_dir, "Community_mean_std_grid_100reps.json")

# Output directory
output_dir = "Figure/PhaseDiagram_mean_variance"
os.makedirs(output_dir, exist_ok=True)

# Grid parameters (must match run_mean_std_grid.py)
mean_values = np.arange(0.1, 1.21, 0.1)  # 0.1, 0.2, ..., 1.2 (12 values)
std_values = np.arange(0.1, 0.61, 0.1)   # 0.1, 0.2, ..., 0.6 (6 values)

print("="*70)
print("GENERATING MEAN×VARIANCE HEATMAPS")
print("="*70)
print(f"\nLoading data from: {data_file}")

# Load simulation data
with open(data_file, 'r') as f:
    data = json.load(f)

print(f"✓ Data loaded successfully")
print(f"  Grid: {len(mean_values)} means × {len(std_values)} stds = {len(mean_values) * len(std_values)} combinations")

# Initialize outcome counts for each (mean, std) combination
# Grid: rows = std values, columns = mean values
dominance_count = np.zeros((len(std_values), len(mean_values)))
mixing_count = np.zeros((len(std_values), len(mean_values)))
restructuring_count = np.zeros((len(std_values), len(mean_values)))
total_count = np.zeros((len(std_values), len(mean_values)))

# Process each (mean, std) combination
print("\nProcessing coalescence outcomes...")
total_coalescence_events = 0
processed_combinations = 0

for mean_idx, mean in enumerate(mean_values):
    for std_idx, std in enumerate(std_values):
        key = f"mean{mean:.2f}_std{std:.2f}"

        if key not in data:
            print(f"  Warning: Missing data for {key}")
            continue

        processed_combinations += 1

        # Process all reps for this (mean, std) combination
        for rep_key, rep_data in data[key].items():
            if not rep_key.startswith('rep_'):
                continue

            sc_list = rep_data['sc_list']
            cc_list = rep_data['cc_list']

            # Process all coalescence events for this rep
            for cc_key, cc_final in cc_list.items():
                # Parse community indices from key like "c1_c2"
                parts = cc_key.split('_')
                c1_key = parts[0]  # e.g., "c1"
                c2_key = parts[1]  # e.g., "c2"

                c1_final = sc_list[c1_key]
                c2_final = sc_list[c2_key]

                # Calculate outcome using vector decomposition
                try:
                    u, v, k = metric_VectorDecomposition_onlyPositive(
                        c1_final, c2_final, cc_final
                    )

                    # Transform to asymmetricity coordinates
                    x, y = calculate_assymetricity(u, v, k)

                    # Classify using old asymmetricity-based boundaries
                    # - Dominance: x² > 0.5 AND y > 0.5
                    # - Mixing: x² > 0.5 AND y < 0.5
                    # - Restructuring: x² < 0.5
                    outcome_class = characterize_case(x, y)

                    if outcome_class == 0:
                        dominance_count[std_idx, mean_idx] += 1
                    elif outcome_class == 1:
                        mixing_count[std_idx, mean_idx] += 1
                    elif outcome_class == 2:
                        restructuring_count[std_idx, mean_idx] += 1

                    total_count[std_idx, mean_idx] += 1
                    total_coalescence_events += 1

                except Exception as e:
                    # Skip if vector decomposition fails
                    pass

print(f"✓ Processed {processed_combinations} combinations")
print(f"✓ Total coalescence events: {total_coalescence_events}")

# Calculate fractions
dominance_fraction = np.divide(dominance_count, total_count,
                               out=np.zeros_like(dominance_count),
                               where=total_count>0)
mixing_fraction = np.divide(mixing_count, total_count,
                           out=np.zeros_like(mixing_count),
                           where=total_count>0)
restructuring_fraction = np.divide(restructuring_count, total_count,
                                   out=np.zeros_like(restructuring_count),
                                   where=total_count>0)

# Verify fractions sum to 1
fraction_sum = dominance_fraction + mixing_fraction + restructuring_fraction
print(f"\n✓ Fraction sum check: min={fraction_sum.min():.3f}, max={fraction_sum.max():.3f} (should be ~1.0)")

# Print data ranges for each outcome type
print(f"\n✓ Data ranges:")
print(f"  Dominance: min={dominance_fraction.min():.3f}, max={dominance_fraction.max():.3f}")
print(f"  Mixing: min={mixing_fraction.min():.3f}, max={mixing_fraction.max():.3f}")
print(f"  Restructuring: min={restructuring_fraction.min():.3f}, max={restructuring_fraction.max():.3f}")

# Create custom colormaps
# For each outcome type, we'll use a different color scheme
cmap_dominance = LinearSegmentedColormap.from_list('dominance', ['white', 'darkred'])
cmap_mixing = LinearSegmentedColormap.from_list('mixing', ['white', 'purple'])
cmap_restructuring = LinearSegmentedColormap.from_list('restructuring', ['white', 'darkgreen'])

# Plot settings
fig_width = 8
fig_height = 6
fontsize_title = 14
fontsize_labels = 12
fontsize_ticks = 10

# ===== HEATMAP 1: DOMINANCE =====
print("\nGenerating dominance heatmap (auto-scaled)...")
fig, ax = plt.subplots(figsize=(fig_width, fig_height))

# Auto-scale: use actual data range instead of [0, 1]
vmin_dom = dominance_fraction.min()
vmax_dom = dominance_fraction.max()

im = ax.imshow(dominance_fraction, aspect='auto', origin='lower',
               cmap=cmap_dominance, vmin=vmin_dom, vmax=vmax_dom,
               extent=[mean_values[0]-0.05, mean_values[-1]+0.05,
                      std_values[0]-0.05, std_values[-1]+0.05])

ax.set_xlabel('Mean Interaction Strength', fontsize=fontsize_labels)
ax.set_ylabel('Std Interaction Strength', fontsize=fontsize_labels)
ax.set_title(f'Dominance Fraction (range: {vmin_dom:.3f}-{vmax_dom:.3f})',
            fontsize=fontsize_title, fontweight='bold')

# Add colorbar
cbar = plt.colorbar(im, ax=ax)
cbar.set_label('Fraction', fontsize=fontsize_labels)

# Add grid
ax.grid(True, alpha=0.3, linewidth=0.5)

plt.tight_layout()
output_file = os.path.join(output_dir, "heatmap_dominance.svg")
plt.savefig(output_file, dpi=300, bbox_inches='tight')
plt.savefig(output_file.replace('.svg', '.png'), dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_file}")
plt.close()

# ===== HEATMAP 2: MIXING =====
print("Generating mixing heatmap (auto-scaled)...")
fig, ax = plt.subplots(figsize=(fig_width, fig_height))

# Auto-scale: use actual data range instead of [0, 1]
vmin_mix = mixing_fraction.min()
vmax_mix = mixing_fraction.max()

im = ax.imshow(mixing_fraction, aspect='auto', origin='lower',
               cmap=cmap_mixing, vmin=vmin_mix, vmax=vmax_mix,
               extent=[mean_values[0]-0.05, mean_values[-1]+0.05,
                      std_values[0]-0.05, std_values[-1]+0.05])

ax.set_xlabel('Mean Interaction Strength', fontsize=fontsize_labels)
ax.set_ylabel('Std Interaction Strength', fontsize=fontsize_labels)
ax.set_title(f'Mixing Fraction (range: {vmin_mix:.3f}-{vmax_mix:.3f})',
            fontsize=fontsize_title, fontweight='bold')

# Add colorbar
cbar = plt.colorbar(im, ax=ax)
cbar.set_label('Fraction', fontsize=fontsize_labels)

# Add grid
ax.grid(True, alpha=0.3, linewidth=0.5)

plt.tight_layout()
output_file = os.path.join(output_dir, "heatmap_mixing.svg")
plt.savefig(output_file, dpi=300, bbox_inches='tight')
plt.savefig(output_file.replace('.svg', '.png'), dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_file}")
plt.close()

# ===== HEATMAP 3: RESTRUCTURING =====
print("Generating restructuring heatmap (auto-scaled)...")
fig, ax = plt.subplots(figsize=(fig_width, fig_height))

# Auto-scale: use actual data range instead of [0, 1]
vmin_res = restructuring_fraction.min()
vmax_res = restructuring_fraction.max()

im = ax.imshow(restructuring_fraction, aspect='auto', origin='lower',
               cmap=cmap_restructuring, vmin=vmin_res, vmax=vmax_res,
               extent=[mean_values[0]-0.05, mean_values[-1]+0.05,
                      std_values[0]-0.05, std_values[-1]+0.05])

ax.set_xlabel('Mean Interaction Strength', fontsize=fontsize_labels)
ax.set_ylabel('Std Interaction Strength', fontsize=fontsize_labels)
ax.set_title(f'Restructuring Fraction (range: {vmin_res:.3f}-{vmax_res:.3f})',
            fontsize=fontsize_title, fontweight='bold')

# Add colorbar
cbar = plt.colorbar(im, ax=ax)
cbar.set_label('Fraction', fontsize=fontsize_labels)

# Add grid
ax.grid(True, alpha=0.3, linewidth=0.5)

plt.tight_layout()
output_file = os.path.join(output_dir, "heatmap_restructuring.svg")
plt.savefig(output_file, dpi=300, bbox_inches='tight')
plt.savefig(output_file.replace('.svg', '.png'), dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_file}")
plt.close()

# ===== COMBINED 3-PANEL PLOT =====
print("Generating combined 3-panel heatmap (auto-scaled)...")
fig, axes = plt.subplots(1, 3, figsize=(20, 6))

# Panel 1: Dominance (auto-scaled)
im1 = axes[0].imshow(dominance_fraction, aspect='auto', origin='lower',
                     cmap=cmap_dominance, vmin=vmin_dom, vmax=vmax_dom,
                     extent=[mean_values[0]-0.05, mean_values[-1]+0.05,
                            std_values[0]-0.05, std_values[-1]+0.05])
axes[0].set_xlabel('Mean Interaction Strength', fontsize=fontsize_labels)
axes[0].set_ylabel('Std Interaction Strength', fontsize=fontsize_labels)
axes[0].set_title(f'Dominance\n[{vmin_dom:.3f}-{vmax_dom:.3f}]',
                 fontsize=fontsize_title, fontweight='bold')
axes[0].grid(True, alpha=0.3, linewidth=0.5)
cbar1 = plt.colorbar(im1, ax=axes[0])
cbar1.set_label('Fraction', fontsize=fontsize_labels)

# Panel 2: Mixing (auto-scaled)
im2 = axes[1].imshow(mixing_fraction, aspect='auto', origin='lower',
                     cmap=cmap_mixing, vmin=vmin_mix, vmax=vmax_mix,
                     extent=[mean_values[0]-0.05, mean_values[-1]+0.05,
                            std_values[0]-0.05, std_values[-1]+0.05])
axes[1].set_xlabel('Mean Interaction Strength', fontsize=fontsize_labels)
axes[1].set_ylabel('Std Interaction Strength', fontsize=fontsize_labels)
axes[1].set_title(f'Mixing\n[{vmin_mix:.3f}-{vmax_mix:.3f}]',
                 fontsize=fontsize_title, fontweight='bold')
axes[1].grid(True, alpha=0.3, linewidth=0.5)
cbar2 = plt.colorbar(im2, ax=axes[1])
cbar2.set_label('Fraction', fontsize=fontsize_labels)

# Panel 3: Restructuring (auto-scaled)
im3 = axes[2].imshow(restructuring_fraction, aspect='auto', origin='lower',
                     cmap=cmap_restructuring, vmin=vmin_res, vmax=vmax_res,
                     extent=[mean_values[0]-0.05, mean_values[-1]+0.05,
                            std_values[0]-0.05, std_values[-1]+0.05])
axes[2].set_xlabel('Mean Interaction Strength', fontsize=fontsize_labels)
axes[2].set_ylabel('Std Interaction Strength', fontsize=fontsize_labels)
axes[2].set_title(f'Restructuring\n[{vmin_res:.3f}-{vmax_res:.3f}]',
                 fontsize=fontsize_title, fontweight='bold')
axes[2].grid(True, alpha=0.3, linewidth=0.5)
cbar3 = plt.colorbar(im3, ax=axes[2])
cbar3.set_label('Fraction', fontsize=fontsize_labels)

plt.tight_layout()
output_file = os.path.join(output_dir, "heatmap_combined_3panel.svg")
plt.savefig(output_file, dpi=300, bbox_inches='tight')
plt.savefig(output_file.replace('.svg', '.png'), dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_file}")
plt.close()

print("\n" + "="*70)
print("HEATMAP GENERATION COMPLETE!")
print("="*70)
print(f"Output directory: {output_dir}")
print(f"\nGenerated files:")
print(f"  • heatmap_dominance.svg/.png")
print(f"  • heatmap_mixing.svg/.png")
print(f"  • heatmap_restructuring.svg/.png")
print(f"  • heatmap_combined_3panel.svg/.png")
print("="*70)
