"""
Explain the EXACT classification rule with all edge cases
"""

print("="*70)
print("EXACT CLASSIFICATION RULE")
print("="*70)

print("""
The classification uses a SEQUENTIAL if-elif-else structure:

STEP 1: Check if x1 > 0.7
    → YES: DOMINANCE (Community 1 wins)
    → NO: Go to Step 2

STEP 2: Check if x2 > 0.7
    → YES: DOMINANCE (Community 2 wins)
    → NO: Go to Step 3

STEP 3: Check if x3 > 0.7
    → YES: RESTRUCTURING
    → NO: Go to Step 4

STEP 4: (else clause)
    → MIXING

""")

print("="*70)
print("IMPORTANT: ORDER MATTERS!")
print("="*70)

print("""
Because of the if-elif-else structure, the checks happen IN ORDER:

Priority hierarchy:
1. x1 > 0.7 (checked first) → DOMINANCE
2. x2 > 0.7 (checked second) → DOMINANCE
3. x3 > 0.7 (checked third) → RESTRUCTURING
4. Everything else → MIXING

""")

print("="*70)
print("EDGE CASES")
print("="*70)

test_cases = [
    # (x1, x2, x3, expected_outcome, explanation)
    (0.85, 0.10, 0.05, "DOMINANCE", "x1 > 0.7, stops at first check"),
    (0.10, 0.85, 0.05, "DOMINANCE", "x1 < 0.7, x2 > 0.7, stops at second check"),
    (0.10, 0.10, 0.85, "RESTRUCTURING", "x1 < 0.7, x2 < 0.7, x3 > 0.7"),
    (0.50, 0.45, 0.35, "MIXING", "All < 0.7, falls through to else"),
    (0.71, 0.71, 0.00, "DOMINANCE", "Both x1 and x2 > 0.7, but x1 checked FIRST → DOMINANCE (c1)"),
    (0.65, 0.65, 0.71, "RESTRUCTURING", "x1 and x2 < 0.7, x3 > 0.7"),
    (0.71, 0.20, 0.71, "DOMINANCE", "x1 > 0.7 checked FIRST, even though x3 > 0.7 too!"),
    (0.20, 0.71, 0.71, "DOMINANCE", "x2 > 0.7 checked SECOND, even though x3 > 0.7 too!"),
    (0.70, 0.70, 0.70, "MIXING", "All exactly 0.7 (not > 0.7), falls through to else"),
    (0.71, 0.00, 0.00, "DOMINANCE", "x1 barely over threshold"),
]

print("\nTest cases showing exact behavior:\n")
for x1, x2, x3, expected, explanation in test_cases:
    # Simulate the exact classification logic
    if x1 > 0.7:
        result = "DOMINANCE (c1)"
    elif x2 > 0.7:
        result = "DOMINANCE (c2)"
    elif x3 > 0.7:
        result = "RESTRUCTURING"
    else:
        result = "MIXING"

    print(f"x1={x1:.2f}, x2={x2:.2f}, x3={x3:.2f}")
    print(f"  → {result}")
    print(f"  → {explanation}")
    print()

print("="*70)
print("KEY INSIGHTS")
print("="*70)

print("""
1. **x1 has priority over x2 and x3**
   If x1 > 0.7, it's DOMINANCE, even if x2 or x3 are also > 0.7

2. **x2 has priority over x3**
   If x1 ≤ 0.7 but x2 > 0.7, it's DOMINANCE, even if x3 > 0.7

3. **x3 is only checked if both x1 and x2 ≤ 0.7**

4. **The threshold is exclusive** (> 0.7, not ≥ 0.7)
   So x1 = 0.7 exactly does NOT count as dominance

5. **Only ONE category per event**
   Even if multiple xi > 0.7, only one category is assigned based on priority

6. **Is it possible for multiple xi > 0.7 simultaneously?**
   Given the constraint x1² + x2² + x3² = 1:
   - If x1 = 0.71, then x2² + x3² = 1 - 0.71² = 0.496
   - Maximum for either x2 or x3: √0.496 ≈ 0.70
   - So it's BARELY possible for two to exceed 0.7, but not three
   - Example: x1 = 0.71, x2 = 0.70, x3 = 0.01 (x1² + x2² + x3² ≈ 0.995 ≈ 1)

""")

print("="*70)
print("MATHEMATICALLY POSSIBLE CASES WHERE MULTIPLE > 0.7")
print("="*70)

import numpy as np

# Check if two can exceed 0.7 simultaneously
x1_test = 0.71
remaining = 1 - x1_test**2
x2_max = np.sqrt(remaining)

print(f"\nIf x1 = {x1_test}:")
print(f"  Remaining for x2² + x3²: {remaining:.4f}")
print(f"  Maximum x2 or x3: {x2_max:.4f}")
print(f"  So if x1 > 0.7, can x2 also be > 0.7? {x2_max > 0.7}")

# Find minimum x1 such that x2 can still be > 0.7
# We need x1² + 0.7² ≤ 1
# x1² ≤ 1 - 0.49 = 0.51
# x1 ≤ √0.51 ≈ 0.714
x1_max_for_x2_over_07 = np.sqrt(1 - 0.7**2)
print(f"\nFor x2 to be > 0.7, x1 must be ≤ {x1_max_for_x2_over_07:.4f}")
print(f"So YES, both x1 and x2 can simultaneously exceed 0.7")
print(f"Example: x1 = 0.71, x2 = 0.70, x3 = 0.01")
print(f"  Check: {0.71**2 + 0.70**2 + 0.01**2:.4f} (should be ≈ 1.0)")

print(f"\nIn this case, the classification would be:")
print(f"  DOMINANCE (c1 wins) because x1 > 0.7 is checked FIRST")
print(f"  Even though x2 > 0.7 as well!")

print("\n" + "="*70)
print("CONCLUSION")
print("="*70)
print("""
The classification rule is:

    if x1 > 0.7:
        DOMINANCE (Community 1 wins)
    elif x2 > 0.7:
        DOMINANCE (Community 2 wins)
    elif x3 > 0.7:
        RESTRUCTURING
    else:
        MIXING

This is a HIERARCHICAL rule with priority order: x1 > x2 > x3.

Edge cases where multiple xi > 0.7 are possible but rare, and the first
condition that passes determines the classification.
""")
