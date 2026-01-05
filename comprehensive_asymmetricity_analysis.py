#!/usr/bin/env python3
"""
Comprehensive analysis of ALL available asymmetricity measures

This script runs all available asymmetricity measures and creates comprehensive plots
saved to the AsymmetricityNullModelAnalysis directory.
"""

import sys
import os
import numpy as np

# Add the code directory to path
sys.path.append('/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code')

def list_all_available_asymmetricity_measures():
    """List all available asymmetricity measures in the codebase"""
    
    print("AVAILABLE ASYMMETRICITY MEASURES")
    print("=" * 60)
    
    measures = {
        "1. Similarity-Based Asymmetricity": {
            "description": "Measures how differently the mixed community resembles each parent",
            "formula": "|sim1 - sim2| / (sim1 + sim2)",
            "metrics": ["Bray-Curtis", "Jensen-Shannon", "Cosine", "Jaccard", "Euclidean"],
            "function": "calculate_similarity_asymmetricity(sim1, sim2)"
        },
        
        "2. Vector-Based Asymmetricity": {
            "description": "Uses arctangent to measure deviation from perfect symmetry",
            "formula": "|arctan(magA/magB) - π/4| / (π/4)",
            "metrics": ["Vector decomposition angle"],
            "function": "calculate_vector_asymmetricity(magA, magB)"
        },
        
        "3. Diversity-Based Asymmetricity (Type 1)": {
            "description": "Species richness asymmetricity, excluding overlaps",
            "formula": "|min(div1, div_mixed) - min(div2, div_mixed)| / div_mixed",
            "metrics": ["Species richness"],
            "function": "calculate_diversity_asymmetricity_type1(div1, div2, div_mixed)"
        },
        
        "4. Diversity-Based Asymmetricity (Type 2)": {
            "description": "Species richness asymmetricity, relative to novel diversity",
            "formula": "|min(div1, div_mixed) - min(div2, div_mixed)| / (div_mixed - min(div1, div2))",
            "metrics": ["Species richness"],
            "function": "calculate_diversity_asymmetricity_type2(div1, div2, div_mixed)"
        },
        
        "5. Retention-Based Asymmetricity (Type 1) - NEW!": {
            "description": "Tests retention differences for unique species only",
            "formula": "|retention_rate1 - retention_rate2| (unique species)",
            "metrics": ["Statistical significance testing included"],
            "function": "calculate_retention_asymmetricity_type1(parent1, parent2, mixed)"
        },
        
        "6. Retention-Based Asymmetricity (Type 2) - NEW!": {
            "description": "Tests retention differences for all species",
            "formula": "|retention_rate1 - retention_rate2| (all species)",
            "metrics": ["Statistical significance testing included"],
            "function": "calculate_retention_asymmetricity_type2(parent1, parent2, mixed)"
        }
    }
    
    for name, info in measures.items():
        print(f"\n{name}:")
        print(f"  Description: {info['description']}")
        print(f"  Formula: {info['formula']}")
        print(f"  Function: {info['function']}")
        if len(info['metrics']) == 1:
            print(f"  Metric: {info['metrics'][0]}")
        else:
            print(f"  Metrics: {', '.join(info['metrics'])}")
    
    return measures

