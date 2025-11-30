# How Same-Origin vs Mixed-Origin Pairs Are Classified

## The Key Question

When we have a coalescence experiment:
- **Parent A** (community 1) has some species
- **Parent B** (community 2) has some species
- **Offspring** (coalesced community) has species from both parents

For any pair of species (i, j) in the offspring, we need to determine:
- Are both from **Parent A**? → Same-origin (A-A)
- Are both from **Parent B**? → Same-origin (B-B)
- Is one from A and one from B? → Mixed-origin (A-B)

## The Challenge

**Problem**: In the offspring community, we only see which species are present. We **don't directly know** which parent each species came from!

**Example**:
```
Parent A: Species [1, 2, 3, 4, 5]
Parent B: Species [6, 7, 8, 9, 10]
Offspring: Species [2, 3, 7, 8]

Question: Where did Species 2 come from? Parent A!
Question: Where did Species 7 come from? Parent B!
```

This is easy when parents have **completely non-overlapping** species. But what about overlapping species?

## The Solution: Origin Tracking Based on Parent Communities

### Step 1: Determine Species Origins

For **each species** in the dataset, we determine its origin by looking at the **parent communities**:

```python
def determine_species_origin(species_idx, parent1_list, parent2_list, threshold=1e-4):
    """
    Determine if a species originates from Parent A (0) or Parent B (1).

    Averaged across all replicates.
    """
    # Calculate average abundance in each parent across ALL replicates
    avg_parent1 = np.mean([p1[species_idx] for p1 in parent1_list])
    avg_parent2 = np.mean([p2[species_idx] for p2 in parent2_list])

    # Check presence in parents
    present_in_p1 = avg_parent1 > threshold
    present_in_p2 = avg_parent2 > threshold

    if present_in_p1 and not present_in_p2:
        return 0  # Parent A only
    elif present_in_p2 and not present_in_p1:
        return 1  # Parent B only
    elif present_in_p1 and present_in_p2:
        # Overlapping species - assign to parent with higher abundance
        return 0 if avg_parent1 >= avg_parent2 else 1
    else:
        # Novel species (not in either parent) - default to Parent A
        return 0
```

### Step 2: Classify Pairs

Once we know each species' origin, classifying pairs is straightforward:

```python
def classify_pair(species_i, species_j, species_origins):
    """
    Classify a pair as same-origin or mixed-origin.
    """
    origin_i = species_origins[species_i]
    origin_j = species_origins[species_j]

    if origin_i == origin_j:
        # Both from same parent
        if origin_i == 0:
            return 'same_origin', 'A-A'
        else:
            return 'same_origin', 'B-B'
    else:
        # One from each parent
        return 'mixed_origin', 'A-B'
```

## Detailed Example

### Scenario: LN_12 Experiment (52 replicates)

#### Parent Communities (Averaged Across Replicates)

```
Species Index    Avg in Parent A    Avg in Parent B    Origin Assignment
─────────────────────────────────────────────────────────────────────────
    0                0.08               0.00              A (only in A)
    1                0.06               0.00              A (only in A)
    2                0.12               0.00              A (only in A)
    3                0.09               0.00              A (only in A)
    4                0.00               0.15              B (only in B)
    5                0.00               0.11              B (only in B)
    6                0.05               0.08              B (overlap, higher in B)
    7                0.10               0.02              A (overlap, higher in A)
    ...
```

#### Species Origin Array

```python
species_origins = [0, 0, 0, 0, 1, 1, 1, 0, 1, 1, ...]
                   A  A  A  A  B  B  B  A  B  B
```

#### Pair Classification Examples

**Example 1: Species 2 and Species 3**
```
origin[2] = 0 (Parent A)
origin[3] = 0 (Parent A)

→ Same origin? YES (both A)
→ Pair type: 'same_origin'
→ Pair subtype: 'A-A'
```

**Example 2: Species 4 and Species 5**
```
origin[4] = 1 (Parent B)
origin[5] = 1 (Parent B)

→ Same origin? YES (both B)
→ Pair type: 'same_origin'
→ Pair subtype: 'B-B'
```

**Example 3: Species 2 and Species 5**
```
origin[2] = 0 (Parent A)
origin[5] = 1 (Parent B)

→ Same origin? NO (A vs B)
→ Pair type: 'mixed_origin'
→ Pair subtype: 'A-B'
```

## Handling Edge Cases

### Case 1: Overlapping Species

**Species 6** appears in both parents:
```
Avg abundance in Parent A: 0.05
Avg abundance in Parent B: 0.08

→ Assign to Parent B (higher abundance)
→ origin[6] = 1
```

**Why this makes sense**: If the species is more abundant in Parent B, it's more likely to be "characteristic" of that community.

### Case 2: Novel Species

**Species 99** appears in offspring but not in either parent:
```
Avg abundance in Parent A: 0.000
Avg abundance in Parent B: 0.000

→ Default assignment: Parent A
→ origin[99] = 0
```

**Why**: Novel species are rare. Default to Parent A for consistency.

### Case 3: Rare/Borderline Species

