#!/usr/bin/env python3
"""
Apply bistability filter to experimental plot functions
This script adds the filter code to functions that don't have it yet
"""

with open('generate_fig5_4_mostabundant_experimental.py', 'r') as f:
    content = f.read()

# The filter code to insert
filter_code = '''
            # FILTER: Exclude bistability cases (both α > 1)
            # Infer from pairwise colony counts: if both species are strongly reduced
            # compared to monoculture, this indicates mutual strong inhibition (both α > 1)
            n1_pair = data_p_1[C1, C2]
            n2_pair = data_p_2[C1, C2]
            n1_mono = mono_means[C1]
            n2_mono = mono_means[C2]

            if not np.isnan(n1_pair) and not np.isnan(n2_pair):
                reduction_1 = 1 - (n1_pair / n1_mono) if n1_mono > 0 else 0
                reduction_2 = 1 - (n2_pair / n2_mono) if n2_mono > 0 else 0

                # If both species reduced > 50%, likely both α > 1 (bistability)
                if reduction_1 > 0.5 and reduction_2 > 0.5:
                    bistability_filtered_count += 1
                    continue

'''

# Initialize code for single medium functions
init_single = '''
    # Get monoculture means for bistability filter
    mono_means = np.mean(Mono_Count_data[medium+'N'], 1)

'''

# Initialize code for M+H combined functions (inside loop)
init_loop = '''
        # Get monoculture means for bistability filter
        mono_means = np.mean(Mono_Count_data[medium+'N'], 1)

'''

# Strategy: Find patterns and insert code

# Pattern 1: For single medium functions - add mono_means after data_p_ratio
# Only if mono_means not already there
if '# Get monoculture means for bistability filter' not in content[:content.find('def plot_species_vs_community_dominance_M_H_combined')]:
    # Already added in first function
    pass

# Pattern 2: For M_H_combined functions - add mono_means inside the loop
# Find occurrences of the for medium in ['M', 'H'] loop
import re

# Function 2: plot_species_vs_community_dominance_M_H_combined
func2_start = content.find('def plot_species_vs_community_dominance_M_H_combined():')
func3_start = content.find('def plot_species_vs_community_dominance_M_H_combined_remove_abundant():')

if func2_start > 0 and func3_start > 0:
    func2_content = content[func2_start:func3_start]

    # Check if mono_means already added
    if 'mono_means = np.mean(Mono_Count_data' not in func2_content:
        # Find where to insert: after data_p_ratio line
        pattern = r"(for medium in \['M', 'H'\]:\n        data_p_1, data_p_2, data_flag, data_p_ratio = getProcessedPairwiseCountData\(Mono_Count_data, Pairwise_Count_data, medium\+'N'\)\n\n)(        data_label)"
        replacement = r"\1" + init_loop + r"\2"
        content = re.sub(pattern, replacement, content, count=1)
        print("Added mono_means to plot_species_vs_community_dominance_M_H_combined")

    # Add bistability counter after data_abspecies
    if 'bistability_filtered_count = 0' not in func2_content:
        pattern2 = r"(        data_label = \[\]\n        data_community = \[\]\n        data_abspecies = \[\]\n\n)(        # Loop through all species pool sizes)"
        replacement2 = r"\1        bistability_filtered_count = 0\n\n\2"
        content = re.sub(pattern2, replacement2, content, count=1)
        print("Added bistability_filtered_count to plot_species_vs_community_dominance_M_H_combined")

    # Add filter code before appending data
    pattern3 = r"(                if data_p_ratio\[C1, C2\] == None:\n                    continue\n)(                else:\n                    data_label\.append)"
    replacement3 = r"\1" + filter_code + r"\2"
    if 'FILTER: Exclude bistability cases' not in content[func2_start:func3_start]:
        content = re.sub(pattern3, replacement3, content, count=1)
        print("Added bistability filter to plot_species_vs_community_dominance_M_H_combined")

# Function 3: plot_species_vs_community_dominance_M_H_combined_remove_abundant
func4_start = content.find('def plot_species_vs_dominant_fraction_M_H_combined():')
if func4_start == -1:
    func4_start = len(content)

