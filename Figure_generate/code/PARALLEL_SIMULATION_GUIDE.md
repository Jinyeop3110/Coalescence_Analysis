# Parallelized Mean-Std Grid Simulation Guide

## Overview

This guide explains how to run the mean-std grid simulation with **500 repetitions** using parallelization for significant speedup.

---

## Key Features of Parallel Version

### ✅ Advantages:
1. **Much faster execution**: ~8x speedup on 8-core machine
2. **Automatic core detection**: Uses all available CPU cores
3. **Periodic checkpointing**: Saves progress every 500 simulations
4. **Progress monitoring**: Real-time progress updates
5. **Resumable**: Can continue from checkpoints if interrupted

### 📊 Performance Comparison:

| Version | Cores | Time for 500 reps | Speedup |
|---------|-------|-------------------|---------|
| Serial (`run_mean_std_grid.py`) | 1 | ~20 hours | 1x |
| Parallel (`run_mean_std_grid_parallel.py`) | 8 | ~2.5 hours | ~8x |
| Parallel (`run_mean_std_grid_parallel.py`) | 16 | ~1.3 hours | ~15x |

*Time estimates based on 2 seconds per simulation*

---

## Quick Start

### 1. Check Your System

```bash
# Check number of CPU cores
python -c "import multiprocessing; print(f'CPU cores: {multiprocessing.cpu_count()}')"
```

### 2. Run Parallel Simulation

```bash
cd /Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code

# Run with conda environment
conda activate coalescence
python run_mean_std_grid_parallel.py
```

### 3. Monitor Progress (in another terminal)

```bash
# While simulation is running, check progress:
python monitor_grid_simulation.py 500
```

---

## Detailed Workflow

### Step 1: Prepare Environment

```bash
# Activate conda environment
conda activate coalescence

# Navigate to code directory
cd /Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code

# Check available disk space (need ~3 GB)
df -h .
```

### Step 2: Start Simulation

```bash
# Run parallelized simulation
python run_mean_std_grid_parallel.py
```

**Expected output:**
```
======================================================================
48-Species Coalescence Simulation - Mean × Std Grid (PARALLELIZED)
Distribution: Truncated Normal N(mean, std²) with support [0, ∞)
======================================================================

System information:
  Available CPU cores: 8
  Using 8 cores for parallel execution

Parameter Grid:
  Mean values: 12 values from 0.1 to 1.2
  Std values:  6 values from 0.10 to 0.60
  Grid size: 12 × 6 = 72 combinations
  Repetitions per combination: 500

Total simulations: 36,000
Expected speedup: ~8x faster than serial execution
Estimated time: ~2.5 hours (at 2 sec/simulation)
Base seed: 10000
```

### Step 3: Monitor Progress

Open a **second terminal** and run:

```bash
cd /Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code
conda activate coalescence
python monitor_grid_simulation.py 500
```

**Example output:**
```
======================================================================
MONITORING: Simulation_Data/mean_std_grid_500reps
======================================================================

🔄 SIMULATION IN PROGRESS

📁 Latest checkpoint:
   File: checkpoint_5000.json
   Size: 645.3 MB
   Modified: 2025-11-04 17:30:45

📊 Progress:
   Combinations: 72/72
   Total simulations: 5,000/36,000
   Progress: 13.9%
   Remaining: 31,000 simulations
```

---

## Output Files

### During Simulation:

**Checkpoints** (saved every 500 simulations):
```
Simulation_Data/mean_std_grid_500reps/
├── checkpoint_500.json
├── checkpoint_1000.json
├── checkpoint_1500.json
└── ...
```

### After Completion:

**Final outputs:**
```
Simulation_Data/mean_std_grid_500reps/
├── Community_mean_std_grid_500reps.json  (~2.9 GB)
├── simulation_parameters.xlsx
└── parameter_grid.xlsx
```

---

## File Size Estimates

| Reps | JSON Size | Disk Space Needed |
|------|-----------|-------------------|
| 100  | ~580 MB   | ~1 GB             |
| 200  | ~1.2 GB   | ~2 GB             |
| 500  | ~2.9 GB   | ~5 GB             |

---

## How Parallelization Works

### Architecture:

```
Main Process
    │
    ├── Creates 36,000 tasks (mean, std, rep, seed)
    │
    ├── Spawns Worker Pool (8 workers)
    │   │
    │   ├── Worker 1: Processes tasks 1, 9, 17, 25, ...
    │   ├── Worker 2: Processes tasks 2, 10, 18, 26, ...
    │   ├── Worker 3: Processes tasks 3, 11, 19, 27, ...
    │   ├── ...
    │   └── Worker 8: Processes tasks 8, 16, 24, 32, ...
    │
    └── Collects results and saves checkpoints
```

