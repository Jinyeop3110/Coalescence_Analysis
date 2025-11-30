"""
Sample Lists Organized by Condition
All samples for 12-species pool experiments, organized by medium (LN/MN/HN) and type (Subcommunity/Coalescence)
"""

# ============================================================================
# LN (Low Nitrogen) - 12 Species Pool
# ============================================================================

LN_subcommunity_rep1 = ['P1-25', 'P1-26', 'P1-27', 'P1-28', 'P1-29', 'P1-30', 'P1-31', 'P1-32', 'P1-33']
LN_subcommunity_rep2 = ['P1-37', 'P1-38', 'P1-39', 'P1-40', 'P1-41', 'P1-42', 'P1-43', 'P1-44', 'P1-45']

LN_coalescence_rep1 = ['P4-15', 'P4-16', 'P4-17', 'P4-18', 'P4-19', 'P4-20', 'P4-21', 'P4-22',
                       'P4-23', 'P4-24', 'P4-25', 'P4-26', 'P4-27', 'P4-28', 'P4-29', 'P4-30',
                       'P4-31', 'P4-32', 'P4-33', 'P4-34', 'P4-35', 'P4-36', 'P4-37', 'P4-38',
                       'P4-39', 'P4-40', 'P4-41']

LN_coalescence_rep2 = ['P4-56', 'P4-57', 'P4-58', 'P4-59', 'P4-60', 'P4-61', 'P4-62', 'P4-63',
                       'P4-64', 'P4-65', 'P4-66', 'P4-67', 'P4-68', 'P4-69', 'P4-70', 'P4-71',
                       'P4-72', 'P4-73', 'P4-74', 'P4-75', 'P4-76', 'P4-77', 'P4-78', 'P4-79',
                       'P4-80', 'P4-81', 'P4-82']

# ============================================================================
# MN (Medium Nitrogen) - 12 Species Pool
# ============================================================================

MN_subcommunity_rep1 = ['P8-73', 'P8-74', 'P8-75', 'P8-76', 'P8-77', 'P8-78', 'P8-79', 'P8-80', 'P8-81']
MN_subcommunity_rep2 = ['P8-85', 'P8-86', 'P8-87', 'P8-88', 'P8-89', 'P8-90', 'P8-91', 'P8-92', 'P8-93']

MN_coalescence_rep1 = ['P5-15', 'P5-16', 'P5-17', 'P5-18', 'P5-19', 'P5-20', 'P5-21', 'P5-22',
                       'P5-23', 'P5-24', 'P5-25', 'P5-26', 'P5-27', 'P5-28', 'P5-29', 'P5-30',
                       'P5-31', 'P5-32', 'P5-33', 'P5-34', 'P5-35', 'P5-36', 'P5-37', 'P5-38',
                       'P5-39', 'P5-40', 'P5-41']

MN_coalescence_rep2 = ['P5-56', 'P5-57', 'P5-58', 'P5-59', 'P5-60', 'P5-61', 'P5-62', 'P5-63',
                       'P5-64', 'P5-65', 'P5-66', 'P5-67', 'P5-68', 'P5-69', 'P5-70', 'P5-71',
                       'P5-72', 'P5-73', 'P5-74', 'P5-75', 'P5-76', 'P5-77', 'P5-78', 'P5-79',
                       'P5-80', 'P5-81', 'P5-82']

# ============================================================================
# HN (High Nitrogen) - 12 Species Pool
# ============================================================================

HN_subcommunity_rep1 = ['P2-25', 'P2-26', 'P2-27', 'P2-28', 'P2-29', 'P2-30', 'P2-31', 'P2-32', 'P2-33']
HN_subcommunity_rep2 = ['P2-37', 'P2-38', 'P2-39', 'P2-40', 'P2-41', 'P2-42', 'P2-43', 'P2-44', 'P2-45']

HN_coalescence_rep1 = ['P6-15', 'P6-16', 'P6-17', 'P6-18', 'P6-19', 'P6-20', 'P6-21', 'P6-22',
                       'P6-23', 'P6-24', 'P6-25', 'P6-26', 'P6-27', 'P6-28', 'P6-29', 'P6-30',
                       'P6-31', 'P6-32', 'P6-33', 'P6-34', 'P6-35', 'P6-36', 'P6-37', 'P6-38',
                       'P6-39', 'P6-40', 'P6-41']

