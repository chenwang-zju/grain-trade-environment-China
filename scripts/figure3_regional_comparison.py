Fig.3

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib as mpl
import os

# Global font: Arial
mpl.rcParams['font.family'] = 'Arial'

# Global font sizes
mpl.rcParams['font.size'] = 14
mpl.rcParams['axes.labelsize'] = 14
mpl.rcParams['xtick.labelsize'] = 12
mpl.rcParams['ytick.labelsize'] = 12
mpl.rcParams['figure.titlesize'] = 16
mpl.rcParams['legend.fontsize'] = 14

# ======================
# Paths
# ======================
save_dir = r"E:\OneDrive\Python_me\paper_figures\1.trade_grain"
os.makedirs(save_dir, exist_ok=True)

save_png = os.path.join(save_dir, "trade_grain_fig6ok.png")
save_pdf = os.path.join(save_dir, "trade_grain_fig6ok.pdf")
save_svg = os.path.join(save_dir, "trade_grain_fig6ok.svg")

# ======================
# Region settings
# Exclude SC in panels a/b/c; keep SC in panel d
# ======================
regions_all = ['NE', 'NC', 'NW', 'MLYR', 'SC', 'SW']
regions_abc = ['NE', 'NC', 'NW', 'MLYR', 'SW']
regions_d   = ['NE', 'NC', 'NW', 'MLYR', 'SC', 'SW']
years = np.array([1980, 1990, 2000, 2010, 2020])

drop_region = 'SC'
drop_idx = regions_all.index(drop_region)

# ======================
# VL
# ======================
VL_all = np.array([
    [2.97, 3.88, 0.44, 11.61, 14.12],
    [0.00, 0.99, 1.55, 3.13, 2.75],
    [0.00, 0.86, 0.29, 3.09, 4.10],
    [2.52, 3.00, 2.84, 2.40, 1.53],
    [0.00, 0.00, 0.00, 0.00, 0.00],
    [2.13, 2.53, 0.19, 0.00, 0.00],
])
VL_nat = np.array([7.62, 11.25, 5.30, 20.23, 22.50])

# ======================
# VW
# ======================
VW_all = np.array([
    [6.99, 15.60,  1.39, 60.28, 83.05],
    [0.00,  2.68,  5.09, 12.71, 13.05],
    [0.02,  2.63,  1.48, 13.01, 20.76],
    [11.90, 16.72, 16.54, 15.05, 10.70],
    [0.00,  0.00,  0.00,  0.00,  0.00],
    [5.84,  9.66,  0.89,  0.00,  0.00],
])
VW_nat = np.array([24.75, 47.28, 25.39, 101.04, 127.56])

# ======================
# totN
# ======================
totN_all = np.array([
    [0.08, 0.13, 0.02, 0.31, 0.39],
    [0.00, 0.04, 0.06, 0.12, 0.11],
    [0.00, 0.04, 0.01, 0.16, 0.21],
    [0.10, 0.13, 0.12, 0.11, 0.07],
    [0.00, 0.00, 0.00, 0.00, 0.00],
    [0.07, 0.08, 0.01, 0.00, 0.00],
])
totN_nat = np.array([0.25, 0.42, 0.22, 0.69, 0.78])

# ======================
# totC (new data, excluding transport)
# ======================
totC_all = np.array([
    [6.23, 13.60, 1.78, 41.35, 51.76],
    [0.00, 3.85, 7.31, 14.73, 13.14],
    [0.01, 3.17, 1.31, 13.62, 19.06],
    [8.00, 12.55, 13.46, 10.67, 6.66],
    [0.00, 0.00, 0.00, 0.00, 0.00],
    [4.70, 7.81, 0.74, 0.00, 0.00],
])
totC_nat = np.array([18.94, 40.98, 24.60, 80.37, 90.61])

# ======================
# Transport emissions (added in panel d)
# ======================
tottanGHG_all = np.array([
    [0.135, 0.559, 0.015, 1.853, 2.880],
    [0.109, 0.133, 0.102, 0.499, 0.396],
    [0.092, 0.134, 0.019, 0.365, 0.614],
    [0.114, 0.188, 0.164, 0.656, 0.543],
    [0.024, 0.172, 0.175, 1.346, 2.219],
    [0.107, 0.656, 0.023, 0.473, 0.757],
])
tottanGHG_nat = np.array([0.582, 1.843, 0.498, 5.192, 7.410])

# ======================
# Panels a/b/c: exclude SC; panel d: keep SC
# ======================
VL_abc   = np.delete(VL_all,   drop_idx, axis=0)
VW_abc   = np.delete(VW_all,   drop_idx, axis=0)
totN_abc = np.delete(totN_all, drop_idx, axis=0)

# Panel d: netGHG = totC + transport
netGHG_d = totC_all + tottanGHG_all
netGHG_nat_d = totC_nat + tottanGHG_nat

