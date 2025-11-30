#!/usr/bin/env python3
"""
Revert the bistability filter from experimental plot functions
"""

with open('generate_fig5_4_mostabundant_experimental.py', 'r') as f:
    lines = f.readlines()

new_lines = []
i = 0
skip_until_else = False

while i < len(lines):
    line = lines[i]

    # Remove mono_means lines
    if 'Get monoculture means for bistability filter' in line:
        # Skip this comment and the next line (mono_means = ...)
        i += 1  # skip comment
        i += 1  # skip mono_means line
        i += 1  # skip blank line after it
        continue

    # Remove bistability_filtered_count initialization
    if 'bistability_filtered_count = 0' in line:
        i += 1
        continue

    # Remove the entire filter block
    if 'FILTER: Exclude bistability cases' in line:
        # Skip all lines until we hit the data_label.append line
        # The filter block is about 15 lines
        while i < len(lines) and 'data_label.append' not in lines[i]:
            i += 1
        continue

    # Remove print statement about filtered cases
    if 'Filtered' in line and 'bistability cases' in line:
        i += 1
        continue

    new_lines.append(line)
    i += 1

# Write the reverted file
with open('generate_fig5_4_mostabundant_experimental.py', 'w') as f:
    f.writelines(new_lines)

print("Bistability filter reverted successfully!")
print("All mono_means, bistability_filtered_count, and filter blocks removed.")
