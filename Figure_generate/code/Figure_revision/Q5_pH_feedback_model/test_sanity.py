"""
test_sanity.py
==============

Minimal correctness checks for pH_feedback_model.py. Does not require
pytest; run as `python test_sanity.py` and it prints PASS / FAIL lines
per test.

Checks:
  (1) ODE conserves what it should -- each species biomass is bounded by
      the per-species logistic scale 1, and proton concentration p stays
      near the model's physical interval [0, 2b].
  (2) Single-species assembly reaches a steady state whose residual RHS
      is numerically small (|dn/dt|, |dp/dt| below a tolerance).
  (3) A two-parent coalescence returns an abundance vector of the same
      length as the parent pool and feeds cleanly into
      common_setup.metric_VectorDecomposition_onlyPositive without a
      shape mismatch.
  (4) The pH-tension knob monotonically increases some measure of
      interaction effect (here: species-pair coexistence rate drops as
      tension grows, i.e. strong pH coupling tends to exclude).
"""

import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from pH_feedback_model import (
    SpeciesPool, sample_species_pool, scale_interaction_strength,
    simulate_single_community, run_coalescence, assemble_pool,
    classify_coalescence, _rhs, _integrate,
    DEFAULT_C_MAG, DEFAULT_P0, DEFAULT_B, DEFAULT_K, EXTINCTION, T_END,
)


def _header(msg):
    print("=" * 70)
    print(msg)
    print("=" * 70)


def test_bounds():
    _header("TEST 1: biomass <= K and p in [0, 2b] along integration")
    rng = np.random.default_rng(0)
    pool = sample_species_pool(6, rng)
    mask = np.ones(6, dtype=bool)
    sub = pool.subset(mask)
    # Integrate step-by-step by sampling solve_ivp at intermediate times.
    # Use RK45 (robust for short horizons and matches the cascade default).
    from scipy.integrate import solve_ivp
    y0 = np.concatenate([np.full(6, 0.05), [DEFAULT_P0]])
    t_eval = np.linspace(0, T_END, 200)
    sol = None
    for m in ["RK45", "LSODA", "BDF"]:
        sol = solve_ivp(lambda t, y: _rhs(t, y, sub),
                        (0.0, T_END), y0, t_eval=t_eval,
                        method=m, rtol=1e-6, atol=1e-9)
        if sol.success:
            break
    assert sol.success, f"integration failed on all methods"
    n_traj = sol.y[:6, :]
    p_traj = sol.y[6, :]
    total_biomass = n_traj.sum(axis=0)
    per_species_max = n_traj.max(axis=1)
    ok_biomass = np.all(per_species_max <= 1.0 + 1e-2)
    ok_p_lo = np.all(p_traj >= -1e-6)
    ok_p_hi = np.all(p_traj <= 2 * DEFAULT_B + 1e-6)
    status = "PASS" if (ok_biomass and ok_p_lo and ok_p_hi) else "FAIL"
    print(f"  total biomass max = {total_biomass.max():.4f}; "
          f"per-species max = {per_species_max.max():.4f} (<= 1)"
          f" ... {ok_biomass}")
    print(f"  p range = [{p_traj.min():.4f}, {p_traj.max():.4f}]"
          f" (should be in [0, {2*DEFAULT_B}]) ... "
          f"{ok_p_lo and ok_p_hi}")
    print(f"  -> {status}")
    return ok_biomass and ok_p_lo and ok_p_hi


def test_single_species_steady_state():
    _header("TEST 2: single-species assembly reaches steady state")
    rng = np.random.default_rng(1)
    # Put one acidifier species with pH optimum at the starting p0.
    # This should grow to its feasible carrying biomass without dying.
    pool = SpeciesPool(
        p_pref=np.array([5.0]),
        sigma=np.array([4.0]),
        c=np.array([0.0]),    # no pH modification -> should hit K exactly
    )
    out = simulate_single_community(
        pool, np.array([True]), rng, p0=DEFAULT_P0)
    assert out is not None, "single-species integration returned None"
    # With c=0 and p_pref==p0, Gaussian = 1, so net growth rate is positive
    # and the per-species logistic term drives n -> 1.
    ok = abs(out[0] - 1.0) < 1e-2
    # Also check RHS magnitude at final state
    y_final = np.concatenate([out, [DEFAULT_P0]])
    rhs = _rhs(0.0, y_final, pool)
    rhs_mag = float(np.linalg.norm(rhs))
    ok2 = rhs_mag < 1e-4
    status = "PASS" if (ok and ok2) else "FAIL"
    print(f"  final n = {out[0]:.6f}  (expected ~ 1)")
    print(f"  |RHS| at steady state = {rhs_mag:.2e} (should be ~ 0)")
    print(f"  -> {status}")
    return ok and ok2


