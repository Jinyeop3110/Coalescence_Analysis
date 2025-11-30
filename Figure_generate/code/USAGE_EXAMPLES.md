# Usage Examples: Gamma Distribution Simulations

## Quick Start

### 1. Test the Implementation (Fast - 2 minutes)
```bash
conda activate coalescence
cd /Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Figure_generate/code

# Run with just 2 parameter combinations, 5 reps
python run_simulation_WITH_GAMMA.py --means 0.3 0.5 --cvs 0.5 --reps 5
```

### 2. Match Existing Uniform Distribution
```bash
# This should give similar results to uniform u=0.5
python run_simulation_WITH_GAMMA.py \
  --distribution gamma \
  --means 0.5 \
  --cvs 0.577 \
  --reps 10
```

### 3. Explore Variance at Fixed Mean (Recommended First Experiment)
```bash
# Test how variance affects outcomes at mean=0.5
python run_simulation_WITH_GAMMA.py \
  --distribution gamma \
  --means 0.5 0.5 0.5 \
  --cvs 0.2 0.5 1.0 \
  --reps 10

# This creates 3 datasets with same mean (0.5) but different variances:
# - CV=0.2: std=0.10 (tight)
# - CV=0.5: std=0.25 (moderate)
# - CV=1.0: std=0.50 (wide)
```

### 4. Full Parameter Sweep (Like your 200 reps study)
```bash
# 24 mean values × 10 reps = 240 simulations (~20 minutes)
python run_simulation_WITH_GAMMA.py \
  --distribution gamma \
  --means 0.05 0.10 0.15 0.20 0.25 0.30 0.35 0.40 0.45 0.50 \
          0.55 0.60 0.65 0.70 0.75 0.80 0.85 0.90 0.95 1.00 \
          1.05 1.10 1.15 1.20 \
  --cvs 0.577 \
  --reps 10
```

---

## Experimental Designs

### Experiment A: Verify Gamma Matches Uniform
**Question:** Does gamma with CV=0.577 reproduce uniform results?

```bash
# 1. Run uniform baseline
python run_simulation_WITH_GAMMA.py \
  --distribution uniform \
  --means 0.3 0.5 0.8 \
  --reps 10

# 2. Run gamma with matched CV
python run_simulation_WITH_GAMMA.py \
  --distribution gamma \
  --means 0.3 0.5 0.8 \
  --cvs 0.577 \
  --reps 10

# 3. Compare phase diagrams (TODO: create comparison plotting script)
```

**Expected:** Nearly identical phase diagrams

---

### Experiment B: Effect of Variance at Fixed Mean
**Question:** At the same average interaction strength, does variance matter?

```bash
# Test at mean=0.5 with 5 different CV values
python run_simulation_WITH_GAMMA.py \
  --distribution gamma \
  --means 0.5 0.5 0.5 0.5 0.5 \
  --cvs 0.2 0.4 0.6 1.0 1.5 \
  --reps 20

# This gives:
# CV=0.2: Very predictable interactions (std=0.10)
# CV=0.4: Moderately variable (std=0.20)
# CV=0.6: Uniform-like (std=0.30)
# CV=1.0: High variability (std=0.50)
# CV=1.5: Very high variability (std=0.75)
```

**Hypotheses to test:**
- Low CV → More deterministic outcomes (dominance or clear mixing)
- High CV → More variable outcomes (restructuring more common?)
- Threshold CV where behavior changes dramatically?

---

### Experiment C: 2D Parameter Space
**Question:** How do mean AND variance jointly affect coalescence?

```bash
# Grid: 3 means × 3 CVs = 9 combinations
python run_simulation_WITH_GAMMA.py \
  --distribution gamma \
  --means 0.3 0.3 0.3 0.5 0.5 0.5 0.8 0.8 0.8 \
  --cvs 0.2 0.577 1.0 0.2 0.577 1.0 0.2 0.577 1.0 \
  --reps 10

# This creates a 3×3 grid:
#           CV=0.2    CV=0.577   CV=1.0
# mean=0.3  [data]    [data]     [data]
# mean=0.5  [data]    [data]     [data]
# mean=0.8  [data]    [data]     [data]
```

**Analysis:** Create 2D heatmap showing outcome fractions

---

### Experiment D: Full Resolution (Publication Quality)
**Question:** Complete characterization with statistical power

```bash
# 24 means × 100 reps = 2,400 simulations (~3-4 hours)
python run_simulation_WITH_GAMMA.py \
  --distribution gamma \
  --means 0.05 0.10 0.15 0.20 0.25 0.30 0.35 0.40 0.45 0.50 \
          0.55 0.60 0.65 0.70 0.75 0.80 0.85 0.90 0.95 1.00 \
          1.05 1.10 1.15 1.20 \
  --cvs 0.577 \
  --reps 100

# Then repeat with different CVs:
# CV = 0.2 (low variance)
# CV = 0.577 (uniform-like, baseline)
# CV = 1.0 (high variance)
```

---

## Understanding the Output

### File Structure
```
Simulation_Data/
└── gamma_mean0.50_cv0.50_10reps/
    ├── simulation_parameters.xlsx      # All settings
    └── Community_gamma.json             # All results + matrices
```

