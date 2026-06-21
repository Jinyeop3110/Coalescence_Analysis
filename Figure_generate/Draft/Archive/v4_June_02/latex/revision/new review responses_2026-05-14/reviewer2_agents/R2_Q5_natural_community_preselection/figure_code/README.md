# Figure Code For R2 Q5

This folder contains one response-only analysis:

- `plot_post_stabilization_taxonomic_distinctness.py`

Run from the assigned response folder:

```sh
/Users/jysong/miniforge3/bin/python figure_code/plot_post_stabilization_taxonomic_distinctness.py
```

Outputs are written to `../figures/`:

- `post_stabilization_taxonomic_distinctness.pdf`
- `post_stabilization_taxonomic_distinctness.png`
- `post_stabilization_taxonomic_summary.txt`

The script reads:

- `/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Analyzed/processed_Communities_natural.xlsx`
- `/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/Postprocessed/processed_Sequences_natural.xlsx`

Only one figure was generated because the available processed data can support a post-stabilization taxonomic distinctness check, but cannot support a direct pre-to-post stabilization convergence figure. The processed metadata contain final stabilized parental communities and coalesced communities only, not original environmental inocula before the seven serial dilution cycles. No functional profiles are available, so a functional convergence figure would overstate the evidence.