**Species 50** is just above threshold:
```
Avg abundance in Parent A: 0.0012
Avg abundance in Parent B: 0.0008
Threshold: 0.001

→ Both above threshold (present in both)
→ Assign to Parent A (higher abundance)
→ origin[50] = 0
```

## Implementation in Code

From `CooccurrenceAsymmetricityAnalysis.py`:

```python
def analyze_type3_asymmetricity(offspring_list, parent1_list, parent2_list,
                                threshold=1e-4):
    """
    Main Type 3 analysis function.
    """
    n_species = len(offspring_list[0])

    # Determine species origins
    species_origins = np.zeros(n_species, dtype=int)

    for s in range(n_species):
        # Calculate average abundance in each parent across ALL replicates
        avg_parent1 = np.mean([p1[s] for p1 in parent1_list])
        avg_parent2 = np.mean([p2[s] for p2 in parent2_list])

        # Check presence
        present_in_p1 = avg_parent1 > threshold
        present_in_p2 = avg_parent2 > threshold

        if present_in_p1 and not present_in_p2:
            species_origins[s] = 0  # Parent A
        elif present_in_p2 and not present_in_p1:
            species_origins[s] = 1  # Parent B
        elif present_in_p1 and present_in_p2:
            # Assign to parent with higher abundance
            species_origins[s] = 0 if avg_parent1 >= avg_parent2 else 1
        else:
            species_origins[s] = 0  # Default to Parent A

    # Now classify all pairs
    for i in range(n_species):
        for j in range(i + 1, n_species):
            origin_i = species_origins[i]
            origin_j = species_origins[j]

            if origin_i == origin_j:
                pair_type = 'same_origin'
                pair_subtype = 'A-A' if origin_i == 0 else 'B-B'
            else:
                pair_type = 'mixed_origin'
                pair_subtype = 'A-B'
```

## Visual Example: LN_12 with 20 Species

```
Species Origins (determined from parent communities):
┌─────────────────────────────────────────────────────┐
│ Species:  0  1  2  3  4  5  6  7  8  9 10 11 12 ... │
│ Origin:   A  A  A  A  A  B  B  B  B  B  A  A  B ... │
│           ↑──────Parent A──────↑     ↑──Parent B──↑ │
└─────────────────────────────────────────────────────┘

Pair Classifications:
┌──────────────────────────────────────────────────────┐
│ Pair (0,1):  A + A  →  Same-origin (A-A)            │
│ Pair (0,5):  A + B  →  Mixed-origin (A-B)           │
│ Pair (2,3):  A + A  →  Same-origin (A-A)            │
│ Pair (5,6):  B + B  →  Same-origin (B-B)            │
│ Pair (4,10): A + A  →  Same-origin (A-A)            │
│ ...                                                  │
└──────────────────────────────────────────────────────┘
```

## What Determines "Parent A" vs "Parent B"?

In the experimental design:
- **Parent A** (parent1) = First parent community mixed
- **Parent B** (parent2) = Second parent community mixed

The distinction is maintained throughout:
```
Parent1 samples: Always labeled as "Sub1" in SampleIDX
Parent2 samples: Always labeled as "Sub2" in SampleIDX
```

## Summary Statistics

After classification, we count:

```python
# Count pairs by type
n_same_origin_AA = count(pair_subtype == 'A-A')
n_same_origin_BB = count(pair_subtype == 'B-B')
n_same_origin_total = n_same_origin_AA + n_same_origin_BB

n_mixed_origin_AB = count(pair_subtype == 'A-B')

# Example output for LN_12:
# Same-origin pairs: 231 total (120 A-A, 111 B-B)
# Mixed-origin pairs: 234 total (all A-B)
```

## Why This Classification Matters

**The enrichment question**: Are same-origin pairs (A-A or B-B) more likely to co-occur than mixed-origin pairs (A-B)?

**Biological interpretation**:
- **High same-origin enrichment** → Species from the same parent community "stick together"
  - Suggests pre-existing facilitative interactions
  - Community-level selection

- **No enrichment** → Co-occurrence is random with respect to parent origin
  - Species mix independently
  - No parent community structure preserved

## Real Results from LN_12

```
Species origins determined from 52 replicates:
- Parent A species: ~65 species (on average)
- Parent B species: ~65 species (on average)

Pair classifications:
- Same-origin pairs: 231 (from ~65×64/2 + ~65×64/2 possible)
- Mixed-origin pairs: 234 (from ~65×65 possible)

Enrichment result:
- Same-origin significant: 49/231 = 21%
- Mixed-origin significant: 7/234 = 3%
- Enrichment ratio: 7.09× (p < 0.0001 ***)

Interpretation: Species from the same parent are 7× more likely to co-occur!
```

## Key Takeaway

✓ **Species origins** are determined by comparing their abundance in parent communities (averaged across all replicates)

✓ **Pair classification** is based on whether both species have the same origin or different origins

✓ This is a **property of the species themselves**, not of individual coalescence events

✓ Once origins are assigned, every pair has a fixed classification (same vs mixed)
