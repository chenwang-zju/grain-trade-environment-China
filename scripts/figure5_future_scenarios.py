Fig.5
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.lines import Line2D
import numpy as np
from scipy.interpolate import PchipInterpolator
from pathlib import Path
import os

# ==========================================
# 0. Path settings
# ==========================================
# Input file path
input_file_path = r"E:\OneDrive\stata\Grain_data\Future_Env_Tax_Formatted_Resultsnew12.xlsx"

# Output directory
output_dir = Path(r"E:\OneDrive\Python_me\paper_figures\1.trade_grain")
output_dir.mkdir(parents=True, exist_ok=True)

# ==========================================
    df = pd.DataFrame(data)

df['scenario'] = df['scenario'].astype(str)
df['scenario_label'] = df['scenario'].apply(lambda x: x if str(x).endswith('s') else str(x) + 's')

# ==========================================
# 2. Plot parameter settings
# ==========================================
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.weight'] = 'normal'
plt.rcParams['font.size'] = 22

# Plot configuration
plot_configs = [
    {
        "col": "VL",
        "title": "Virtual Cropland (Mha)",
        "color_list": ["#a1d99b", "#74c476", "#238b45"]
    },
    {
        "col": "VW",
        "title": "Virtual Water (Gm$^3$)",
        "color_list": ["#9ecae1", "#6baed6", "#2171b5"],
        "y_step": 5
    },
    {
        "col": "totN",
        "title": "N emissions (Mt N)",
        "color_list": ["#fcbba1", "#fb6a4a", "#cb181d"]
    },
    {
        "col": "totC_net",
        "title": "Net GHG emissions (Mt CO$_2$-eq)",
        "color_list": ["#dadaeb", "#9e9ac8", "#54278f"]
    }
]

scenarios_order = ["126s", "245s", "585s"]
markers = ["o", "s", "D"]

# ==========================================
# 3. Start plotting
# ==========================================
# Key adjustment: figsize=(26, 6) makes the figure flatter
fig, axes = plt.subplots(1, 4, figsize=(26, 6), constrained_layout=True)

for i, config in enumerate(plot_configs):
    ax = axes[i]
    var_name = config["col"]
    colors = config["color_list"]

    for j, scen in enumerate(scenarios_order):
        sub_df = df[df['scenario_label'] == scen].sort_values("year")
        x = sub_df["year"].values
        y = sub_df[var_name].values

        # PCHIP interpolation
        x_smooth = np.linspace(x.min(), x.max(), 300)
        interpolator = PchipInterpolator(x, y)
        y_smooth = interpolator(x_smooth)

        # Plot lines and markers
        ax.plot(x_smooth, y_smooth, linestyle='-', linewidth=3.5, color=colors[j], alpha=0.95)
        ax.plot(x, y, marker=markers[j], markersize=12, linestyle='None', color=colors[j], zorder=10)

    # Title and style
    ax.set_title(config["title"], loc='left', fontsize=28, fontweight='normal', pad=10)

    # Axes
    ax.set_xticks([2030, 2040, 2050, 2060])
    ax.set_xlabel("", fontsize=0)

    if "y_step" in config:
        ax.yaxis.set_major_locator(ticker.MultipleLocator(config["y_step"]))
    else:
        ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=5))

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)
    ax.tick_params(axis='both', which='major', labelsize=26, width=1.5, length=7)

# ==========================================
# 4. Legend settings (with light-to-dark distinction)
# ==========================================
legend_colors = ["#BFBFBF", "#7F7F7F", "#2F2F2F"]  # Light, Medium, Dark

legend_elements = [
    Line2D([0], [0], color=legend_colors[0], marker='o', label='SSP1-2.6', markersize=18, linestyle='-', linewidth=3),
    Line2D([0], [0], color=legend_colors[1], marker='s', label='SSP2-4.5', markersize=18, linestyle='-', linewidth=3),
    Line2D([0], [0], color=legend_colors[2], marker='D', label='SSP5-8.5', markersize=18, linestyle='-', linewidth=3)
]

