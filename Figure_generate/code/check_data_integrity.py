#!/usr/bin/env python3
"""
Check data integrity of 100-repetition simulation
"""

import json

def check_data_integrity():
    with open('Simulation_Data/48species_100reps_final/Community_100reps_final.json', 'r') as f:
        data = json.load(f)

    print("Data structure check:")
    print("=" * 50)
    
    for u in ['0.3', '0.5', '0.8']:
        if u in data:
            reps = len(data[u])
            print(f"\nu = {u}: {reps} repetitions")
            
            # Sample rep keys
            rep_keys = list(data[u].keys())[:3]
            print(f"  Sample rep keys: {rep_keys}")
            
            # Check structure
            first_rep = data[u][rep_keys[0]]
            sc_count = len(first_rep['sc_list'])
            cc_count = len(first_rep['cc_list'])
            print(f"  Structure: sc_list={sc_count}, cc_list={cc_count}")
            
            # Check if seeds are unique
            seeds_seen = set()
            duplicate_seeds = 0
            for rep_key in data[u].keys():
                rep_data = data[u][rep_key]
                if 'parameters' in rep_data and 'seed' in rep_data['parameters']:
                    seed = rep_data['parameters']['seed']
                    if seed in seeds_seen:
                        duplicate_seeds += 1
                    else:
                        seeds_seen.add(seed)
                        
            print(f"  Unique seeds: {len(seeds_seen)}, Duplicates: {duplicate_seeds}")
            
            # Check for empty coalescence results
            empty_coalescence = 0
            total_pairs = 0
            for rep_key in data[u].keys():
                rep_data = data[u][rep_key]
                for pair_key, c_mix in rep_data['cc_list'].items():
                    total_pairs += 1
                    if sum(c_mix) == 0:
                        empty_coalescence += 1
            
            print(f"  Total pairs: {total_pairs}, Empty results: {empty_coalescence} ({100*empty_coalescence/total_pairs:.1f}%)")
            
            # Sample some actual data
            sample_rep = data[u]['rep_000']
            sample_pair = list(sample_rep['cc_list'].keys())[0]
            sample_result = sample_rep['cc_list'][sample_pair]
            print(f"  Sample result ({sample_pair}): sum={sum(sample_result):.3f}, alive={sum(1 for x in sample_result if x > 1e-3)}")
            
        else:
            print(f"\nu = {u}: NOT FOUND")
    
    print("\n" + "=" * 50)
    print("Summary:")
    print(f"Total interaction strengths: {len(data.keys())}")
    total_reps = sum(len(data[u]) for u in data.keys())
    print(f"Total repetitions: {total_reps}")

if __name__ == "__main__":
    check_data_integrity()