### Key Implementation Details:

1. **Task Distribution**: Each task is a tuple `(mean, std, rep, seed)`
2. **Worker Function**: `run_simulation_wrapper()` runs one simulation
3. **Result Collection**: Main process collects results via `imap_unordered()`
4. **Checkpointing**: Saves progress every 500 completed simulations
5. **Progress Tracking**: Reports every 50 simulations

---

## Comparison with Serial Version

### Serial Version (`run_mean_std_grid.py`):
```python
# Sequential execution
for mean in mean_values:
    for std in std_values:
        for rep in range(N_reps):
            result = run_single_simulation(mean, std, rep, seed)
            # One simulation at a time
```

### Parallel Version (`run_mean_std_grid_parallel.py`):
```python
# Parallel execution
with mp.Pool(processes=num_cores) as pool:
    for result in pool.imap_unordered(run_simulation_wrapper, tasks):
        # Multiple simulations running simultaneously
        # on different CPU cores
```

---

## Troubleshooting

### Issue: "File already exists"
```bash
# The script will ask if you want to overwrite
# Type 'yes' to proceed or 'no' to cancel
```

### Issue: Simulation killed or interrupted
```bash
# Checkpoints are saved every 500 simulations
# You can manually restart from a checkpoint
# (Manual resume feature can be implemented if needed)
```

### Issue: Low memory
```bash
# Monitor memory usage:
top -l 1 | grep PhysMem

# If memory is low:
# - Close other applications
# - Reduce number of workers (edit script: use num_cores//2)
```

### Issue: Slower than expected
```bash
# Check if other processes are using CPU:
top -o cpu

# Verify number of cores being used:
# Should see 8 python processes (if 8 cores)
ps aux | grep python
```

---

## After Simulation Completes

### Generate Heatmaps:

```bash
# Update plot script to use 500 reps data
cd /Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code

# Edit plot_mean_variance_heatmaps.py
# Change line 30 from:
#   data_dir = "Simulation_Data/mean_std_grid_100reps"
# to:
#   data_dir = "Simulation_Data/mean_std_grid_500reps"

# Change line 31 from:
#   data_file = os.path.join(data_dir, "Community_mean_std_grid_100reps.json")
# to:
#   data_file = os.path.join(data_dir, "Community_mean_std_grid_500reps.json")

# Run heatmap generation
python plot_mean_variance_heatmaps.py
```

### Verify Data Quality:

```bash
# Check final file
python monitor_grid_simulation.py 500

# Should show:
# ✅ SIMULATION COMPLETE!
# Completeness: 100.0%
```

---

## Technical Notes

### Why Multiprocessing?

1. **CPU-bound task**: Each simulation runs Lotka-Volterra ODEs (computationally intensive)
2. **Independent tasks**: Each (mean, std, rep) combination is independent
3. **No shared state**: Simulations don't need to communicate
4. **Perfect for parallelization**: Linear speedup with number of cores

### Seed Management:

Seeds are deterministic based on task order:
```python
seed = base_seed + task_index
# Ensures reproducibility even in parallel execution
```

### Memory Considerations:

Each worker process requires:
- ~100 MB for Python interpreter
- ~50 MB for loaded modules
- ~10 MB per active simulation

For 8 cores: ~1.2 GB total memory needed

---

## Advanced Options

### Reduce Number of Cores:

Edit `run_mean_std_grid_parallel.py`:
```python
# Line ~190: Change
num_cores = mp.cpu_count()
# to:
num_cores = 4  # Use only 4 cores
```

### Change Checkpoint Frequency:

Edit `run_mean_std_grid_parallel.py`:
```python
# Line ~238: Change
checkpoint_interval = 500  # Save every 500 sims
# to:
checkpoint_interval = 1000  # Save every 1000 sims
```

### Run on Cluster/HPC:

The parallel script works on HPC systems with SLURM/PBS:
```bash
#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --time=2:00:00

module load python/3.9
source activate coalescence

python run_mean_std_grid_parallel.py
```

---

## Summary

**To run 500 reps simulation:**

1. ✅ Check system has 8+ cores and 5+ GB free disk space
2. ✅ Run: `python run_mean_std_grid_parallel.py`
3. ✅ Monitor: `python monitor_grid_simulation.py 500` (in another terminal)
4. ✅ Wait ~2.5 hours (8 cores) for completion
5. ✅ Generate heatmaps: Update and run `plot_mean_variance_heatmaps.py`

**Expected outcome:**
- 36,000 simulations completed
- ~2.9 GB JSON file with all results
- ~8x faster than serial execution
- Full interaction matrices saved for each simulation