HN_coalescence_rep2 = ['P6-56', 'P6-57', 'P6-58', 'P6-59', 'P6-60', 'P6-61', 'P6-62', 'P6-63',
                       'P6-64', 'P6-65', 'P6-66', 'P6-67', 'P6-68', 'P6-69', 'P6-70', 'P6-71',
                       'P6-72', 'P6-73', 'P6-74', 'P6-75', 'P6-76', 'P6-77', 'P6-78', 'P6-79',
                       'P6-80', 'P6-81', 'P6-82']

# ============================================================================
# Dictionary Organization for Easy Access
# ============================================================================

SAMPLES_BY_CONDITION = {
    'LN': {
        'subcommunity': {
            'rep1': LN_subcommunity_rep1,
            'rep2': LN_subcommunity_rep2,
            'all': LN_subcommunity_rep1 + LN_subcommunity_rep2
        },
        'coalescence': {
            'rep1': LN_coalescence_rep1,
            'rep2': LN_coalescence_rep2,
            'all': LN_coalescence_rep1 + LN_coalescence_rep2
        }
    },
    'MN': {
        'subcommunity': {
            'rep1': MN_subcommunity_rep1,
            'rep2': MN_subcommunity_rep2,
            'all': MN_subcommunity_rep1 + MN_subcommunity_rep2
        },
        'coalescence': {
            'rep1': MN_coalescence_rep1,
            'rep2': MN_coalescence_rep2,
            'all': MN_coalescence_rep1 + MN_coalescence_rep2
        }
    },
    'HN': {
        'subcommunity': {
            'rep1': HN_subcommunity_rep1,
            'rep2': HN_subcommunity_rep2,
            'all': HN_subcommunity_rep1 + HN_subcommunity_rep2
        },
        'coalescence': {
            'rep1': HN_coalescence_rep1,
            'rep2': HN_coalescence_rep2,
            'all': HN_coalescence_rep1 + HN_coalescence_rep2
        }
    }
}


def get_samples(medium, sample_type, replicate='all'):
    """
    Get sample IDs for a specific condition.

    Parameters:
    -----------
    medium : str
        'LN', 'MN', or 'HN'
    sample_type : str
        'subcommunity' or 'coalescence'
    replicate : str or int
        'all', 'rep1', 'rep2', 1, or 2

    Returns:
    --------
    list : Sample IDs

    Examples:
    ---------
    >>> get_samples('MN', 'subcommunity', 'rep1')
    ['P8-73', 'P8-74', ..., 'P8-81']

    >>> get_samples('LN', 'coalescence', 1)
    ['P4-15', 'P4-16', ..., 'P4-41']
    """
    if isinstance(replicate, int):
        replicate = f'rep{replicate}'

    return SAMPLES_BY_CONDITION[medium][sample_type][replicate]


# ============================================================================
# Summary Statistics
# ============================================================================

def print_summary():
    """Print summary of available samples."""
    medium_names = {'LN': 'Low Nitrogen', 'MN': 'Medium Nitrogen', 'HN': 'High Nitrogen'}
    print("Sample Organization Summary (12-species pool)")
    print("=" * 60)
    for medium in ['LN', 'MN', 'HN']:
        print(f"\n{medium} ({medium_names[medium]})")
        print("-" * 60)
        for sample_type in ['subcommunity', 'coalescence']:
            rep1_count = len(SAMPLES_BY_CONDITION[medium][sample_type]['rep1'])
            rep2_count = len(SAMPLES_BY_CONDITION[medium][sample_type]['rep2'])
            total_count = len(SAMPLES_BY_CONDITION[medium][sample_type]['all'])
            print(f"  {sample_type.capitalize():15s}: Rep1={rep1_count:2d}, Rep2={rep2_count:2d}, Total={total_count:2d}")


if __name__ == "__main__":
    print_summary()

    # Example usage
    print("\n\nExample Usage:")
    print("=" * 60)
    print("MN subcommunities replicate 1:")
    print(get_samples('MN', 'subcommunity', 1))
    print("\nHN coalescence all replicates:")
    print(get_samples('HN', 'coalescence', 'all')[:5], "... (showing first 5)")
