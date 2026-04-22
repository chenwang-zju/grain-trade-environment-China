import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.ticker as ticker
import numpy as np
import os

# ==============================================================================
# 1. Path Settings
# ==============================================================================
folder_path = r"E:\OneDrive\Python_me\sheng"
map_filename = "CN-sheng-A.shp"
map_file_path = os.path.join(folder_path, map_filename)

output_dir = r"E:\OneDrive\Python_me\paper_figures\1.trade_grain"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Updated filename to reflect larger legend font
save_path = os.path.join(output_dir, "China_Map_Final_v8_LargeLegendOK.png")

# ==============================================================================
# 2. Prepare Data
# ==============================================================================
data_source = {
    'PAC': [
        110000, 120000, 130000, 140000, 150000,
        210000, 220000, 230000,
        310000, 320000, 330000, 340000, 350000, 360000, 370000,
        410000, 420000, 430000, 440000, 450000, 460000,
        500000, 510000, 520000, 530000, 540000,
        610000, 620000, 630000, 640000, 650000
    ],
    '1980': [-643.56, -643.56, -643.56, -679.96, -679.96, 666.97, 666.97, 666.97, 608.27, 608.27, 608.27, 608.27, -103.84, 608.27, -643.56, -643.56, 608.27, 608.27, -103.84, -103.84, -103.84, -424.73, -424.73, -424.73, -424.73, -424.73, -679.96, -679.96, -679.96, -679.96, -679.96],
    '1990': [26.29, 26.29, 26.29, -46.68, -46.68, 2292.61, 2292.61, 2292.61, 1060.32, 1060.32, 1060.32, 1060.32, -1208.84, 1060.32, 26.29, 26.29, 1060.32, 1060.32, -1208.84, -1208.84, -1208.84, -1421.37, -1421.37, -1421.37, -1421.37, -1421.37, -46.68, -46.68, -46.68, -46.68, -46.68],
    '2000': [1147.21, 1147.21, 1147.21, 627.68, 627.68, 1863.72, 1863.72, 1863.72, 1436.02, 1436.02, 1436.02, 1436.02, -1307.32, 1436.02, 1147.21, 1147.21, 1436.02, 1436.02, -1307.32, -1307.32, -1307.32, -34.45, -34.45, -34.45, -34.45, -34.45, 627.68, 627.68, 627.68, 627.68, 627.68],
    '2010': [1352.75, 1352.75, 1352.75, 1399.88, 1399.88, 5372.06, 5372.06, 5372.06, -1276.66, -1276.66, -1276.66, -1276.66, -4301.31, -1276.66, 1352.75, 1352.75, -1276.66, -1276.66, -4301.31, -4301.31, -4301.31, -2168.97, -2168.97, -2168.97, -2168.97, -2168.97, 1399.88, 1399.88, 1399.88, 1399.88, 1399.88],
    '2020': [294.55, 294.55, 294.55, 906.00, 906.00, 7869.66, 7869.66, 7869.66, -4156.96, -4156.96, -4156.96, -4156.96, -7700.75, -4156.96, 294.55, 294.55, -4156.96, -4156.96, -7700.75, -7700.75, -7700.75, -4450.38, -4450.38, -4450.38, -4450.38, -4450.38, 906.00, 906.00, 906.00, 906.00, 906.00]
}
df_data = pd.DataFrame(data_source)

# ==============================================================================
# 3. Data Processing
# ==============================================================================
try:
    df_data['SHENG_Code'] = df_data['PAC'] // 10000

    if not os.path.exists(map_file_path):
        raise FileNotFoundError(f"File not found: {map_file_path}")

    china_map = gpd.read_file(map_file_path)
    china_map['SHENG'] = china_map['SHENG'].astype(int)

    gdf = china_map.merge(df_data, left_on='SHENG', right_on='SHENG_Code', how='left')
    full_extent = china_map.total_bounds

except Exception as e:
    print(f"Data processing error: {e}")
    raise

