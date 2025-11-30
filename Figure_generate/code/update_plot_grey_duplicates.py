#!/usr/bin/env python3
"""
Update plotting functions to show duplicated points in grey
"""

import re

# Read the experimental file
with open('generate_fig5_4_mostabundant_experimental.py', 'r') as f:
    content = f.read()

# Pattern 1: For functions that plot directly after duplication (plot_species_vs_community_dominance_combined)
# This pattern already updated, skip

# Pattern 2: For M_H_combined functions that store in dictionary
# Find and update the part where we plot from data_by_medium

# Find the plotting section in M_H_combined functions
plot_section_pattern = r"(# Plot M and H data with separate colors and regression lines\s+for medium in \['M', 'H'\]:\s+x = data_by_medium\[medium\]\['x'\]\s+y = data_by_medium\[medium\]\['y'\]\s+\n\s+# Choose color\s+color = color_M if medium == 'M' else color_H\s+\n\s+# Calculate regression)"

replacement_plot = r"""\1
        x_original = data_by_medium[medium]['x_original']
        y_original = data_by_medium[medium]['y_original']
"""

# Actually, let me just manually add the changes for now
print("This script needs manual implementation - the patterns are too complex.")
print("Please apply changes manually to the M_H_combined plotting sections.")
