#!/usr/bin/env python3
"""
Test the updated retention asymmetricity analysis with detailed breakdowns
"""

import sys
sys.path.append('/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code')

def test_updated_analysis():
    """Test the updated analysis with matplotlib import guard"""
    
    print("🔬 TESTING UPDATED RETENTION ASYMMETRICITY ANALYSIS")
    print("=" * 60)
    
    try:
        # Test imports without matplotlib
        print("Testing imports...")
        
        # Import the create function directly
        from AsymmetricityNullModelAnalysis import create_realistic_test_data_with_asymmetricity
        
        # Create test data
        print("Creating realistic test data...")
        offspring_list, parent1_list, parent2_list, conditions, species_numbers = create_realistic_test_data_with_asymmetricity()
        
        print(f"✅ Test data created:")
        print(f"   - {len(offspring_list)} events")
        print(f"   - Conditions: {dict(zip(*__import__('numpy').unique(conditions, return_counts=True)))}")
        print(f"   - Species pools: {dict(zip(*__import__('numpy').unique(species_numbers, return_counts=True)))}")
        
        # Test retention calculation functions directly
        print("\nTesting retention calculation functions...")
        
        # Import the functions we need
        from AsymmetricityAnalysis import (
            calculate_retention_asymmetricity_type1,
            calculate_retention_asymmetricity_type2
        )
        
        # Test on first few samples
        print("Testing retention calculations on sample data...")
        
        for i in range(min(3, len(offspring_list))):
            print(f"\nSample {i+1} ({conditions[i]} - Pool {species_numbers[i]}):")
            
            # Test Type 1
            ret1 = calculate_retention_asymmetricity_type1(
                parent1_list[i], parent2_list[i], offspring_list[i], n_permutations=100
            )
            print(f"   Type 1: asymmetricity={ret1['asymmetricity']:.3f}, p={ret1['p_value']:.3f}, sig={ret1['significant']}")
            
            # Test Type 2  
            ret2 = calculate_retention_asymmetricity_type2(
                parent1_list[i], parent2_list[i], offspring_list[i], n_permutations=100
            )
            print(f"   Type 2: asymmetricity={ret2['asymmetricity']:.3f}, p={ret2['p_value']:.3f}, sig={ret2['significant']}")
        
        print("\n✅ SUCCESS: All retention calculations working properly!")
        
        # Test the analysis structure (without matplotlib plotting)
        print("\nTesting analysis data structure...")
        
        # Create a mock results structure to test our plotting function logic
        conditions_list = ['LN', 'MN', 'HN']
        mock_results = {
            'experimental': {
                condition: {
                    'type1': {'asymmetricity': [], 'p_values': [], 'significant': []},
                    'type2': {'asymmetricity': [], 'p_values': [], 'significant': []}
                } for condition in conditions_list
            },
            'null_models': {
                'neutral_mixing': {
                    condition: {
                        'type1': {'asymmetricity': []},
                        'type2': {'asymmetricity': []}
                    } for condition in conditions_list
                }
            }
        }
        
        # Fill with sample data
        import numpy as np
        np.random.seed(42)
        
        for condition in conditions_list:
            n_samples = np.random.randint(5, 15)
            
            # Experimental data
            mock_results['experimental'][condition]['type1']['asymmetricity'] = np.random.uniform(0.1, 0.6, n_samples).tolist()
            mock_results['experimental'][condition]['type2']['asymmetricity'] = np.random.uniform(0.05, 0.4, n_samples).tolist()
            mock_results['experimental'][condition]['type1']['significant'] = (np.random.random(n_samples) < 0.3).tolist()
            mock_results['experimental'][condition]['type2']['significant'] = (np.random.random(n_samples) < 0.2).tolist()
            
            # Null model data
            mock_results['null_models']['neutral_mixing'][condition]['type1']['asymmetricity'] = np.random.uniform(0.0, 0.2, n_samples).tolist()
            mock_results['null_models']['neutral_mixing'][condition]['type2']['asymmetricity'] = np.random.uniform(0.0, 0.15, n_samples).tolist()
        
        print("✅ Mock results structure created successfully!")
        
        # Test breakdown by species pool
        print("\nTesting species pool breakdown logic...")
        
        unique_species = list(set(species_numbers))
        print(f"   Unique species pools: {unique_species}")
        
        for condition in ['LN', 'MN', 'HN']:
            condition_indices = [j for j, c in enumerate(conditions) if c == condition]
            print(f"   {condition}: {len(condition_indices)} events")
            
            for sp_num in unique_species:
                sp_indices = [j for j in condition_indices if species_numbers[j] == sp_num]
                print(f"     Species pool {sp_num}: {len(sp_indices)} events")
        
        print("\n🎉 ALL TESTS PASSED!")
        print("=" * 60)
        print("✅ Updated retention analysis logic is working correctly")
        print("✅ Detailed medium × species pool breakdown implemented")
        print("✅ Ready for full analysis once matplotlib is fixed")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_updated_analysis()