# ==============================================================================
# 4. Helper Function
# ==============================================================================
def get_reasonable_ticks(vmin, vmax):
    s_vmin, s_vmax = vmin / 100, vmax / 100
    max_abs_s = max(abs(s_vmin), abs(s_vmax))

    # Include small step sizes to better handle earlier years with smaller values
    nice_steps = np.array([1, 2, 5, 10, 20, 25, 50, 100])
    target_step = max_abs_s / 2
    step_idx = (np.abs(nice_steps - target_step)).argmin()
    step = nice_steps[step_idx]

    potential_s_ticks = np.unique(
        np.array([0, step, 2 * step, 3 * step, 4 * step, -step, -2 * step, -3 * step, -4 * step])
    )
    final_s_ticks = potential_s_ticks[(potential_s_ticks >= s_vmin) & (potential_s_ticks <= s_vmax)]

    if 0 not in final_s_ticks:
        final_s_ticks = np.sort(np.append(final_s_ticks, 0))

    return final_s_ticks * 100


def integer_divide_by_100(x, pos):
    return f"{int(x / 100)}"

# ==============================================================================
# 5. Plotting
# ==============================================================================
plt.rcParams['font.family'] = 'Arial'
colors = ['#4575b4', '#74add1', '#e0f3f8', '#fee090', '#f46d43', '#d73027']
cmap = mcolors.LinearSegmentedColormap.from_list("OriginalRedBlue", colors)

fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()

years = ['1980', '1990', '2000', '2010', '2020']
labels = ['a', 'b', 'c', 'd', 'e']

for i, year in enumerate(years):
    ax = axes[i]

    # 1. Base map
    china_map.plot(ax=ax, color='#f0f0f0', edgecolor='white', linewidth=0.5, aspect=1)

    # 2. Data layer
    valid_data = gdf[year].dropna()
    if len(valid_data) > 0:
        current_gdf = gdf.dropna(subset=[year])
        vmin = valid_data.min()
        vmax = valid_data.max()
        norm = mcolors.TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)

        # Fill layer
        current_gdf.plot(column=year, ax=ax, cmap=cmap, norm=norm, edgecolor='face', linewidth=0.0, aspect=1)

        # Border layer
        dissolved_gdf = current_gdf.dissolve(by=year)
        dissolved_gdf.plot(ax=ax, facecolor='none', edgecolor='white', linewidth=0.8, aspect=1)

        # 3. Legend
        cax = ax.inset_axes([0.05, 0.22, 0.45, 0.04])
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm._A = []

        reasonable_ticks = get_reasonable_ticks(vmin, vmax)

        cbar = fig.colorbar(sm, cax=cax, orientation='horizontal', ticks=reasonable_ticks)
        cbar.ax.xaxis.set_major_formatter(ticker.FuncFormatter(integer_divide_by_100))
        cbar.ax.text(
            1.05, 0.5, "(Mt)",
            transform=cbar.ax.transAxes,
            va="center", ha="left",
            fontsize=20
        )

        # Update 1: label size to 18
        cbar.ax.tick_params(labelsize=18)

        # Update 2: size to 24, weight to normal, pad to 6
        # cbar.set_label(f"{year}yr (Mt)", size=20, weight='normal', labelpad=6)
        cbar.ax.xaxis.set_label_position('top')

    ax.set_xlim(full_extent[0], full_extent[2])
    ax.set_ylim(full_extent[1], full_extent[3])
    ax.axis('off')

fig.delaxes(axes[5])

plt.tight_layout()
plt.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02, wspace=0.01, hspace=0.05)

print(f"Saving image to: {save_path}")
plt.savefig(save_path, dpi=400, bbox_inches='tight')
plt.show()
print("Done!")
Fig.2f
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.path as mpath
import pandas as pd
import numpy as np
import os  # <--- [Revision 1] Import the os module

# ==========================================
# 1. Prepare data
# ==========================================
data = {
    'Year': ['1980', '1990', '2000', '2010', '2020'],
    'NE':   [6.7,  17.7, 1.9,  56.2, 79.6],
    'NC':   [0.0,  3.9,  7.4,  17.6, 17.6],
    'NW':   [0.0,  2.5,  1.1,  13.5, 22.6],
    'MLYR': [9.6,  14.0, 13.7, 12.2, 8.5],
    'SC':   [0.0,  0.0,  0.0,  0.0,  0.0],
    'SW':   [5.8,  9.6,  0.9,  0.0,  0.0]
}
df = pd.DataFrame(data)

# ==========================================
# 2. Plot parameter settings (larger font)
# ==========================================
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 22  # Increase global font size

