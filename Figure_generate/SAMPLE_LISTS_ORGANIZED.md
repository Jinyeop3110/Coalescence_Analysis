# Sample Lists Organized by Condition

All samples for **12-species pool experiments**, organized by medium type and replicate.

## Summary Statistics

| Medium | Type          | Rep 1 | Rep 2 | Total |
|--------|---------------|-------|-------|-------|
| **LN** | Subcommunity  | 9     | 9     | 18    |
| **LN** | Coalescence   | 27    | 27    | 54    |
| **MN** | Subcommunity  | 9     | 9     | 18    |
| **MN** | Coalescence   | 27    | 27    | 54    |
| **HN** | Subcommunity  | 9     | 9     | 18    |
| **HN** | Coalescence   | 27    | 27    | 54    |

---

## LN (Low Nitrogen)

### Subcommunities
- **Replicate 1 (9 samples)**: P1-25, P1-26, P1-27, P1-28, P1-29, P1-30, P1-31, P1-32, P1-33
- **Replicate 2 (9 samples)**: P1-37, P1-38, P1-39, P1-40, P1-41, P1-42, P1-43, P1-44, P1-45

### Coalescence
- **Replicate 1 (27 samples)**: P4-15 through P4-41
- **Replicate 2 (27 samples)**: P4-56 through P4-82

---

## MN (Medium Nitrogen)

### Subcommunities
- **Replicate 1 (9 samples)**: P8-73, P8-74, P8-75, P8-76, P8-77, P8-78, P8-79, P8-80, P8-81
- **Replicate 2 (9 samples)**: P8-85, P8-86, P8-87, P8-88, P8-89, P8-90, P8-91, P8-92, P8-93

### Coalescence
- **Replicate 1 (27 samples)**: P5-15 through P5-41
- **Replicate 2 (27 samples)**: P5-56 through P5-82

---

## HN (High Nitrogen)

### Subcommunities
- **Replicate 1 (9 samples)**: P2-25, P2-26, P2-27, P2-28, P2-29, P2-30, P2-31, P2-32, P2-33
- **Replicate 2 (9 samples)**: P2-37, P2-38, P2-39, P2-40, P2-41, P2-42, P2-43, P2-44, P2-45

### Coalescence
- **Replicate 1 (27 samples)**: P6-15 through P6-41
- **Replicate 2 (27 samples)**: P6-56 through P6-82

---

## Notes

1. Each medium condition has 9 subcommunities per replicate (2 replicates = 18 total)
2. Each medium condition has 27 coalescence samples per replicate (C(9,2) = 36 pairwise combinations, but 27 are present)
3. The pattern is consistent across all three medium types (LN, MN, HN)

## Usage

Import the organized dictionary from `sample_lists_by_condition.py`:

```python
from sample_lists_by_condition import SAMPLES_BY_CONDITION, get_samples

# Get MN subcommunities replicate 1
mn_sub_rep1 = get_samples('MN', 'subcommunity', 1)

# Get all HN coalescence samples
hn_coal_all = get_samples('HN', 'coalescence', 'all')

# Or access directly
ln_samples = SAMPLES_BY_CONDITION['LN']['coalescence']['rep2']
```
