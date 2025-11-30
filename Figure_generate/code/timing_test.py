#!/usr/bin/env python3
"""
Quick timing test to estimate 100-repetition runtime
"""

import time
import numpy as np
from scipy.integrate import solve_ivp

def gLV(y, t, I_simul, g_simul, k_simul):
    """Generalized Lotka-Volterra dynamics"""
    dydt = np.zeros_like(y)
    for i in range(len(y)):
        dydt[i] = g_simul[i] * y[i] * (1 - (np.sum(I_simul[i,:] * y) / k_simul[i]))
    return dydt

def run_lotka_volterra(y0, t, s_idx, I, g, k):
    """Run Lotka-Volterra simulation"""
    s_idx = np.where(s_idx)[0].tolist()
    N = len(y0)
    y0_simul = y0[s_idx]
    I_simul = I[s_idx,:]
    I_simul = I_simul[:,s_idx]
    g_simul = g[s_idx]
    k_simul = k[s_idx]
    
    def f(t,y): 
        return gLV(y, t, I_simul, g_simul, k_simul)
    
    y = solve_ivp(f, t, y0_simul, method='RK45', rtol=1e-6)
    y = y.y[:,-1]
    y_out = np.zeros(N)
    for i in range(y.shape[0]):
        y_out[s_idx[i]] = y[i] 
    return y_out

def timing_test():
    """Test timing for a single repetition simulation"""
    
    print("Running timing test for single repetition...")
    
    # Parameters
    N = 48
    num_S = 12
    num_C = 4
    t = [0, 2000]
    threshold = 1e-3
    u = 0.5  # Test with medium interaction
    
    start_time = time.time()
    
    # Single repetition simulation
    np.random.seed(42)
    
    # Initialize species pool
    I = np.random.uniform(0, 2*u, (N, N))
    np.fill_diagonal(I, 1)
    g = np.ones(N)
    k = np.ones(N)
    
    # Create communities
    all_species = np.random.permutation(N)
    CommunitiesLibrary = np.zeros([num_C, N])
    for i in range(num_C):
        start_idx = i * num_S
        end_idx = start_idx + num_S
        selected_species = all_species[start_idx:end_idx]
        CommunitiesLibrary[i, selected_species] = 1
    
    # Initialize abundances
    y = np.random.rand(N) * 0.1
    
    # Run single community simulations
    sc_list = {}
    for idx in range(num_C):
        y1 = run_lotka_volterra(y, t, CommunitiesLibrary[idx, :], I, g, k)
        y1[y1 < threshold] = 0
        sc_list[str(idx)] = y1.tolist()
    
    # Run coalescence simulations
    cc_list = {}
    for idx in range(num_C):
        for jdx in range(idx + 1, num_C):
            y1 = np.array(sc_list[str(idx)])
            y2 = np.array(sc_list[str(jdx)])
            y3 = (y1 + y2) / 2
            
            survived = y3 > threshold
            y3 = run_lotka_volterra(y3, t, survived, I, g, k)
            y3[y3 < threshold] = 0
            
            cc_list[f"{idx}_{jdx}"] = y3.tolist()
    
    end_time = time.time()
    single_rep_time = end_time - start_time
    
    print(f"Single repetition completed in: {single_rep_time:.2f} seconds")
    print(f"Communities simulated: {len(sc_list)}")
    print(f"Coalescence pairs: {len(cc_list)}")
    
    # Extrapolate to 100 repetitions × 3 intensities
    total_reps = 100 * 3
    estimated_total_time = single_rep_time * total_reps
    
    print(f"\n=== TIMING ESTIMATES ===")
    print(f"Single repetition: {single_rep_time:.2f} seconds")
    print(f"100 reps × 3 intensities = {total_reps} total repetitions")
    print(f"Estimated total time: {estimated_total_time:.1f} seconds ({estimated_total_time/60:.1f} minutes)")
    
    # Conservative estimate (add 20% buffer)
    conservative_time = estimated_total_time * 1.2
    print(f"Conservative estimate: {conservative_time:.1f} seconds ({conservative_time/60:.1f} minutes)")
    
    return single_rep_time, estimated_total_time

if __name__ == "__main__":
    timing_test()