if func3_start > 0:
    func3_content = content[func3_start:func4_start]

    # Check if mono_means already added
    if 'mono_means = np.mean(Mono_Count_data' not in func3_content:
        # This function also has for medium in ['M', 'H'] loop
        pattern = r"(def plot_species_vs_community_dominance_M_H_combined_remove_abundant.*?for medium in \['M', 'H'\]:\n        data_p_1, data_p_2, data_flag, data_p_ratio = getProcessedPairwiseCountData\(Mono_Count_data, Pairwise_Count_data, medium\+'N'\)\n\n)(        data_label)"
        replacement = r"\1" + init_loop + r"\2"
        content = re.sub(pattern, replacement, content, count=1, flags=re.DOTALL)
        print("Added mono_means to plot_species_vs_community_dominance_M_H_combined_remove_abundant")

    # Add bistability counter
    if 'bistability_filtered_count = 0' not in func3_content:
        # Find the pattern in this function
        pattern_lines = content[func3_start:func4_start].split('\n')
        for i, line in enumerate(pattern_lines):
            if 'data_abspecies = []' in line:
                # Insert after this line
                insert_idx = func3_start + sum(len(l)+1 for l in pattern_lines[:i+1])
                content = content[:insert_idx] + '        bistability_filtered_count = 0\n' + content[insert_idx:]
                print("Added bistability_filtered_count to plot_species_vs_community_dominance_M_H_combined_remove_abundant")
                break

    # Add filter - similar pattern but may have different spacing
    # Recompute func3_content after previous modifications
    func3_content = content[func3_start:func4_start]
    if 'FILTER: Exclude bistability cases' not in func3_content:
        pattern3 = r"(                if data_p_ratio\[C1, C2\] == None:\n                    continue\n)(                else:\n                    data_label\.append)"
        # Find this pattern in func3 region
        match_start = content.find('if data_p_ratio[C1, C2] == None:', func3_start)
        if match_start > 0 and match_start < func4_start:
            # Find the 'else:' after this
            else_pos = content.find('else:', match_start)
            if else_pos > 0 and else_pos < func4_start:
                # Insert filter_code before 'else:'
                # First find end of 'continue' line
                continue_end = content.find('\n', content.find('continue', match_start)) + 1
                content = content[:continue_end] + filter_code + content[continue_end:]
                print("Added bistability filter to plot_species_vs_community_dominance_M_H_combined_remove_abundant")

# Function 4: plot_species_vs_dominant_fraction_M_H_combined
if func4_start > 0 and func4_start < len(content):
    func4_end = len(content)  # Last function

    func4_content = content[func4_start:func4_end]

    # Similar pattern
    if 'mono_means = np.mean(Mono_Count_data' not in func4_content:
        pattern = r"(def plot_species_vs_dominant_fraction_M_H_combined.*?for medium in \['M', 'H'\]:\n        data_p_1, data_p_2, data_flag, data_p_ratio = getProcessedPairwiseCountData\(Mono_Count_data, Pairwise_Count_data, medium\+'N'\)\n\n)(        data_label)"
        replacement = r"\1" + init_loop + r"\2"
        content = re.sub(pattern, replacement, content, count=1, flags=re.DOTALL)
        print("Added mono_means to plot_species_vs_dominant_fraction_M_H_combined")

    # Add bistability counter
    func4_content = content[func4_start:func4_end]
    if 'bistability_filtered_count = 0' not in func4_content:
        pattern_lines = content[func4_start:func4_end].split('\n')
        for i, line in enumerate(pattern_lines):
            if 'data_abspecies = []' in line:
                insert_idx = func4_start + sum(len(l)+1 for l in pattern_lines[:i+1])
                content = content[:insert_idx] + '        bistability_filtered_count = 0\n' + content[insert_idx:]
                print("Added bistability_filtered_count to plot_species_vs_dominant_fraction_M_H_combined")
                break

    # Add filter
    func4_content = content[func4_start:func4_end]
    if 'FILTER: Exclude bistability cases' not in func4_content:
        match_start = content.find('if data_p_ratio[C1, C2] == None:', func4_start)
        if match_start > 0:
            continue_end = content.find('\n', content.find('continue', match_start)) + 1
            content = content[:continue_end] + filter_code + content[continue_end:]
            print("Added bistability filter to plot_species_vs_dominant_fraction_M_H_combined")

# Write updated file
with open('generate_fig5_4_mostabundant_experimental.py', 'w') as f:
    f.write(content)

print("\nFile updated successfully!")
