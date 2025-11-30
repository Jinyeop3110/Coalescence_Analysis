#!/usr/bin/env python3
"""
Generate vector decomposition map with coalescence trajectories
Shows how mixed communities evolve from (1/sqrt(2), 1/sqrt(2)) during coalescence
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
from scipy.integrate import solve_ivp
from scipy.ndimage import gaussian_filter
import os
import sys

# Add path for importing modules
sys.path.append('/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/Main_Fig_2')

# Import the LV dynamics
from LV import gLV
from InitializeSpeciesPool import InitializeSpeceiesPool

# Set up plotting parameters
mm = 0.1/2.54
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['figure.dpi'] = 300
mpl.rcParams['font.size'] = 8
mpl.rcParams['axes.linewidth'] = 0.5

# Output directory
dynamics_dir = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code/Figure/Dynamics"
os.makedirs(dynamics_dir, exist_ok=True)

def normalize(v):
    """Normalize vector"""
    norm = np.linalg.norm(v)
    if norm == 0:
       return v
    return v / norm

def metric_VectorDecomposition_onlyPositive(u, v, m):
    """Vector decomposition metric - projects mixed community onto basis of parent communities"""
    u = normalize(u)
    v = normalize(v)
    m = normalize(m)

    A = np.array([[np.sum(u*u), np.sum(u*v)], [np.sum(u*v), np.sum(v*v)]])

    try:
        e12 = np.matmul(np.linalg.inv(A), np.array([np.sum(m*u), np.sum(m*v)]))
    except np.linalg.LinAlgError:
        return 0, 0, 1

    x1 = (e12[0]) * (e12[0] > 0)
    x2 = (e12[1]) * (e12[1] > 0)
    x3 = np.linalg.norm(m - (e12[0]*u) - (e12[1]*v))

    if x1**2 + x2**2 == 0:
        return 0, 0, x3

    try:
        convert = np.sqrt((1 - x3**2) / (x1**2 + x2**2))
    except:
        return x1, x2, x3

    return convert*x1, convert*x2, x3

def uniform_distribution(u, o):
    """Generate uniform distribution for interaction matrix"""
    return (2*u + 2*o) * np.random.random() - o

def run_lotka_volterra_dynamics_full(y0, t_span, t_eval, s_idx, I, g, k):
    """Run LV dynamics and return full time series"""
    s_idx = np.where(s_idx)[0].tolist()
    N = len(y0)
    y0_simul = y0[s_idx]
    I_simul = I[s_idx, :]
    I_simul = I_simul[:, s_idx]
    g_simul = g[s_idx]
    k_simul = k[s_idx]

    def f(t, y):
        return gLV(y, t, I_simul, g_simul, k_simul)

    result = solve_ivp(f, t_span, y0_simul, t_eval=t_eval, method='RK45')

    # Map back to full species space
    y_out = np.zeros((N, len(t_eval)))
    for i, idx in enumerate(s_idx):
        y_out[idx, :] = result.y[i, :]

    return y_out

def run_coalescence_with_trajectory(I, g, k, num_C, num_S, threshold=1e-3, seed=None):
    """
    Run a single coalescence simulation and track vector decomposition trajectory

    Returns:
        trajectory: list of (u, v) coordinates at different time points
        final_state: final (u, v, k) coordinates
    """
    if seed is not None:
        np.random.seed(seed)

    N = num_C * num_S

    # Create community library
    CommunitiesLibrary = np.zeros([num_C, N])
    for i in range(num_C):
        CommunitiesLibrary[i, np.arange(num_S*i, num_S*(i+1))] = 1

    # Time points - focus on early dynamics (log-spaced)
    t_final = 5000
    t_span = (0, t_final)
    # More time points in early phase
    t_eval = np.concatenate([
        np.linspace(0, 100, 20),
        np.linspace(100, 500, 15)[1:],  # Skip duplicate at 100
        np.linspace(500, 2000, 15)[1:],  # Skip duplicate at 500
        np.linspace(2000, t_final, 10)[1:]  # Skip duplicate at 2000
    ])

    # Initial conditions
    y0 = np.random.rand(N) * 0.1

    # Run individual communities to equilibrium
    c1_result = run_lotka_volterra_dynamics_full(y0, t_span, [t_final],
                                                   CommunitiesLibrary[0, :], I, g, k)
    c2_result = run_lotka_volterra_dynamics_full(y0, t_span, [t_final],
                                                   CommunitiesLibrary[1, :], I, g, k)

    # Get equilibrium states
    y1 = c1_result[:, -1]
    y2 = c2_result[:, -1]

    # Apply threshold
    y1[y1 < threshold] = 0
    y2[y2 < threshold] = 0

    # Check if both communities survived
    if np.sum(y1 > 0) == 0 or np.sum(y2 > 0) == 0:
        return None, None

    # Mixed community initial conditions - combine the two communities
    # Both y1 and y2 have all N species, but different ones are non-zero
    y3 = y1 + y2  # Add them together (non-overlapping species)
    survived = y3 > threshold

    # Run mixed community dynamics with multiple time points
    c3_results = run_lotka_volterra_dynamics_full(y3, t_span, t_eval, survived, I, g, k)

    # Calculate vector decomposition trajectory
    trajectory = []
    for t_idx in range(len(t_eval)):
        c_mix_t = c3_results[:, t_idx]
        c_mix_t[c_mix_t < threshold] = 0

        if np.sum(c_mix_t > 0) > 0:
            u_coord, v_coord, k_coord = metric_VectorDecomposition_onlyPositive(y1, y2, c_mix_t)

            if not (np.isnan(u_coord) or np.isnan(v_coord)):
                trajectory.append((t_eval[t_idx], u_coord, v_coord, k_coord))

    if len(trajectory) > 0:
        final_u, final_v, final_k = trajectory[-1][1], trajectory[-1][2], trajectory[-1][3]
        return trajectory, (final_u, final_v, final_k)

    return None, None

def create_radial_density_field(u_coords, v_coords, r_bins=50, theta_bins=50, smoothing_sigma=8.0):
    """Create smooth density field using radial coordinates"""
    # Convert to radial coordinates
    r = np.sqrt(u_coords**2 + v_coords**2)
    theta = np.arctan2(v_coords, u_coords)
    theta = np.abs(theta)
    theta = np.minimum(theta, np.pi/2)

    # Create 2D histogram in radial space
    r_max = 1.0
    theta_max = np.pi/2

    H_radial, r_edges, theta_edges = np.histogram2d(
        r, theta,
        bins=[r_bins, theta_bins],
        range=[[0, r_max], [0, theta_max]]
    )

    # Apply Gaussian smoothing
    H_smooth = gaussian_filter(H_radial, sigma=smoothing_sigma)

    # Normalize
    H_norm = H_smooth / np.max(H_smooth) if np.max(H_smooth) > 0 else H_smooth

    return H_norm, r_edges, theta_edges

def main():
    """Generate vector decomposition map with trajectories"""
    print("="*80)
    print("GENERATING VECTOR DECOMPOSITION MAP WITH COALESCENCE TRAJECTORIES")
    print("="*80)

    # Parameters
    u = 0.6  # Interaction strength
    num_C = 2  # Number of communities
    num_S = 12  # Species per community
    N = num_C * num_S
    num_reps = 100  # Number of trajectories to plot

    print(f"\nParameters:")
    print(f"  Interaction strength (u): {u}")
    print(f"  Communities: {num_C}")
    print(f"  Species per community: {num_S}")
    print(f"  Total species: {N}")
    print(f"  Number of trajectories: {num_reps}")

    # Initialize species pool
    print(f"\nInitializing species pool...")
    f_interaction = lambda: uniform_distribution(u, 0)

    # Create temporary directory for species pool data
    temp_dir = f"{dynamics_dir}/temp_species_pool"
    os.makedirs(temp_dir, exist_ok=True)

    I, g, k = InitializeSpeceiesPool(
        N, f_interaction,
        f_g=lambda: np.ones(1),
        f_k=lambda: np.ones(1),
        is_diagonal_one=True,
        save_path=temp_dir
    )

    print(f"✅ Species pool initialized")

    # Run simulations and collect trajectories
    print(f"\nRunning {num_reps} coalescence simulations...")
    all_trajectories = []
    all_final_u = []
    all_final_v = []

    for rep in range(num_reps):
        if (rep + 1) % 20 == 0:
            print(f"  Completed {rep + 1}/{num_reps} simulations...")

        trajectory, final = run_coalescence_with_trajectory(
            I, g, k, num_C, num_S, seed=rep*42
        )

        if trajectory is not None and final is not None:
            all_trajectories.append(trajectory)
            all_final_u.append(final[0])
            all_final_v.append(final[1])

    print(f"✅ Completed {len(all_trajectories)} successful simulations")

    # Create background density field from final points
    all_final_u = np.array(all_final_u)
    all_final_v = np.array(all_final_v)

    print(f"\nCreating background density field...")
    H_radial, r_edges, theta_edges = create_radial_density_field(
        all_final_u, all_final_v,
        r_bins=50, theta_bins=50,
        smoothing_sigma=8.0
    )

    # Create the plot
    print(f"\nCreating vector decomposition plot with trajectories...")

    fig, ax = plt.subplots(1, figsize=(100*mm, 100*mm), facecolor='w')

    # Plot background density as contours
    u_grid = np.linspace(0, 1, 100)
    v_grid = np.linspace(0, 1, 100)
    U, V = np.meshgrid(u_grid, v_grid)

    # Convert radial density back to cartesian for plotting
    R_grid = np.sqrt(U**2 + V**2)
    Theta_grid = np.arctan2(V, U)

    r_centers = (r_edges[:-1] + r_edges[1:]) / 2
    theta_centers = (theta_edges[:-1] + theta_edges[1:]) / 2

    density_uv = np.zeros((100, 100))
    for i in range(100):
        for j in range(100):
            r_val = R_grid[j, i]
            theta_val = Theta_grid[j, i]

            if theta_val >= 0 and theta_val <= np.pi/2 and r_val <= 1.0:
                r_idx = np.argmin(np.abs(r_centers - r_val))
                theta_idx = np.argmin(np.abs(theta_centers - theta_val))

                if r_idx < H_radial.shape[0] and theta_idx < H_radial.shape[1]:
                    density_uv[j, i] = H_radial[r_idx, theta_idx]

    # Plot density as filled contours
    levels = np.linspace(0.1, 1.0, 10)
    contourf = ax.contourf(U, V, density_uv, levels=levels, cmap='Greys', alpha=0.3)

    # Plot trajectories
    print(f"  Plotting {len(all_trajectories)} trajectories...")

    # Color trajectories by time
    cmap = plt.cm.viridis

    for traj_idx, trajectory in enumerate(all_trajectories):
        # Extract u, v coordinates
        times = np.array([t[0] for t in trajectory])
        u_traj = np.array([t[1] for t in trajectory])
        v_traj = np.array([t[2] for t in trajectory])

        # Plot trajectory as a line with color gradient
        # Use alpha to show overlap
        ax.plot(u_traj, v_traj, linewidth=0.5, alpha=0.4, color='royalblue')

        # Mark starting point (should be near 1/sqrt(2), 1/sqrt(2))
        if traj_idx < 10:  # Only mark first 10 to avoid clutter
            ax.plot(u_traj[0], v_traj[0], 'o', markersize=3,
                   color='lime', alpha=0.6, markeredgewidth=0)

        # Mark ending point
        if traj_idx < 10:
            ax.plot(u_traj[-1], v_traj[-1], 's', markersize=3,
                   color='red', alpha=0.6, markeredgewidth=0)

    # Mark the theoretical starting point
    sqrt2_inv = 1.0 / np.sqrt(2)
    ax.plot(sqrt2_inv, sqrt2_inv, '*', markersize=12,
           color='lime', markeredgecolor='black', markeredgewidth=0.5,
           label=f'Initial state\n({sqrt2_inv:.3f}, {sqrt2_inv:.3f})', zorder=10)

    # Add diagonal line
    ax.plot([0, 1], [0, 1], 'k--', linewidth=1, alpha=0.5, label='u = v')

    # Add axes lines
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)

    # Set limits and labels
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel('u (contribution from community 1)', fontsize=10)
    ax.set_ylabel('v (contribution from community 2)', fontsize=10)
    ax.set_title(f'Coalescence Trajectories (u = {u}, n = {len(all_trajectories)})',
                fontsize=11, fontweight='bold')

    # Add grid
    ax.grid(True, alpha=0.3, linewidth=0.5)

    # Set aspect ratio to equal
    ax.set_aspect('equal')

    # Add legend
    ax.legend(loc='upper right', fontsize=8, framealpha=0.9)

    # Save figure
    output_file = f'{dynamics_dir}/VectorDecomp_u{u}_trajectories.svg'
    fig.savefig(output_file, bbox_inches='tight', dpi=300)
    plt.close()

    print(f"✅ Created: {output_file}")

    # Create a second plot focusing on individual trajectories (subsample)
    print(f"\nCreating detailed trajectory plot (subsample)...")

    fig2, ax2 = plt.subplots(1, figsize=(100*mm, 100*mm), facecolor='w')

    # Plot only 20 trajectories for clarity
    n_show = min(20, len(all_trajectories))
    cmap = plt.cm.plasma

    for traj_idx in range(n_show):
        trajectory = all_trajectories[traj_idx]
        times = np.array([t[0] for t in trajectory])
        u_traj = np.array([t[1] for t in trajectory])
        v_traj = np.array([t[2] for t in trajectory])

        # Color by trajectory index
        color = cmap(traj_idx / n_show)

        # Plot trajectory
        ax2.plot(u_traj, v_traj, '-', linewidth=1.5, alpha=0.7, color=color)

        # Mark start and end
        ax2.plot(u_traj[0], v_traj[0], 'o', markersize=6,
                color=color, alpha=0.8, markeredgewidth=0.5, markeredgecolor='black')
        ax2.plot(u_traj[-1], v_traj[-1], 's', markersize=6,
                color=color, alpha=0.8, markeredgewidth=0.5, markeredgecolor='black')

    # Mark theoretical starting point
    ax2.plot(sqrt2_inv, sqrt2_inv, '*', markersize=15,
            color='lime', markeredgecolor='black', markeredgewidth=1,
            label=f'Expected start\n({sqrt2_inv:.3f}, {sqrt2_inv:.3f})', zorder=10)

    # Add diagonal
    ax2.plot([0, 1], [0, 1], 'k--', linewidth=1, alpha=0.5, label='u = v')

    # Set limits and labels
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.set_xlabel('u (contribution from community 1)', fontsize=10)
    ax2.set_ylabel('v (contribution from community 2)', fontsize=10)
    ax2.set_title(f'Individual Coalescence Trajectories (u = {u}, n = {n_show})',
                 fontsize=11, fontweight='bold')

    ax2.grid(True, alpha=0.3, linewidth=0.5)
    ax2.set_aspect('equal')
    ax2.legend(loc='upper right', fontsize=8, framealpha=0.9)

    # Save second figure
    output_file2 = f'{dynamics_dir}/VectorDecomp_u{u}_trajectories_detailed.svg'
    fig2.savefig(output_file2, bbox_inches='tight', dpi=300)
    plt.close()

    print(f"✅ Created: {output_file2}")

    # Print summary statistics
    print(f"\n" + "="*80)
    print(f"SUMMARY STATISTICS")
    print(f"="*80)
    print(f"Successful simulations: {len(all_trajectories)}/{num_reps}")
    print(f"\nFinal u coordinates:")
    print(f"  Mean: {np.mean(all_final_u):.3f} ± {np.std(all_final_u):.3f}")
    print(f"  Range: [{np.min(all_final_u):.3f}, {np.max(all_final_u):.3f}]")
    print(f"\nFinal v coordinates:")
    print(f"  Mean: {np.mean(all_final_v):.3f} ± {np.std(all_final_v):.3f}")
    print(f"  Range: [{np.min(all_final_v):.3f}, {np.max(all_final_v):.3f}]")

    # Check deviation from diagonal
    u_minus_v = all_final_u - all_final_v
    print(f"\nDeviation from diagonal (u - v):")
    print(f"  Mean: {np.mean(u_minus_v):.3f} ± {np.std(u_minus_v):.3f}")

    print(f"\n📁 Output directory: {dynamics_dir}")
    print(f"📊 Generated files:")
    print(f"   - VectorDecomp_u{u}_trajectories.svg")
    print(f"   - VectorDecomp_u{u}_trajectories_detailed.svg")
    print("="*80)

if __name__ == "__main__":
    main()
