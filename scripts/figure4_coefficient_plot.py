import matplotlib.pyplot as plt
import numpy as np
import os

# =========================================================
# 1. Update data
# =========================================================

categories = ["Machinery", "Aging", "Mach. × Aging", "Farm size", "Urbanization", "Irrigation"]

# --- Northern data ---
north_coef = [0.5616479, -1.159496, 0.120735, 0.0420355, -0.0445908, 0.4995775]
north_ci = [
    (0.2998465, 0.8234493),
    (-1.676143, -0.6428496),
    (0.0488207, 0.1926494),
    (-0.1987205, 0.2827915),
    (-0.2195101, 0.1303284),
    (0.2818526, 0.7173024)
]

# --- Southern data ---
south_coef = [0.8151451, -1.193312, 0.1872067, 0.1832243, -0.254382, 0.0163222]
south_ci = [
    (0.4797264, 1.150564),
    (-2.190584, -0.1960407),
    (0.0389643, 0.3354491),
    (0.0570302, 0.3094183),
    (-0.3798648, -0.1288991),
    (-0.3532411, 0.3858855)
]

# --- Crops ---
categories_b = ["Machinery", "Farm size", "Urbanization"]

rice_coef = [0.8879928, 0.1663992, -0.1406718]
rice_ci = [(0.242511, 1.533475), (-0.2424254, 0.5752237), (-0.4892951, 0.2079514)]

wheat_coef = [0.83806, 0.5072618, -0.28454]
wheat_ci = [(-1.210168, 2.886288), (-0.1948926, 1.209416), (-1.532929, 0.9638496)]

maize_coef = [0.1360838, 0.0754475, 0.2263587]
maize_ci = [(-0.8283266, 1.100494), (-0.0861133, 0.2370082), (0.0471563, 0.4055612)]

# =========================================================
# 2. Utility function
# =========================================================

def ci_to_err(coef, ci):
    lower = [abs(coef[i] - ci[i][0]) for i in range(len(coef))]
    upper = [abs(ci[i][1] - coef[i]) for i in range(len(coef))]
    return [lower, upper]

north_err = ci_to_err(north_coef, north_ci)
south_err = ci_to_err(south_coef, south_ci)
rice_err = ci_to_err(rice_coef, rice_ci)
wheat_err = ci_to_err(wheat_coef, wheat_ci)
maize_err = ci_to_err(maize_coef, maize_ci)

# =========================================================
# 3. Plot settings
# =========================================================

plt.style.use("default")
plt.rcParams.update({
    "font.size": 14,
    "font.family": "Arial",
    "axes.linewidth": 1,
    "xtick.major.width": 1,
    "ytick.major.width": 1,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "errorbar.capsize": 3,
})

colors = {
    "North": "#1F78B4",
    "South": "#FF888B",
    "Rice": "#FC8D62",
    "Wheat": "#66C2A5",
    "Maize": "#FDBF6F"
}

fig, axes = plt.subplots(
    1, 2,
    figsize=(14, 4.5),
    gridspec_kw={"wspace": 0.45}
)

# =========================================================
# Panel a: Northern vs Southern
# =========================================================

ax = axes[0]
y = np.arange(len(categories))

north_bg = "#82B8E4"
south_bg = "#F8C5CC"

for i in range(len(categories)):
    ax.axhspan(i + 0.02, i + 0.22, color=north_bg, alpha=0.3, zorder=0)
    ax.axhspan(i - 0.22, i - 0.02, color=south_bg, alpha=0.5, zorder=0)

ax.errorbar(
    north_coef, y + 0.12, xerr=north_err, fmt="s",
    color=colors["North"], markersize=7, elinewidth=1.5, label="Northern"
)
ax.errorbar(
    south_coef, y - 0.12, xerr=south_err, fmt="o",
    color=colors["South"], markersize=7, elinewidth=1.5, label="Southern"
)

ax.set_yticks(y)
ax.set_yticklabels(categories)
ax.axvline(0, color="gray", linestyle="--", linewidth=1)
ax.set_xlabel("Coefficient")

# Core legend setting
# loc="upper left": anchor legend by its upper-left corner
# bbox_to_anchor=(0.02, 0.02): place the anchor point in the blank area below Irrigation
ax.legend(
    frameon=False,
    loc="center left",
    ncol=1,
    columnspacing=1.0,
)

# =========================================================
# Panel b: Crops
# =========================================================

ax = axes[1]
y = np.arange(len(categories_b))
row_colors = ["#ABDDA4", "#f5f5dc", "#E3D5EE"]

for i, rc in enumerate(row_colors):
    ax.axhspan(i - 0.4, i + 0.4, color=rc, alpha=0.5, zorder=0)

ax.errorbar(
    rice_coef, y + 0.18, xerr=rice_err, fmt="o",
    color=colors["Rice"], markersize=7, elinewidth=1.5, label="Rice"
)
ax.errorbar(
    wheat_coef, y, xerr=wheat_err, fmt="s",
    color=colors["Wheat"], markersize=7, elinewidth=1.5, label="Wheat"
)
ax.errorbar(
    maize_coef, y - 0.18, xerr=maize_err, fmt="D",
    color=colors["Maize"], markersize=7, elinewidth=1.5, label="Maize"
)

ax.set_yticks(y)
ax.set_yticklabels(categories_b)
ax.axvline(0, color="gray", linestyle="--", linewidth=1)
ax.set_xlabel("Coefficient")
ax.legend(frameon=False, loc="center right")

plt.tight_layout()

# =========================================================
# 4. Save
# =========================================================

save_dir = r"E:\OneDrive\Python_me\paper_figures\1.trade_grain"
os.makedirs(save_dir, exist_ok=True)

plt.savefig(
    os.path.join(save_dir, "12_north_south_crops_climate_controlled_flatOK.png"),
    dpi=600,
    bbox_inches="tight"
)

plt.show()
