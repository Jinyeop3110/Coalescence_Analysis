#!/usr/bin/env python3
"""
Add bistability filter to all experimental plot functions
"""

# Read the file
with open('generate_fig5_4_mostabundant_experimental.py', 'r') as f:
    lines = f.readlines()

# Find lines where we need to add the filter
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    new_lines.append(line)

    # Check if this line contains the condition to filter before appending data
    # Look for: if data_p_ratio[C1, C2] == None:
    #               continue
    #           else:
    #               data_label.append(ii)

    if 'if data_p_ratio[C1, C2] == None:' in line:
        # Add current line
        # Next should be continue
        i += 1
        new_lines.append(lines[i])  # continue line
        i += 1

        # Check if next line already has our filter
        if i < len(lines) and 'FILTER: Exclude bistability cases' in lines[i]:
            # Filter already exists, skip it
            new_lines.append(lines[i])
            i += 1
            continue

        # Add the bistability filter before the else block
        filter_code = """
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

"""
        new_lines.append(filter_code)
        continue

    # Add mono_means initialization after data_p_ratio lines (but only in single-medium functions)
    if ('data_p_1, data_p_2, data_flag, data_p_ratio = getProcessedPairwiseCountData(Mono_Count_data, Pairwise_Count_data, medium+\'N\')' in line and
        i + 1 < len(lines) and 'mono_means' not in lines[i+1]):
        # Check the context - is this inside a loop or at function level?
        # Look back to see indentation
        indent = len(line) - len(line.lstrip())

        # Add mono_means and bistability counter
        i += 1
        new_lines.append(lines[i])  # blank line
        i += 1

        # Check if next lines already have our additions
        if i < len(lines) and 'mono_means' not in lines[i]:
            new_lines.append(' ' * indent + '# Get monoculture means for bistability filter\n')
            new_lines.append(' ' * indent + 'mono_means = np.mean(Mono_Count_data[medium+\'N\'], 1)\n')
            new_lines.append('\n')

        # Check if we need to add bistability_filtered_count
        # Look for data_label initialization
        while i < len(lines) and 'data_label = []' not in lines[i]:
            new_lines.append(lines[i])
            i += 1
        if i < len(lines):
            new_lines.append(lines[i])  # data_label = []
            i += 1
            new_lines.append(lines[i])  # data_community = []
            i += 1
            new_lines.append(lines[i])  # data_abspecies = []
            i += 1

            # Add bistability counter if not exists
            if i < len(lines) and 'bistability_filtered_count' not in lines[i]:
                indent2 = len(lines[i-1]) - len(lines[i-1].lstrip())
                new_lines.append(' ' * indent2 + 'bistability_filtered_count = 0\n')
        continue

    i += 1

# Write the updated file
with open('generate_fig5_4_mostabundant_experimental_updated.py', 'w') as f:
    f.writelines(new_lines)

print("Updated file written to: generate_fig5_4_mostabundant_experimental_updated.py")
print("Please review and then replace the original if correct.")