colors = {
    'SW':   '#fcbba1',
    'SC':   '#fb6a4a',
    'MLYR': '#ef3b2c',
    'NW':   '#c6dbef',
    'NC':   '#9ecae1',
    'NE':   '#4292c6'
}

stack_order = ['NE', 'NC', 'NW', 'MLYR', 'SC', 'SW']

# ==========================================
# 3. Helper function: draw curly brace
# ==========================================
def draw_curly_brace(ax, x_pos, y_range, text):
    ymin, ymax = y_range
    ymid = (ymin + ymax) / 2
    x_len = 0.02

    path_data = [
        (mpath.Path.MOVETO, (x_pos, ymax)),
        (mpath.Path.CURVE4, (x_pos + x_len, ymax)),
        (mpath.Path.CURVE4, (x_pos + x_len, ymid + (ymax - ymid) / 4)),
        (mpath.Path.CURVE4, (x_pos + x_len * 2, ymid)),
        (mpath.Path.CURVE4, (x_pos + x_len, ymid - (ymax - ymid) / 4)),
        (mpath.Path.CURVE4, (x_pos + x_len, ymin)),
        (mpath.Path.CURVE4, (x_pos, ymin)),
    ]
    codes, verts = zip(*path_data)
    path = mpath.Path(verts, codes)

    patch = mpatches.PathPatch(
        path, facecolor='none', lw=1.0, edgecolor='black', transform=ax.transAxes
    )
    ax.add_patch(patch)

    ax.text(
        x_pos + x_len * 2.2, ymid, text, transform=ax.transAxes,
        ha='left', va='center', fontsize=22, color='black'
    )

# ==========================================
# 4. Main plotting logic
# ==========================================
fig, ax = plt.subplots(figsize=(7, 6))

bottom = np.zeros(len(df))
width = 0.62

for region in stack_order:
    values = df[region].values
    ax.bar(
        df['Year'], values, width=width, bottom=bottom,
        label=region, color=colors[region], edgecolor='none'
    )
    bottom += values

# --- Border settings ---
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(1.2)
    spine.set_color('black')

# --- Y-axis tick settings ---
ax.set_yticks(np.arange(0, 161, 40))
ax.set_ylim(0, 160)
ax.set_ylabel('Grain trade volume (Mt)', fontsize=22, labelpad=2)

# --- X-axis settings ---
ax.tick_params(axis='both', which='major', labelsize=22, direction='out', width=1.2)

# ==========================================
# 5. Custom legend (shifted left)
# ==========================================
leg_x = 0.03
leg_y_top = 0.96
box_h = 0.05
box_w = 0.08
spacing = 0.012

legend_items = ['SW', 'SC', 'MLYR', 'NW', 'NC', 'NE']
item_positions = {}

current_y = leg_y_top
for item in legend_items:
    rect = mpatches.Rectangle(
        (leg_x, current_y - box_h), box_w, box_h,
        facecolor=colors[item], transform=ax.transAxes, edgecolor='none'
    )
    ax.add_patch(rect)

    ax.text(
        leg_x + box_w + 0.02, current_y - box_h / 2, item,
        transform=ax.transAxes, va='center', ha='left', fontsize=20
    )

    item_positions[item] = (current_y, current_y - box_h)
    current_y -= (box_h + spacing)

# Calculate group ranges
south_top = item_positions['SW'][0]
south_bot = item_positions['MLYR'][1]
north_top = item_positions['NW'][0]
north_bot = item_positions['NE'][1]

# Draw braces
brace_x = leg_x + 0.23
draw_curly_brace(ax, brace_x, (south_bot, south_top), 'South')
draw_curly_brace(ax, brace_x, (north_bot, north_top), 'North')

plt.tight_layout()

# ==========================================
# 6. Save settings (updated path)
# ==========================================
# [Revision 2] Define the output directory path
# Note: the trailing backslash is removed to avoid escape issues
output_dir = r"E:\OneDrive\Python_me\paper_figures\1.trade_grain"

# Create the folder automatically if it does not exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Build the full output path
save_path = os.path.join(output_dir, 'grain_trade_chart_large_font.png')

plt.savefig(save_path, dpi=300, bbox_inches='tight')
plt.show()

print(f"Figure generated and saved to: {save_path}")
