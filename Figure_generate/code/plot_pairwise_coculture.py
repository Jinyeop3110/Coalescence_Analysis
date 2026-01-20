"""
Plot_pairwiseCoCulture.py

Purpose: Analyzes pairwise co-culture interactions under different nutrient conditions (LN, MN, HN)
Key features:
- Categorizes interaction outcomes as Coexistence (C), Exclusion (E), Bistability (B), or Unclassified (U)
- Creates stacked bar charts showing fraction of each outcome type
- Calculates and plots the fraction of exclusions (α > 1) with error bars
- Uses custom color schemes for visualization

Saving paths:
- '../figure/PairwiseInteraction_Errorbarplot.svg'
"""

from common_setup import *

def main():
    # Define data
    LN_case_list = ['C', 'C', 'C', 'C', 'C', 'C', 'C', 'U', 'U', 'C', 'C', 'C', 'C',
                    'C', 'U', 'C', 'C', 'U', 'E', 'C', 'C', 'C', 'C', 'C', 'C', 'C',
                    'C', 'C', 'C', 'C', 'C', 'C', 'C', 'U', 'C', 'C', 'C', 'C', 'C',
                    'C', 'C', 'C', 'C', 'C', 'U', 'C', 'C', 'C', 'C', 'U', 'U', 'C',
                    'C', 'U', 'C', 'C', 'C', 'C', 'C', 'E', 'C']
    MN_case_list = ['U', 'E', 'U', 'E', 'E', 'E', 'U', 'U', 'C', 'E', 'E', 'U', 'C',
                    'E', 'E', 'E', 'B', 'C', 'E', 'C', 'E', 'E', 'E', 'E', 'E', 'E',
                    'E', 'E', 'C', 'C', 'C', 'E', 'B', 'U', 'E', 'C', 'U', 'E', 'C',
                    'C', 'E', 'C', 'E', 'C', 'C', 'E', 'C', 'E', 'C', 'C', 'E', 'C',
                    'C', 'U', 'U', 'C', 'C', 'B', 'E', 'U', 'E']
    HN_case_list = ['E', 'E', 'E', 'E', 'E', 'B', 'E', 'U', 'U', 'E', 'E', 'E', 'U',
                    'B', 'E', 'E', 'B', 'C', 'B', 'C', 'E', 'E', 'E', 'E', 'E', 'B',
                    'E', 'E', 'U', 'U', 'E', 'E', 'E', 'C', 'E', 'C', 'U', 'U', 'U',
                    'C', 'E', 'B', 'B', 'U', 'C', 'E', 'C', 'E', 'C', 'C', 'E', 'E',
                    'U', 'U', 'E', 'E', 'C', 'B', 'E', 'E', 'E']

    # Count occurrences and calculate fractions
    def get_fractions(case_list):
        counts = {key: case_list.count(key) for key in ['C', 'U', 'E', 'B']}
        total = len(case_list)
        return {key: counts[key] / total for key in counts}

    LN_fractions = get_fractions(LN_case_list)
    MN_fractions = get_fractions(MN_case_list)
    HN_fractions = get_fractions(HN_case_list)

    # DataFrame to print table
    df = pd.DataFrame([LN_fractions, MN_fractions, HN_fractions], index=['LN', 'MN', 'HN'])
    categories = ['LN', 'MN', 'HN']
    colors_local = ['#FFC3C3', '#B3C9FF', '#C3FFC3', '#CCCCCC']  # more gentle and visible colors

    bottoms = [0, 0, 0]
    labels = ['Coexistence', 'Exclusion', 'Bistability', 'Unclassified']
    fractions = ['C', 'E', 'B', 'U']

    # Create stacked bar chart
    fig, ax = plt.subplots(figsize=(5, 4))

    bottoms = [0, 0, 0]

    for frac, color, label in zip(fractions, colors_local, labels):
        heights = [LN_fractions[frac], MN_fractions[frac], HN_fractions[frac]]
        bars = ax.bar(categories, heights, bottom=bottoms, color=color, label=label, edgecolor='none')

        # Add text labels
        for bar in bars:
            height = bar.get_height()
            if height > 0.05:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + height / 2, f'{height:.2f}', 
                        ha='center', va='center', fontsize=9)

        # Update bottom for stacking
        bottoms = [bottom + height for bottom, height in zip(bottoms, heights)]

    # Axis labels
    ax.set_ylim(0, 1)
    ax.set_xlabel('Conditions')
    ax.set_ylabel('Fraction')

    # Move legend to upper position
    ax.legend(title='Cases', loc='lower center', 
              bbox_to_anchor=(0.5, 1.02), ncol=4)

    plt.tight_layout()
    fig.savefig('Figure/PairwiseInteraction/PairwiseInteraction_StackedBar.svg', bbox_inches='tight')
    plt.show()

    # Create error bar plot for exclusion ratio
    def convert_to_exc_ratio(case_list):
        # Convert the cases to their respective numbers (excluding 'U')
        num_list = [0 if case == 'C' else 0.5 if case == 'E' else 1 if case == 'B' else None for case in case_list]
        
        # Remove None values (which correspond to 'U' cases)
        num_list = [num for num in num_list if num is not None]
        
        # Return the count of each number
        return num_list

    # Get the counts for each condition
    LN_I_mean = np.mean(convert_to_exc_ratio(LN_case_list))
    LN_I_mean_var = np.var(convert_to_exc_ratio(LN_case_list))/len(convert_to_exc_ratio(LN_case_list))

    MN_I_mean = np.mean(convert_to_exc_ratio(MN_case_list))
    MN_I_mean_var = np.var(convert_to_exc_ratio(MN_case_list)) / len(convert_to_exc_ratio(MN_case_list))

    HN_I_mean = np.mean(convert_to_exc_ratio(HN_case_list))
    HN_I_mean_var = np.var(convert_to_exc_ratio(HN_case_list)) / len(convert_to_exc_ratio(HN_case_list))

    means = [LN_I_mean, MN_I_mean, HN_I_mean]
    mean_vars = [LN_I_mean_var, MN_I_mean_var, HN_I_mean_var]

    # Create a list of x positions for the groups
    groups = ['LN', 'MN', 'HN']
    x_pos = range(len(groups))

    # Set up the figure
    fig, axs = plt.subplots(1, figsize=(45*mm,45*mm))

    # Plot scatter plot with error bars for the means
    for i, c in enumerate(colors):
        plt.errorbar(x_pos[i], means[i], yerr=np.sqrt(mean_vars)[i], fmt='o', color=c, capsize=3, markersize=5, label=groups[i], alpha=1)
    plt.plot(x_pos, means,color='black', alpha=0.5)
    plt.xlim(-0.3,2.3)
    # Add labels and title
    plt.xticks(x_pos, groups)
    plt.xlabel(' ')
    plt.ylabel(r'Fraction of $\alpha >1$')
    plt.title('Frequency of Exclusions')

    # Add labels and legend
    plt.ylim([0,0.6])

    # Save the plot
    fig.savefig('Figure/PairwiseInteraction/PairwiseInteraction_Errorbarplot.svg', bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    main()