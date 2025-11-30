#!/usr/bin/env python3
"""
Add mixing filter (u²+v² > 0.5) to experimental plot functions
"""

with open('generate_fig5_4_mostabundant_experimental.py', 'r') as f:
    content = f.read()

# The filter code to insert (for regular plots - before removing dominant taxa)
filter_code_regular = '''
            # FILTER: Only include mixing events (u²+v² > 0.5)
            mixing_strength = u**2 + v**2
            if mixing_strength <= 0.5:
                continue

'''

# The filter code for AbundantRemoved plot (after removing dominant taxa)
filter_code_removed = '''
                # FILTER: Only include mixing events (u²+v² > 0.5)
                mixing_strength = u**2 + v**2
                if mixing_strength <= 0.5:
                    continue

'''

import re

# Function 1: plot_species_vs_community_dominance_combined
# Add filter after vector_similarity_score calculation
pattern1 = r'(vector_similarity_score = np\.arctan\(u / \(v \+ 1e-8\)\) / \(np\.pi / 2\)\n\n)(            C1 = c_1)'
if re.search(pattern1, content):
    content = re.sub(pattern1, r'\1' + filter_code_regular + r'\2', content, count=1)
    print("Added mixing filter to plot_species_vs_community_dominance_combined")

# Function 2: plot_species_vs_community_dominance_M_H_combined
# Find the second occurrence (in the loop for M and H)
matches = list(re.finditer(r'vector_similarity_score = np\.arctan\(u / \(v \+ 1e-8\)\) / \(np\.pi / 2\)', content))
if len(matches) >= 2:
    pos = matches[1].end()
    # Insert after this line (find the next newline and character pattern)
    insert_pos = content.find('\n\n                C1 = c_1', pos)
    if insert_pos > 0:
        content = content[:insert_pos+2] + filter_code_regular + content[insert_pos+2:]
        print("Added mixing filter to plot_species_vs_community_dominance_M_H_combined")

# Function 3: plot_species_vs_community_dominance_M_H_combined_remove_abundant
# This one has different indentation (8 spaces) and comes after removal
matches = list(re.finditer(r'vector_similarity_score = np\.arctan\(u / \(v \+ 1e-8\)\) / \(np\.pi / 2\)', content))
if len(matches) >= 3:
    pos = matches[2].end()
    # Find the "Skip if vector decomposition..." comment after this
    insert_pos = content.find('\n\n                # Skip if vector decomposition', pos)
    if insert_pos > 0:
        content = content[:insert_pos+2] + filter_code_removed + content[insert_pos+2:]
        print("Added mixing filter to plot_species_vs_community_dominance_M_H_combined_remove_abundant")

# Function 4: plot_species_vs_dominant_fraction_M_H_combined
# Similar to function 2, another M+H combined
matches = list(re.finditer(r'vector_similarity_score = np\.arctan\(u / \(v \+ 1e-8\)\) / \(np\.pi / 2\)', content))
if len(matches) >= 4:
    pos = matches[3].end()
    # Find the next C1 = c_1 pattern
    insert_pos = content.find('\n\n                C1 = c_1', pos)
    if insert_pos > 0:
        content = content[:insert_pos+2] + filter_code_regular + content[insert_pos+2:]
        print("Added mixing filter to plot_species_vs_dominant_fraction_M_H_combined")

# Write updated file
with open('generate_fig5_4_mostabundant_experimental.py', 'w') as f:
    f.write(content)

print("\n✓ Mixing filter (u²+v² > 0.5) added to all experimental plot functions!")
print("Now regenerating plots...")
