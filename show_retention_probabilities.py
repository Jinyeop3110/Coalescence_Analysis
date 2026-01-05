#!/usr/bin/env python3
"""
Show what retention probabilities would be used by species pool size
"""

import os
import json

# Expected lookup table structure based on the code
print("RETENTION PROBABILITY SETTINGS BY SPECIES POOL SIZE")
print("=" * 70)
print()

# Check if lookup files exist
v1_path = "Figure_generate/code/Figure/AsymmetricityAnalysis/version_1/retention_probability_lookup.json"
v2_path = "Figure_generate/code/Figure/AsymmetricityAnalysis/version_2/retention_probability_lookup.json"

v1_exists = os.path.exists(v1_path)
v2_exists = os.path.exists(v2_path)

if not v1_exists and not v2_exists:
    print("CURRENT SETTINGS:")
    print("-" * 40)
    print("Lookup tables NOT FOUND - Using default probability: 0.5 (50%)")
    print()
    print("This means ALL conditions and species pools use:")
    print("  - Selection probability: 0.5")
    print("  - Each species has 50% chance of being retained")
    print("  - No variation by nutrient condition (LN/MN/HN)")
    print("  - No variation by species pool size (6/12/24)")
    print()
else:
    if v1_exists:
        with open(v1_path, 'r') as f:
            v1_lookup = json.load(f)
        print("VERSION 1 (Excluding overlaps):")
        print("-" * 40)
        print("Key format: {Nutrient}_{Species_Pool}")
        print()
        for key in sorted(v1_lookup.keys()):
            print(f"  {key}: {v1_lookup[key]:.3f}")
        print()
    
    if v2_exists:
        with open(v2_path, 'r') as f:
            v2_lookup = json.load(f)
        print("VERSION 2 (Including overlaps):")
        print("-" * 40)
        print("Key format: {Nutrient}_{Species_Pool}")
        print()
        for key in sorted(v2_lookup.keys()):
            print(f"  {key}: {v2_lookup[key]:.3f}")
        print()

print("EXPECTED PROBABILITY STRUCTURE (when calculated):")
print("-" * 50)
print()
print("The lookup table should contain entries for:")
print("  - LN_6:  Low nutrient, 6 species pool")
print("  - LN_12: Low nutrient, 12 species pool")
print("  - LN_24: Low nutrient, 24 species pool")
print("  - MN_6:  Medium nutrient, 6 species pool")
print("  - MN_12: Medium nutrient, 12 species pool")
print("  - MN_24: Medium nutrient, 24 species pool")
print("  - HN_6:  High nutrient, 6 species pool")
print("  - HN_12: High nutrient, 12 species pool")
print("  - HN_24: High nutrient, 24 species pool")
print()
print("Plus defaults:")
print("  - LN_default: Average for all LN conditions")
print("  - MN_default: Average for all MN conditions")
print("  - HN_default: Average for all HN conditions")
print()

print("HOW SELECTION WORKS:")
print("-" * 50)
print()
print("1. For each null model iteration:")
print("   - Randomly select a real parent pair")
print("   - Get their nutrient condition (LN/MN/HN)")
print("   - Get their species pool size (6/12/24)")
print()
print("2. Look up retention probability:")
print("   - First try: '{nutrient}_{species_pool}' (e.g., 'LN_12')")
print("   - If not found: '{nutrient}_default' (e.g., 'LN_default')")
print("   - If not found: 0.5 (50%)")
print()
print("3. Apply to each species:")
print("   - Each species has 'selection_prob' chance of retention")
print("   - Selected species get random abundances")
print()

# Show documented ranges from code
print("DOCUMENTED EMPIRICAL RANGES (from code comments):")
print("-" * 50)
print()
print("Version 1 (excluding overlaps):")
print("  LN: 0.61-0.66 (61-66% retention)")
print("  MN: 0.37-0.66 (37-66% retention)")
print("  HN: 0.39-0.61 (39-61% retention)")
print()
print("Version 2 (including overlaps):")
print("  LN: 0.70-0.76 (70-76% retention)")
print("  MN: 0.54-0.90 (54-90% retention)")
print("  HN: 0.55-0.90 (55-90% retention)")
print()
print("Note: These ranges likely vary by species pool size within each nutrient condition")