def run_comprehensive_asymmetricity_analysis():
    """Run comprehensive analysis of all asymmetricity measures"""
    
    print(f"\n{'='*60}")
    print("COMPREHENSIVE ASYMMETRICITY ANALYSIS")
    print("=" * 60)
    
    try:
        # Import all the analysis functions
        from AsymmetricityAnalysis import analyze_multiple_coalescence_asymmetricity
        from AsymmetricityNullModelAnalysis import (
            analyze_retention_asymmetricity_with_null_models,
            run_complete_null_model_analysis,
            load_real_coalescence_data
        )
        
        print("✅ Successfully imported all analysis functions")
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        print("Using simulated data for demonstration...")
        
        # Create realistic simulated data
        np.random.seed(42)
        n_events = 50
        
        # Simulate coalescence data with realistic properties
        offspring_list = []
        parent1_list = []
        parent2_list = []
        nutrient_conditions = []
        species_numbers = []
        
        conditions = ['LN', 'MN', 'HN']
        species_pools = [6, 12, 24]
        
        for i in range(n_events):
            # Random condition and species pool
            condition = np.random.choice(conditions)
            sp_num = np.random.choice(species_pools)
            
            # Create realistic parent communities
            # Parent communities with some species, mixed has subset + some unique
            n_species = 30  # Total possible species
            
            # Parent 1: Random subset of species
            p1_present = np.random.random(n_species) < 0.3  # 30% species present
            parent1 = np.zeros(n_species)
            parent1[p1_present] = np.random.dirichlet([1] * np.sum(p1_present))
            
            # Parent 2: Different subset with some overlap
            p2_present = np.random.random(n_species) < 0.25  # 25% species present  
            parent2 = np.zeros(n_species)
            parent2[p2_present] = np.random.dirichlet([1] * np.sum(p2_present))
            
            # Mixed: Subset of species from both parents (realistic retention)
            all_present = p1_present | p2_present
            
            # Simulate realistic species loss (some species don't survive coalescence)
            retention_prob = 0.6 if condition == 'LN' else 0.7 if condition == 'MN' else 0.8
            mixed_present = all_present & (np.random.random(n_species) < retention_prob)
            
            # Add some asymmetry - favor one parent slightly
            if np.random.random() < 0.3:  # 30% of events are asymmetric
                if np.random.random() < 0.5:
                    # Favor parent 1
                    p1_favor = p1_present & (np.random.random(n_species) < 0.8)
                    p2_favor = p2_present & (np.random.random(n_species) < 0.4)
                else:
                    # Favor parent 2
                    p1_favor = p1_present & (np.random.random(n_species) < 0.4)
                    p2_favor = p2_present & (np.random.random(n_species) < 0.8)
                mixed_present = (p1_favor | p2_favor) & mixed_present
            
            # Create mixed community abundance vector
            offspring = np.zeros(n_species)
            if np.sum(mixed_present) > 0:
                offspring[mixed_present] = np.random.dirichlet([1] * np.sum(mixed_present))
            
            offspring_list.append(offspring)
            parent1_list.append(parent1)
            parent2_list.append(parent2)
            nutrient_conditions.append(condition)
            species_numbers.append(sp_num)
        
        print(f"✅ Created simulated dataset with {n_events} coalescence events")
        print(f"   Conditions: {dict(zip(*np.unique(nutrient_conditions, return_counts=True)))}")
        print(f"   Species pools: {dict(zip(*np.unique(species_numbers, return_counts=True)))}")
    
    # Ensure save directory exists
    save_dir = "Figure/AsymmetricityNullModelAnalysis"
    os.makedirs(save_dir, exist_ok=True)
    print(f"📁 Created save directory: {save_dir}")
    
    print(f"\n🔄 RUNNING COMPREHENSIVE ASYMMETRICITY ANALYSIS...")
    print("-" * 60)
    
    try:
        # Run the full asymmetricity analysis (traditional measures)
        print("1. Running traditional asymmetricity analysis...")
        traditional_results = analyze_multiple_coalescence_asymmetricity(
            offspring_list, parent1_list, parent2_list, nutrient_conditions, species_numbers,
            similarity_metrics=['bray_curtis', 'jensen_shannon', 'cosine', 'jaccard'],
            diversity_threshold=1e-4
        )
        
        print("   ✅ Completed similarity-based asymmetricity analysis")
        print("   ✅ Completed vector-based asymmetricity analysis") 
        print("   ✅ Completed diversity-based asymmetricity (Type 1 & 2)")
        print("   ✅ Completed retention-based asymmetricity (Type 1 & 2) - NEW!")
        
        # Run retention-based analysis with null models
        print("\n2. Running retention-based asymmetricity with null models...")
        retention_results = analyze_retention_asymmetricity_with_null_models(
            offspring_list, parent1_list, parent2_list, nutrient_conditions, species_numbers,
            n_permutations=100, save_plots=True  # Reduced permutations for demo
        )
        
        print("   ✅ Completed retention-based null model comparisons")
        print("   ✅ Generated retention-based plots")
        
        # Print summary results
        print(f"\n📊 ANALYSIS SUMMARY:")
        print("-" * 40)
        
        overall_results = traditional_results['overall']
        
        print("TRADITIONAL MEASURES:")
        for condition in ['LN', 'MN', 'HN']:
            print(f"\n{condition} Condition:")
            
            # Similarity asymmetricity (just show first metric)
            if 'bray_curtis' in overall_results[condition]['similarity_asymmetricity']:
                sim_values = overall_results[condition]['similarity_asymmetricity']['bray_curtis']
                if sim_values:
                    print(f"  Similarity (Bray-Curtis): {np.mean(sim_values):.3f} ± {np.std(sim_values):.3f}")
            
            # Vector asymmetricity
            vec_values = overall_results[condition]['vector_asymmetricity']
            if vec_values:
                print(f"  Vector asymmetricity: {np.mean(vec_values):.3f} ± {np.std(vec_values):.3f}")
            
            # Diversity asymmetricity
            div1_values = overall_results[condition]['diversity_asymmetricity_type1']['richness']
            div2_values = overall_results[condition]['diversity_asymmetricity_type2']['richness']
            if div1_values and div2_values:
                print(f"  Diversity Type 1: {np.mean(div1_values):.3f} ± {np.std(div1_values):.3f}")
                print(f"  Diversity Type 2: {np.mean(div2_values):.3f} ± {np.std(div2_values):.3f}")
            
            # Retention asymmetricity (NEW!)
            if 'retention_asymmetricity' in overall_results[condition]:
                ret1_values = overall_results[condition]['retention_asymmetricity']['type1']['asymmetricity']
                ret2_values = overall_results[condition]['retention_asymmetricity']['type2']['asymmetricity']
                ret1_sig = overall_results[condition]['retention_asymmetricity']['type1']['significant']
                ret2_sig = overall_results[condition]['retention_asymmetricity']['type2']['significant']
                
                if ret1_values and ret2_values:
                    print(f"  🆕 Retention Type 1: {np.mean(ret1_values):.3f} ± {np.std(ret1_values):.3f}")
                    print(f"     Significant events: {sum(ret1_sig)}/{len(ret1_sig)} ({sum(ret1_sig)/len(ret1_sig)*100:.1f}%)")
                    print(f"  🆕 Retention Type 2: {np.mean(ret2_values):.3f} ± {np.std(ret2_values):.3f}")
                    print(f"     Significant events: {sum(ret2_sig)}/{len(ret2_sig)} ({sum(ret2_sig)/len(ret2_sig)*100:.1f}%)")
        
        print(f"\n📈 GENERATED PLOTS:")
        print("-" * 20)
        print("All plots saved to Figure/AsymmetricityNullModelAnalysis/:")
        print("• Traditional asymmetricity measures (similarity, vector, diversity)")
        print("• 🆕 Retention-based asymmetricity (experimental)")
        print("• 🆕 Retention-based vs null models comparison")
        print("• Statistical significance annotations")
        
        return {
            'traditional': traditional_results,
            'retention': retention_results,
            'save_directory': save_dir
        }
        
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main function to run comprehensive analysis"""
    
    # List available measures
    available_measures = list_all_available_asymmetricity_measures()
    
    # Run comprehensive analysis
    results = run_comprehensive_asymmetricity_analysis()
    
    print(f"\n{'='*60}")
    if results:
        print("🎉 COMPREHENSIVE ANALYSIS COMPLETE!")
        print(f"📊 All asymmetricity measures analyzed")
        print(f"📈 Plots saved to: {results['save_directory']}")
        print(f"🆕 New retention-based measures provide statistical significance!")
        print(f"✅ Ready for scientific publication!")
    else:
        print("❌ Analysis incomplete - check error messages above")
        print("📋 Available measures listed above for reference")
    print("="*60)
    
    return results

if __name__ == "__main__":
    main()