### JSON Data Structure
```json
{
  "0.50": {                              // Mean interaction strength
    "rep_000": {                         // Repetition 0
      "sc_list": {...},                  // Single community outcomes
      "cc_list": {...},                  // Coalescence outcomes
      "parameters": {
        "seed": 5000,
        "mean": 0.5,
        "cv": 0.5,
        "distribution": "gamma",
        "interaction_matrix": [[...]],   // Full 48×48 matrix
        "growth_rates": [...],           // All 1.0
        "carrying_capacities": [...],    // All 1.0
        "interaction_matrix_stats": {
          "mean": 0.502,                 // Empirical mean
          "std": 0.251,                  // Empirical std
          "min": 0.001,
          "max": 2.134,
          "cv": 0.500                    // Empirical CV
        }
      }
    },
    "rep_001": {...},
    ...
  }
}
```

---

## Plotting Phase Diagrams

### After running simulations:

```bash
# 1. Modify plot_phase_diagrams_WITH_MATRICES.py to handle gamma data
#    (TODO: create plot_phase_diagrams_GAMMA.py)

# 2. Generate phase diagram
python plot_phase_diagrams_GAMMA.py \
  --input Simulation_Data/gamma_mean0.50_cv0.50_10reps/Community_gamma.json \
  --output Figure/PhaseDiagram/Fig_gamma_mean0.50_cv0.50.svg

# 3. Compare multiple CVs on one plot
python plot_phase_diagrams_GAMMA_COMPARISON.py \
  --cv_values 0.2 0.5 1.0 \
  --mean 0.5 \
  --reps 10
```

---

## Advanced: Custom Parameter Combinations

### Specify different CV for each mean:
```bash
python run_simulation_WITH_GAMMA.py \
  --means 0.3 0.5 0.8 \
  --cvs 0.2 0.5 1.0 \
  --reps 10

# This creates:
# mean=0.3 with CV=0.2
# mean=0.5 with CV=0.5
# mean=0.8 with CV=1.0
```

### Single CV applied to all means:
```bash
python run_simulation_WITH_GAMMA.py \
  --means 0.3 0.5 0.8 \
  --cvs 0.5 \
  --reps 10

# This creates:
# mean=0.3 with CV=0.5
# mean=0.5 with CV=0.5
# mean=0.8 with CV=0.5
```

---

## Command-Line Options Reference

```bash
python run_simulation_WITH_GAMMA.py [OPTIONS]

Options:
  --distribution {gamma,uniform}
      Distribution type (default: gamma)

  --means FLOAT [FLOAT ...]
      Mean interaction strengths (default: 0.3 0.5 0.8)
      Example: --means 0.3 0.5 0.8

  --cvs FLOAT [FLOAT ...]
      CV values for gamma distribution (default: 0.5 for all means)
      - Single value: applied to all means
      - Multiple values: must match number of means
      Example: --cvs 0.2 0.5 1.0

  --reps INT
      Number of repetitions per parameter combination (default: 10)
      Example: --reps 20

Examples:
  # Minimal test
  python run_simulation_WITH_GAMMA.py --means 0.5 --reps 5

  # Compare distributions
  python run_simulation_WITH_GAMMA.py --distribution uniform --means 0.5 --reps 10
  python run_simulation_WITH_GAMMA.py --distribution gamma --means 0.5 --cvs 0.577 --reps 10

  # Variance sweep
  python run_simulation_WITH_GAMMA.py --means 0.5 0.5 0.5 --cvs 0.2 0.5 1.0 --reps 20
```

---

## Troubleshooting

### "Number of CVs must match number of means"
```bash
# Wrong:
python run_simulation_WITH_GAMMA.py --means 0.3 0.5 0.8 --cvs 0.2 0.5
# → 3 means but only 2 CVs

# Fixed (option 1): Specify CV for each mean
python run_simulation_WITH_GAMMA.py --means 0.3 0.5 0.8 --cvs 0.2 0.5 1.0

# Fixed (option 2): Use single CV for all
python run_simulation_WITH_GAMMA.py --means 0.3 0.5 0.8 --cvs 0.5
```

### Simulation taking too long?
- Reduce `--reps` (10 is good for testing)
- Reduce number of `--means` values
- Each simulation takes ~5 seconds
- Estimate: (N_means × N_reps × 5 sec) / 60 = minutes

### File size too large?
- Matrices are 48×48 = 2,304 floats each
- 10 reps × 3 means = ~5-10 MB
- 100 reps × 24 means = ~500-700 MB
- This is expected and necessary for your analysis

---

## Recommended First Steps

1. **Quick test** (2 min):
   ```bash
   python run_simulation_WITH_GAMMA.py --means 0.5 --reps 5
   ```

2. **Verify matches uniform** (10 min):
   ```bash
   python run_simulation_WITH_GAMMA.py --distribution gamma --means 0.5 --cvs 0.577 --reps 10
   ```

3. **Test variance effect** (15 min):
   ```bash
   python run_simulation_WITH_GAMMA.py --means 0.5 0.5 0.5 --cvs 0.2 0.5 1.0 --reps 10
   ```

4. **If results interesting, scale up** (2-3 hours):
   ```bash
   python run_simulation_WITH_GAMMA.py --means 0.5 0.5 0.5 --cvs 0.2 0.5 1.0 --reps 100
   ```

Good luck with your experiments! 🚀
