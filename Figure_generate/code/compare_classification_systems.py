"""
Compare the two classification systems used in the codebase
"""

import numpy as np

print("="*70)
print("COMPARING TWO CLASSIFICATION SYSTEMS")
print("="*70)

print("\n" + "="*70)
print("SYSTEM 1: Original Phase Diagrams (200reps, 500reps, etc.)")
print("="*70)

print("""
Step 1: Calculate assymetricity from (x1, x2, x3):
    x = sqrt(x1² + x2²)
    y = |abs(arctan(x1/x2)) - π/4| / (π/4)

Step 2: Classify based on (x, y):
    if (x² > 0.5) AND (y > 0.5):
        return 0  # Dominance
    if (x² > 0.5) AND (y < 0.5):
        return 1  # Mixing
    if (x² < 0.5):
        return 2  # Restructuring
""")

print("\n" + "="*70)
print("SYSTEM 2: New Heatmaps (mean×variance)")
print("="*70)

print("""
Direct classification from (x1, x2, x3):
    if x1 > 0.7:
        DOMINANCE (c1 wins)
    elif x2 > 0.7:
        DOMINANCE (c2 wins)
    elif x3 > 0.7:
        RESTRUCTURING
    else:
        MIXING
""")

print("\n" + "="*70)
print("KEY DIFFERENCES")
print("="*70)

print("""
1. **System 1 uses (x, y) transformed coordinates**
   - x = sqrt(x1² + x2²) measures combined parent contribution
   - y measures asymmetry between parents

2. **System 2 uses raw (x1, x2, x3) coordinates**
   - Direct thresholds on individual components

3. **Different threshold values**:
   - System 1: x² > 0.5 (i.e., x > 0.707...) for parent contribution
   - System 2: x1 or x2 > 0.7 for dominance

4. **Different mixing criteria**:
   - System 1: x² > 0.5 AND y < 0.5 (high parent contribution, low asymmetry)
   - System 2: All x1, x2, x3 ≤ 0.7
""")

print("\n" + "="*70)
print("COMPARING THRESHOLDS")
print("="*70)

# System 1: x² > 0.5 means x > sqrt(0.5) ≈ 0.707
threshold_system1 = np.sqrt(0.5)
print(f"\nSystem 1 threshold: x > {threshold_system1:.4f} (≈ 0.707)")
print(f"System 2 threshold: x1 or x2 > 0.7")
print(f"\nThese are VERY SIMILAR!")

print("\n" + "="*70)
print("TEST CASES COMPARISON")
print("="*70)

def system1_classify(x1, x2, x3):
    """Original system classification"""
    x = np.sqrt(x1**2 + x2**2)
    if x2 == 0:
        y = 1.0 if x1 > 0 else 0.0
    else:
        y = np.abs(np.abs(np.arctan(x1/x2)) - np.pi/4) / (np.pi/4)

    if (x**2 > 0.5) and (y > 0.5):
        return "DOMINANCE"
    if (x**2 > 0.5) and (y < 0.5):
        return "MIXING"
    if (x**2 < 0.5):
        return "RESTRUCTURING"
    return "UNCLEAR"

def system2_classify(x1, x2, x3):
    """New system classification"""
    if x1 > 0.7:
        return "DOMINANCE"
    elif x2 > 0.7:
        return "DOMINANCE"
    elif x3 > 0.7:
        return "RESTRUCTURING"
    else:
        return "MIXING"

test_cases = [
    (0.85, 0.10, 0.05, "Strong c1 dominance"),
    (0.10, 0.85, 0.05, "Strong c2 dominance"),
    (0.60, 0.60, 0.20, "Balanced parents"),
    (0.50, 0.50, 0.50, "Equal three-way"),
    (0.10, 0.10, 0.85, "Strong restructuring"),
    (0.71, 0.00, 0.00, "Barely c1 dominance"),
    (0.00, 0.71, 0.00, "Barely c2 dominance"),
    (0.50, 0.50, 0.71, "Restructuring with parents"),
]

print("\n")
for x1, x2, x3, description in test_cases:
    # Normalize to ensure constraint
    norm = np.sqrt(x1**2 + x2**2 + x3**2)
    x1_n, x2_n, x3_n = x1/norm, x2/norm, x3/norm

    result1 = system1_classify(x1_n, x2_n, x3_n)
    result2 = system2_classify(x1_n, x2_n, x3_n)

    match = "✓" if result1 == result2 else "✗"

    print(f"{match} x1={x1_n:.2f}, x2={x2_n:.2f}, x3={x3_n:.2f} - {description}")
    print(f"  System 1: {result1:15s}  System 2: {result2}")
    if result1 != result2:
        print(f"  >>> MISMATCH!")
    print()

print("="*70)
print("CONCLUSION")
print("="*70)
print("""
The two systems are SIMILAR but NOT IDENTICAL:

1. Both use similar thresholds (~0.707 vs 0.7)
2. System 1 considers ASYMMETRY between parents (y parameter)
3. System 2 treats each parent independently

For the original phase diagrams (200reps, 500reps, narrow/wide uniform),
System 1 is used with the asymmetricity calculation.

For your new mean×variance heatmaps, System 2 is used with direct thresholds.

This means the classifications are SLIGHTLY DIFFERENT between the two
sets of plots!
""")