# ======================
# Colors
# ======================
colors_VL   = ['#edf8e9', '#c7e9c0', '#a1d99b', '#74c476', '#41ab5d']
colors_VW   = ['#ebf7fc', '#c3ecfa', '#82d6f6', '#4cbff0', '#149fe8']
colors_totN = ['#fde0ca', '#fbd1c9', '#f7cad1', '#fec1db', '#f8abd1']
colors_totC = ['#e6cddd', '#cdaccd', '#c49fc4', '#bc93bc', '#ac71ac']

fig, axes = plt.subplots(2, 2, figsize=(10, 8), sharex=False)

# ======================
# y-axis ticks and limits
# ======================
yticks_VL   = np.arange(0, 16, 5)
yticks_VW   = np.arange(0, 101, 20)
yticks_totN = np.arange(0.0, 0.51, 0.1)
yticks_d    = np.arange(0, 81, 20)

datasets = [
    (VL_abc,     VL_nat,       axes[0, 0], 'a', regions_abc, 'Virtual cropland (Mha)',             colors_VL,   yticks_VL,   (0, 15)),
    (VW_abc,     VW_nat,       axes[0, 1], 'b', regions_abc, 'Virtual water (Gm$^3$)',             colors_VW,   yticks_VW,   (0, 100)),
    (totN_abc,   totN_nat,     axes[1, 0], 'c', regions_abc, 'N emissions (Mt N)',                 colors_totN, yticks_totN, (0, 0.5)),
    (netGHG_d,   netGHG_nat_d, axes[1, 1], 'd', regions_d,   r'Net GHG emissions (Mt CO$_2$-eq)',  colors_totC, yticks_d,    (0, 80)),
]

bar_width = 0.15
offset_step = bar_width * 1.2

for data, nat, ax, panel_label, regions_used, ylabel, color_list, yticks, ylim in datasets:
    x = np.arange(len(regions_used))
    offsets = (np.arange(len(years)) - (len(years) - 1) / 2.0) * offset_step

    # Main bars
    for i, year in enumerate(years):
        ax.bar(
            x + offsets[i],
            data[:, i],
            width=bar_width,
            color=color_list[i],
            edgecolor='none'
        )

    ax.set_xticks(x)
    ax.set_xticklabels(regions_used)
    ax.set_xlim(-0.5, len(regions_used) - 0.5)
    ax.set_ylim(*ylim)
    ax.set_yticks(yticks)

    # Left/right axis settings
    if panel_label in ['b', 'd']:
        ax.set_ylabel(ylabel, rotation=90)
        ax.yaxis.set_label_position('right')
        ax.yaxis.tick_right()
        ax.spines['right'].set_visible(True)
        ax.spines['left'].set_visible(False)
        ax.spines['top'].set_visible(False)
    else:
        ax.set_ylabel(ylabel)
        ax.yaxis.set_label_position('left')
        ax.yaxis.tick_left()
        ax.spines['left'].set_visible(True)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

    # Panel labels a/b/c/d at upper left
    ax.text(
        -0.03, 1.08, panel_label,
        transform=ax.transAxes,
        fontsize=18,
        fontweight='bold',
        va='bottom',
        ha='left'
    )

    # Top year color bar
    cax = inset_axes(
        ax,
        width="80%",
        height="28%",
        loc='upper center',
        bbox_to_anchor=(0.1, 0.95, 0.8, 0.13),
        bbox_transform=ax.transAxes,
        borderpad=0
    )
    for i, year in enumerate(years):
        cax.bar(i, 1, color=color_list[i], width=0.7)
        cax.text(i, 1.0, str(year), ha='center', va='bottom', fontsize=11)
    cax.set_xlim(-0.5, len(years) - 0.5)
    cax.set_ylim(0, 1.3)
    cax.set_xticks([])
    cax.set_yticks([])
    for spine in cax.spines.values():
        spine.set_visible(False)

    # Nationwide inset
    inax = inset_axes(
        ax,
        width="100%",
        height="100%",
        loc='upper left',
        bbox_to_anchor=(0.38, 0.53, 0.55, 0.43),
        bbox_transform=ax.transAxes,
        borderpad=0
    )
    for i, year in enumerate(years):
        inax.bar(i, nat[i], color=color_list[i], width=0.5)
    inax.set_xticks(range(len(years)))
    inax.set_xticklabels([])
    inax.text(
        0.08, 0.95, 'Nationwide',
        transform=inax.transAxes,
        ha='left', va='top', fontsize=12
    )
    inax.tick_params(labelsize=11)
    for spine in inax.spines.values():
        spine.set_linewidth(0.5)

# x-axis labels
axes[1, 0].set_xlabel('Region')
axes[1, 1].set_xlabel('Region')

fig.subplots_adjust(hspace=0.3, wspace=0.06, top=0.92, bottom=0.10)

plt.show()

fig.savefig(save_png, dpi=600, bbox_inches="tight")
fig.savefig(save_pdf, bbox_inches="tight")
fig.savefig(save_svg, bbox_inches="tight")

print("Saved:", save_png)
print("Saved:", save_pdf)
print("Saved:", save_svg)