# Because the figure is flatter, move the legend slightly upward to avoid overlapping the titles
fig.legend(
    handles=legend_elements,
    loc='upper center',
    bbox_to_anchor=(0.5, 1.15),
    ncol=3,
    frameon=False,
    fontsize=28,
    handletextpad=0.4,
    columnspacing=3.0,
    handlelength=2.5
)

# ==========================================
# 5. Multi-format output (PNG + PDF + SVG)
# ==========================================
png_path = output_dir / "Future_Results_Flat_PCHIP211ok1.png"
pdf_path = output_dir / "Future_Results_Flat_PCHIP211ok1.pdf"
svg_path = output_dir / "Future_Results_Flat_PCHIP211ok1.svg"

# PNG (raster, high resolution)
plt.savefig(png_path, dpi=400, bbox_inches='tight')
plt.savefig(pdf_path, bbox_inches='tight')
plt.savefig(svg_path, bbox_inches='tight')

# EMF conversion (recommended)
os.system(f'inkscape "{svg_path}" --export-type=emf')

print("All formats saved.")

Fig.c b
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
# Update filename to reflect larger font size
save_path = os.path.join(output_dir, "SSP245_Grain_Surplus_2030_2060_LargeLegendOK.png")

# ==============================================================================
# 2. Prepare Data (SSP2-4.5 Scenario from image_ce008e.png)
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
    '2030': [
        -1677.0, -1677.0, -1677.0, -348.5, -348.5,
        6150.5, 6150.5, 6150.5,
        -4959.9, -4959.9, -4959.9, -4959.9, -9545.1, -4959.9, -1677.0,
        -1677.0, -4959.9, -4959.9, -9545.1, -9545.1, -9545.1,
        -5464.3, -5464.3, -5464.3, -5464.3, -5464.3,
        -348.5, -348.5, -348.5, -348.5, -348.5
    ],
    '2060': [
        -1421.9, -1421.9, -1421.9, 548.7, 548.7,
        7722.1, 7722.1, 7722.1,
        -3500.5, -3500.5, -3500.5, -3500.5, -8690.5, -3500.5, -1421.9,
        -1421.9, -3500.5, -3500.5, -8690.5, -8690.5, -8690.5,
        -4051.8, -4051.8, -4051.8, -4051.8, -4051.8,
        548.7, 548.7, 548.7, 548.7, 548.7
    ]
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
# 4. Helper Function: Reasonable Integer Ticks (Divide by 100)
# ==============================================================================
def get_reasonable_ticks(vmin, vmax):
    s_vmin, s_vmax = vmin / 100, vmax / 100
    max_abs_s = max(abs(s_vmin), abs(s_vmax))
    nice_steps = np.array([1, 2, 5, 10, 20, 25, 50, 100])
    target_step = max_abs_s / 2
    step_idx = (np.abs(nice_steps - target_step)).argmin()
    step = nice_steps[step_idx]
    potential_s_ticks = np.unique(np.array([0, step, 2*step, 3*step, 4*step, -step, -2*step, -3*step, -4*step]))
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

fig, axes = plt.subplots(1, 2, figsize=(14, 8))
axes = axes.flatten()

years = ['2030', '2060']

