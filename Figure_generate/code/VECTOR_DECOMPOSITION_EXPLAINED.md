# How x1, x2, and x3 Are Defined

## The Vector Decomposition Function

The function `metric_VectorDecomposition_onlyPositive(u, v, m)` decomposes the coalesced community `m` into contributions from parent communities `u` and `v`.

### Input:
- `u`: Parent community 1 abundances (48-dimensional vector)
- `v`: Parent community 2 abundances (48-dimensional vector)
- `m`: Coalesced community abundances (48-dimensional vector)

### Step-by-Step Process:

#### Step 1: Normalize all vectors
```python
u = normalize(u)  # u → u/||u||
v = normalize(v)  # v → v/||v||
m = normalize(m)  # m → m/||m||
```

After normalization:
- ||u|| = 1
- ||v|| = 1
- ||m|| = 1

#### Step 2: Solve for coefficients e1 and e2
We want to find coefficients such that:
```
m ≈ e1 × u + e2 × v + residual
```

This is done by solving a least-squares problem:
```python
A = [[u·u, u·v],      # [[1,   u·v],
     [u·v, v·v]]      #  [u·v, 1  ]]

e12 = A^(-1) × [m·u, m·v]
```

This gives us:
- `e1 = e12[0]`: Projection coefficient for community 1
- `e2 = e12[1]`: Projection coefficient for community 2

#### Step 3: Apply "only positive" constraint
```python
x1_raw = e1 if e1 > 0 else 0
x2_raw = e2 if e2 > 0 else 0
```

If a coefficient is negative, it's set to 0. This ensures we only count positive contributions.

#### Step 4: Calculate residual (novel component)
```python
residual_vector = m - (e1 × u) - (e2 × v)
x3 = ||residual_vector||  # Magnitude of residual
```

`x3` measures how much of `m` cannot be explained by the two parent communities.

#### Step 5: Normalize to unit sphere
The raw values (x1_raw, x2_raw, x3) don't necessarily satisfy x1² + x2² + x3² = 1.

To normalize them:
```python
convert = sqrt((1 - x3²) / (x1_raw² + x2_raw²))

x1 = convert × x1_raw
x2 = convert × x2_raw
x3 = x3  # Already normalized
```

This ensures:
**x1² + x2² + x3² = 1**

### Output:
- `x1`: Normalized coefficient for parent community 1
- `x2`: Normalized coefficient for parent community 2
- `x3`: Magnitude of novel/restructured component

### Mathematical Interpretation:

The coalesced community `m` is represented as:
```
m ≈ x1 × (unit vector along u) + x2 × (unit vector along v) + x3 × (novel direction)
```

Where:
- **x1**: How much of m is in the direction of community 1
- **x2**: How much of m is in the direction of community 2
- **x3**: How much of m is in a novel direction (perpendicular to both u and v)

### Why This Makes Sense:

1. **Geometric interpretation**: Think of u, v, and m as points on a unit sphere (since they're normalized)

2. **Decomposition**: We're asking "how much of m can be explained by u and v, and how much is new?"

3. **Positive-only**: Negative coefficients would mean "anti-contribution", which doesn't make biological sense

4. **Normalization**: The constraint x1² + x2² + x3² = 1 puts all outcomes on an equal footing for comparison

### Example:

#### Example 1: Perfect preservation of community 1
```
Input:
  u = [1, 0, 0, ..., 0]  (only species 1 abundant)
  v = [0, 1, 0, ..., 0]  (only species 2 abundant)
  m = [1, 0, 0, ..., 0]  (same as u)

Output:
  x1 ≈ 1.0  (fully explained by u)
  x2 ≈ 0.0  (no contribution from v)
  x3 ≈ 0.0  (no novel component)
```

#### Example 2: 50-50 mix
```
Input:
  u = [1, 0, 0, ..., 0]
  v = [0, 1, 0, ..., 0]
  m = [0.707, 0.707, 0, ..., 0]  (equal mix, normalized)

Output:
  x1 ≈ 0.707
  x2 ≈ 0.707
  x3 ≈ 0.0
```

#### Example 3: Novel community
```
Input:
  u = [1, 0, 0, ..., 0]
  v = [0, 1, 0, ..., 0]
  m = [0, 0, 1, ..., 0]  (different species dominates)

Output:
  x1 ≈ 0.0
  x2 ≈ 0.0
  x3 ≈ 1.0  (fully novel)
```

### Connection to Classification:

With threshold = sqrt(0.5) ≈ 0.707:

- **x1 > 0.707**: Community 1 dominates (>50% of variance explained by u)
- **x2 > 0.707**: Community 2 dominates (>50% of variance explained by v)
- **x3 > 0.707**: Restructuring (>50% of variance is novel)
- **All ≤ 0.707**: Mixing (no single component dominates)

### Why sqrt(0.5)?

If x1 = sqrt(0.5), then x1² = 0.5, meaning 50% of the normalized variance is explained by community 1.

This is a natural threshold because:
- Above sqrt(0.5): More than 50% contribution from that component
- Below sqrt(0.5): Less than 50% contribution

It's equivalent to the old system's criterion: x² > 0.5.