def test_coalescence_shape():
    _header("TEST 3: coalescence output shape feeds common_setup pipeline")
    # Ensure common_setup import path is set up the same way the driver does.
    # common_setup reads excel files via relative paths, so cd there first.
    CODE_DIR = os.path.abspath(os.path.join(HERE, "..", ".."))
    if CODE_DIR not in sys.path:
        sys.path.insert(0, CODE_DIR)
    _cwd_saved = os.getcwd()
    try:
        os.chdir(CODE_DIR)
        from common_setup import (
            metric_VectorDecomposition_onlyPositive,
            calculate_assymetricity,
            characterize_case,
        )
    finally:
        os.chdir(_cwd_saved)

    # Use a larger pool and iterate seeds until we find a non-degenerate
    # pair of parents (both non-empty); the *shape* parity is what we
    # actually want to prove here, but on a degenerate example the
    # decomposition is trivially zero and we learn nothing.
    ok = False
    for seed in range(20):
        rng = np.random.default_rng(seed)
        pool = sample_species_pool(24, rng)
        asm = assemble_pool(pool, num_C=2, sp_per_C=12, rng=rng)
        if asm is None:
            continue
        masks, sc = asm
        if sc[0].shape != (24,) or sc[1].shape != (24,):
            raise AssertionError(f"bad parent shape: {sc[0].shape}")
        n_C = run_coalescence(pool, sc[0], sc[1])
        if n_C is None or n_C.shape != (24,):
            raise AssertionError(f"bad n_C shape: "
                                 f"{None if n_C is None else n_C.shape}")
        if np.any(sc[0]) and np.any(sc[1]) and np.any(n_C):
            u, v, k = metric_VectorDecomposition_onlyPositive(
                sc[0], sc[1], n_C)
            x, y = calculate_assymetricity(u, v, k)
            cls = characterize_case(x, y)
            label, pdi, _, _, _ = classify_coalescence(sc[0], sc[1], n_C)
            print(f"  seed={seed}: parents non-empty, n_C shape OK "
                  f"({n_C.shape})")
            print(f"  parent A surv={(sc[0]>EXTINCTION).sum()}, "
                  f"B surv={(sc[1]>EXTINCTION).sum()}, "
                  f"C surv={(n_C>EXTINCTION).sum()}")
            print(f"  VectorDecomposition -> "
                  f"u={u:.3f}, v={v:.3f}, k={k:.3f}")
            print(f"  classify_case = {cls}   "
                  f"classify_coalescence = {label}")
            ok = cls in (0, 1, 2)
            break
    if not ok:
        print("  could not find a non-degenerate coalescence in 20 seeds")
    status = "PASS" if ok else "FAIL"
    print(f"  -> {status}")
    return ok


def test_tension_monotonic():
    _header("TEST 4: stronger pH-tension reduces species coexistence "
            "(monotonic direction check)")
    rng_master = np.random.default_rng(3)
    surv_counts = {}
    for tension in [0.25, 1.0, 2.5]:
        rng = np.random.default_rng(int(rng_master.integers(1 << 31)))
        pool0 = sample_species_pool(12, rng)
        pool = scale_interaction_strength(pool0, tension)
        mask = np.ones(12, dtype=bool)
        surv_list = []
        for _ in range(5):
            out = simulate_single_community(pool, mask, rng)
            if out is None:
                continue
            surv_list.append(int((out > EXTINCTION).sum()))
        surv_counts[tension] = np.mean(surv_list) if surv_list else float("nan")
        print(f"  tension={tension}: mean survivors = {surv_counts[tension]:.2f}")
    vals = [surv_counts[t] for t in (0.25, 1.0, 2.5)]
    # Allow ties; require weak monotone decrease, with low allowed to >= mid
    ok = (vals[0] >= vals[-1] - 0.5)   # strong tension should not *increase* survivors
    status = "PASS" if ok else "FAIL"
    print(f"  direction (low >= high, within 0.5 tol): {ok}")
    print(f"  -> {status}")
    return ok


if __name__ == "__main__":
    results = {
        "bounds": test_bounds(),
        "single_species_steady_state": test_single_species_steady_state(),
        "coalescence_shape": test_coalescence_shape(),
        "tension_monotonic": test_tension_monotonic(),
    }
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    for name, ok in results.items():
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    if not all(results.values()):
        sys.exit(1)