for i, year in enumerate(years):
    ax = axes[i]
    
    # 1. Base Map (Grey)
    china_map.plot(ax=ax, color='#f0f0f0', edgecolor='white', linewidth=0.5, aspect=1)
    
    # 2. Data Layer
    valid_data = gdf[year].dropna()
    if len(valid_data) > 0:
        current_gdf = gdf.dropna(subset=[year])
        vmin = valid_data.min()
        vmax = valid_data.max()
        norm = mcolors.TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)

        # Fill Layer
        current_gdf.plot(column=year, ax=ax, cmap=cmap, norm=norm, edgecolor='face', linewidth=0.0, aspect=1)
        # Border Layer
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
        # [Revision 1: Increased legend number size] (from 14 to 18)
        cbar.ax.tick_params(labelsize=18) 
        
        # [Revision 2: Increased legend title size, added padding] (size from 16 to 24, labelpad from 4 to 6)
        #cbar.set_label(f"{year}yr (Mt)", size=24, labelpad=6)
        cbar.ax.xaxis.set_label_position('top') 

    ax.set_xlim(full_extent[0], full_extent[2])
    ax.set_ylim(full_extent[1], full_extent[3])
    ax.axis('off')

plt.tight_layout()
plt.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02, wspace=0.05)

print(f"Saving image to: {save_path}")
plt.savefig(save_path, dpi=400, bbox_inches='tight')
plt.show()
print("Done!")

Fig.d
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from pathlib import Path

# ==========================================
# 0. Path settings
# ==========================================
output_dir = Path(r"F:\OneDrive\Python_me\paper_figures\1.trade_grain")
output_dir.mkdir(parents=True, exist_ok=True)

# ==========================================
# 1. Prepare data
# ==========================================
data = {
    '2030': [-5.9, -0.3, 0.1, 1.3, 2.2, 4.4],
    '2040': [-6.0, 0.2, -0.7, 1.5, 2.2, 4.0],
    '2050': [-6.2, 0.8, -0.5, 1.8, 2.1, 3.5],
    '2060': [-6.8, 0.7, -1.4, 0.8, 4.7, 3.2]
}
index_labels = ['NE', 'NC', 'NW', 'MLYR', 'SC', 'SW']

df = pd.DataFrame(data, index=index_labels)

# ==========================================
# 2. Define color map (unchanged)
# ==========================================
custom_colors = ["#479c96", "#d1ebe8", "#ffffff", "#fbe0c9", "#ca8845"]
cmap = mcolors.LinearSegmentedColormap.from_list("custom_teal_orange", custom_colors, N=256)

# ==========================================
# 3. Plot parameter settings
# ==========================================
plt.rcParams['font.family'] = 'Arial'
# Increase global font size
plt.rcParams['font.size'] = 20 

# Slightly increase canvas size to prevent crowded large fonts
fig, ax = plt.subplots(figsize=(10, 7.5))

# Define range
limit = max(abs(df.min().min()), abs(df.max().max()))
v_limit = 7 

# ==========================================
# 4. Draw heatmap (Core modification)
# ==========================================
sns.heatmap(df, 
            ax=ax,
            cmap=cmap,           
            center=0,            
            annot=True,          
            fmt=".1f",           
            vmin=-v_limit,       
            vmax=v_limit,        
            linewidths=1.5,      # Slightly thicken the division lines
            linecolor='#e0e0e0', # <--- [Modification] Lighter color (light gray)
            annot_kws={"size": 24, "color": "black"}, # <--- [Modification] Increase font size to 24
            cbar_kws={'label': ''} 
           )

# ==========================================
# 5. Detail adjustments
# ==========================================
# Adjust coordinate axis label font size (increase to 22)
ax.tick_params(axis='x', labelsize=26, rotation=0) 
ax.tick_params(axis='y', labelsize=26, rotation=0) 

# Adjust color bar
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=24) # Increase tick font size
cbar.ax.text(0.5, -0.06, '(Billion USD)', transform=cbar.ax.transAxes, 
             ha='center', va='top', fontsize=26, color='black')


# Remove axis titles
ax.set_xlabel("")
ax.set_ylabel("")

# ==========================================
# 6. Save and display
# ==========================================
plt.tight_layout()
save_path = output_dir / "Tax_Subsidy_Heatmap_SSP245.png"
plt.savefig(save_path, dpi=300, bbox_inches='tight')
plt.show()

print(f"✅ Font enlarged heatmap has been generated and saved to: {save_path}")
