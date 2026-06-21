"""
Recreate the two-panel pump-probe / 2D-electronic-spectroscopy figure
(panels g and h) showing transient absorption spectra of (n,m) SWCNT
excitonic transitions.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from scipy.interpolate import PchipInterpolator
from scipy.ndimage import gaussian_filter1d


def anchored_curve(xgrid, x_anchor, y_anchor, smooth_sigma=0.8):
    y = PchipInterpolator(x_anchor, y_anchor)(xgrid)
    if smooth_sigma > 0:
        y = gaussian_filter1d(y, smooth_sigma)
    return y


def multi_sine_wiggle(xgrid, amp, phase=0.0):
    return amp * (
        0.85 * np.sin((xgrid - 671) / 4.7 + phase)
        + 0.45 * np.sin((xgrid - 684) / 2.55 + 0.4 * phase)
        + 0.22 * np.sin((xgrid - 699) / 1.33 - 0.2)
        + 0.10 * np.sin((xgrid - 708) / 0.95 + 0.5 * phase)
    )


def tapered_wiggle(xgrid, left, right, amp, phase=0.0):
    taper = np.zeros_like(xgrid)
    mask = (xgrid >= left) & (xgrid <= right)
    taper[mask] = np.sin(np.pi * (xgrid[mask] - left) / (right - left)) ** 2
    return taper * multi_sine_wiggle(xgrid, amp, phase)


def build_panel_g(xgrid):
    x_anchor = np.array(
        [670, 676, 684, 689, 695, 702, 710, 720, 731, 736, 744, 752, 758,
         763, 768, 774, 780, 786, 804, 820],
        dtype=float,
    )
    y_anchor = np.array(
        [0.00, 0.04, 0.12, 0.13, 0.09, 0.05, -0.02, -0.22, -0.56, -0.61,
         -0.52, -0.16, 0.03, 0.10, 0.13, 0.08, 0.01, -0.12, -0.60, 0.00],
        dtype=float,
    )
    y = anchored_curve(xgrid, x_anchor, y_anchor, smooth_sigma=0.95)
    y += tapered_wiggle(xgrid, 679, 713, amp=0.010, phase=0.25)
    y += tapered_wiggle(xgrid, 756, 781, amp=0.008, phase=0.85)
    return gaussian_filter1d(y, 0.7)


def build_panel_h_traces(xgrid):
    colors = {
        "0 μm": "#ff1010",
        "0.27 μm": "#f06a0f",
        "0.60 μm": "#eeb900",
        "1 μm": "#14933e",
    }
    x_anchor = np.array(
        [670, 676, 684, 692, 698, 704, 712, 720, 728, 734, 740, 748, 756, 762,
         770, 778, 786, 794, 800, 806, 812, 820],
        dtype=float,
    )
    anchors = {
        "0 μm": np.array(
            [0.00, 0.04, 0.18, 0.40, 0.48, 0.46, 0.22, -0.12, -0.62, -0.98,
             -0.54, -0.05, 0.30, 0.48, 0.50, 0.18, -0.36, -1.14, -1.78, -1.82,
             -1.50, -0.52],
            dtype=float,
        ),
        "0.27 μm": np.array(
            [0.00, 0.03, 0.14, 0.30, 0.40, 0.38, 0.20, -0.10, -0.54, -0.84,
             -0.52, -0.08, 0.22, 0.40, 0.38, 0.16, -0.28, -0.86, -1.20, -1.24,
             -0.88, -0.32],
            dtype=float,
        ),
        "0.60 μm": np.array(
            [0.00, 0.02, 0.10, 0.20, 0.24, 0.22, 0.12, -0.10, -0.40, -0.70,
             -0.58, -0.20, 0.08, 0.24, 0.26, 0.12, -0.16, -0.52, -0.92, -1.02,
             -0.84, -0.18],
            dtype=float,
        ),
        "1 μm": np.array(
            [0.00, 0.03, 0.10, 0.20, 0.32, 0.36, 0.18, -0.05, -0.30, -0.62,
             -0.42, 0.04, 0.40, 0.64, 0.58, 0.34, 0.00, -0.30, -0.66, -0.40,
             -0.14, 0.28],
            dtype=float,
        ),
    }
    wiggles = {
        "0 μm": (0.060, 0.20),
        "0.27 μm": (0.048, 0.85),
        "0.60 μm": (0.038, 1.15),
        "1 μm": (0.056, 1.85),
    }
    traces = {}
    for label, y_anchor in anchors.items():
        amp, phase = wiggles[label]
        y = anchored_curve(xgrid, x_anchor, y_anchor, smooth_sigma=0.75)
        y += tapered_wiggle(xgrid, 676, 716, amp=amp, phase=phase)
        y += tapered_wiggle(xgrid, 725, 742, amp=amp * 0.75, phase=phase + 0.15)
        y += tapered_wiggle(xgrid, 744, 780, amp=amp * 1.05, phase=phase + 0.3)
        y += tapered_wiggle(xgrid, 792, 818, amp=amp * 1.25, phase=phase + 0.6)
        traces[label] = (colors[label], gaussian_filter1d(y, 0.55))
    return traces


wl = np.linspace(670, 820, 900)
y_g = build_panel_g(wl)
spec_params = ["0 μm", "0.27 μm", "0.60 μm", "1 μm"]
traces = build_panel_h_traces(wl)


plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9.2,
    "axes.linewidth": 2.0,
    "xtick.major.width": 2.0,
    "ytick.major.width": 2.0,
    "xtick.minor.width": 1.0,
    "ytick.minor.width": 1.0,
    "xtick.major.size": 5.0,
    "ytick.major.size": 5.0,
    "xtick.minor.size": 2.8,
    "ytick.minor.size": 2.8,
    "xtick.direction": "in",
    "ytick.direction": "in",
})

fig, (ax_g, ax_h) = plt.subplots(1, 2, figsize=(9.1, 4.0))
fig.subplots_adjust(left=0.085, right=0.985, top=0.855, bottom=0.18, wspace=0.34)


ax_g.plot(wl, y_g, color="#666666", linewidth=1.85)
ax_g.set_xlim(670, 820)
ax_g.set_ylim(-0.62, 0.22)
ax_g.set_xticks([680, 720, 760, 800])
ax_g.set_yticks([-0.6, -0.4, -0.2, 0.0, 0.2])
ax_g.set_yticklabels(["-0.6", "-0.4", "-0.2", "0", "0.2"])
ax_g.xaxis.set_minor_locator(MultipleLocator(10))
ax_g.yaxis.set_minor_locator(MultipleLocator(0.1))
ax_g.tick_params(axis="both", which="both", top=True, right=True, labelsize=10.0)
ax_g.set_xlabel("Wavelength (nm)", fontsize=12.5, fontweight="bold")
ax_g.set_ylabel(r"$\Delta$ mOD", fontsize=12.5, fontweight="bold")
ax_g.text(-0.10, 1.01, "g.", transform=ax_g.transAxes,
          fontsize=15, fontweight="bold", ha="right", va="center")
ax_g.text(0.71, 0.88, r"t$_2$ = 150 fs", transform=ax_g.transAxes,
          fontsize=11.0, fontweight="bold")
ax_g.text(703, -0.49, "(8,6/7)", color="#1e6f37",
          fontsize=11.0, fontweight="bold", ha="center")
ax_g.text(780, -0.49, "(9,7)", color="#d22a7c",
          fontsize=11.0, fontweight="bold", ha="center")


for label in spec_params:
    color, y = traces[label]
    ax_h.plot(wl, y, color=color, linewidth=1.6)

ax_h.set_xlim(670, 820)
ax_h.set_ylim(-2.05, 1.05)
ax_h.set_xticks([680, 720, 760, 800])
ax_h.set_yticks([-2, -1, 0, 1])
ax_h.xaxis.set_minor_locator(MultipleLocator(10))
ax_h.yaxis.set_minor_locator(MultipleLocator(0.5))
ax_h.tick_params(axis="both", which="both", top=True, right=True, labelsize=10.0)
ax_h.set_xlabel("Wavelength (nm)", fontsize=12.5, fontweight="bold")
ax_h.set_ylabel("Amplitude", fontsize=12.5, fontweight="bold")
ax_h.text(-0.11, 1.01, "h.", transform=ax_h.transAxes,
          fontsize=15, fontweight="bold", ha="right", va="center")
ax_h.text(0.73, 0.88, r"t$_2$ = 1.5 ps", transform=ax_h.transAxes,
          fontsize=11.0, fontweight="bold")
ax_h.text(714, -0.70, "D", fontsize=12, fontweight="bold", ha="center")
ax_h.text(782, -0.70, "E", fontsize=12, fontweight="bold", ha="center")

legend_x = 0.05
legend_y0 = 0.28
legend_dy = 0.075
for idx, label in enumerate(spec_params):
    color, _ = traces[label]
    ax_h.text(legend_x, legend_y0 - idx * legend_dy, label,
              transform=ax_h.transAxes, color=color,
              fontsize=10.0, fontweight="bold")

ax_h.text(0.44, 1.03, "Pump slice", transform=ax_h.transAxes,
          fontsize=12.5, fontweight="bold", ha="center", va="bottom")
ax_h.plot([0.61, 0.77], [1.055, 1.055], transform=ax_h.transAxes,
          color="#ea82bd", linewidth=1.7, linestyle=(0, (3.5, 2.5)),
          clip_on=False, solid_capstyle="butt")


out_path = "/Users/jysong/Desktop/Gore_lab/Sequencing/Coalescence_session_20230404/ToDasol_recreation_codex.png"
plt.savefig(out_path, dpi=180, facecolor="white")
print(f"Saved: {out_path}")
