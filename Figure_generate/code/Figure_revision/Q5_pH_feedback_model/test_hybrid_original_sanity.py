"""Sanity sweep for hybrid_original_model.

Sweeps tension in {0.0, 0.1, 1.0, 2.0} at alpha=0.3 for both continuous
and binary modes.  Reports:
    - Dominance / Mixing / Restructuring fractions
    - fraction of events that blew up (ODE failures or n>BLOWUP_CAP)
    - average final env magnitude at steady state
    - average number of survivors per parent

Purpose: confirm integration is stable across the requested tension range
and that the tension knob actually moves class frequencies.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.abspath(os.path.join(HERE, "..", ".."))
if CODE_DIR not in sys.path:
    sys.path.insert(0, CODE_DIR)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

_orig_cwd = os.getcwd()
os.chdir(CODE_DIR)
from common_setup import (
    metric_VectorDecomposition_onlyPositive,
    calculate_assymetricity, characterize_case,
)
os.chdir(_orig_cwd)

import numpy as np
from hybrid_original_model import (
    sample_hybrid_pool, assemble_pool, run_coalescence, EXTINCTION,
)

ALPHA = 0.3
TENSIONS = [0.0, 0.3, 0.6, 1.0]
MODES = ["continuous", "binary"]

N_POOL = 24
NUM_C = 2
SP_PER_C = 12
N_POOLS = 100
SEED = 42

print(f"alpha = {ALPHA};  tensions = {TENSIONS};  modes = {MODES}")
print(f"N_pool = {N_POOL}, num_C = {NUM_C}, sp_per_C = {SP_PER_C}, "
      f"n_pools = {N_POOLS}, seed = {SEED}\n")

header = (f"{'mode':<12}{'tau':>6}  "
          f"{'Dom':>6}{'Mix':>6}{'Res':>6}  "
          f"{'n_ev':>5}{'nan':>5}{'blow':>5}  "
          f"{'env':>8}{'surv':>6}")
print(header)
print("-" * len(header))

for mode in MODES:
    for tau in TENSIONS:
        rng = np.random.default_rng(SEED)
        dom = mix = res = 0
        events = blowup = nanct = 0
        env_abs_sum = 0.0
        env_n = 0
        surv_sum = 0
        surv_n = 0
        for rep in range(N_POOLS):
            pool = sample_hybrid_pool(N_POOL, alpha=ALPHA, tension=tau,
                                       rng=rng, mode=mode)
            ret = assemble_pool(pool, NUM_C, SP_PER_C, rng, return_env=True)
            if ret is None:
                blowup += 1
                continue
            _, sc, envs = ret
            for e in envs:
                env_abs_sum += abs(e)
                env_n += 1
            for n in sc:
                surv_sum += int(np.sum(n > EXTINCTION))
                surv_n += 1
            for i in range(NUM_C):
                for j in range(i + 1, NUM_C):
                    n_c = run_coalescence(pool, sc[i], sc[j])
                    if n_c is None:
                        blowup += 1
                        continue
                    nA, nB = sc[i], sc[j]
                    if (np.linalg.norm(nA) == 0 or
                            np.linalg.norm(nB) == 0 or
                            np.linalg.norm(n_c) == 0):
                        nanct += 1
                        continue
                    try:
                        u, v, k = metric_VectorDecomposition_onlyPositive(
                            nA, nB, n_c)
                    except (np.linalg.LinAlgError, FloatingPointError,
                            ZeroDivisionError):
                        nanct += 1
                        continue
                    if (any(np.isnan([u, v, k])) or
                            any(np.isinf([u, v, k]))):
                        nanct += 1
                        continue
                    x_mag, y_asym = calculate_assymetricity(u, v, k)
                    cat = characterize_case(x_mag, y_asym)
                    if cat is None:
                        nanct += 1
                        continue
                    events += 1
                    if cat == 0:
                        dom += 1
                    elif cat == 1:
                        mix += 1
                    elif cat == 2:
                        res += 1
        denom = max(events, 1)
        env_mean = env_abs_sum / max(env_n, 1)
        surv_mean = surv_sum / max(surv_n, 1)
        print(f"{mode:<12}{tau:>6.2f}  "
              f"{dom/denom:>6.2f}{mix/denom:>6.2f}{res/denom:>6.2f}  "
              f"{events:>5d}{nanct:>5d}{blowup:>5d}  "
              f"{env_mean:>8.2f}{surv_mean:>6.1f}")
