import numpy as np
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D

# Load data
cities = pd.read_csv('ggplot2-minard-gallery/cities.txt', delim_whitespace=True)
temps = pd.read_csv('ggplot2-minard-gallery/temps.txt', delim_whitespace=True)
troops = pd.read_csv('ggplot2-minard-gallery/troops.txt', delim_whitespace=True)

# Group
advances = troops[troops['direction']=='A']
retreats = troops[troops['direction']=='R']

# Define GDF
gdf = geopandas.GeoDataFrame(
    cities,
    geometry=geopandas.points_from_xy(cities.long, cities.lat)
)

# Set frames
fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(25,12), gridspec_kw={'height_ratios': [5, 1]})

# Set colors
advance_colors = ["#F14A37", "#F17566", "#F1BFB5"] #reds
retreat_colors = ["#755FD4", "#9A92D4", "#B4A9D7"] #purples

# Routes
for grp in [1,2,3]:
    advances_grp = advances[advances['group']==grp]
    retreats_grp = retreats[retreats['group']==grp]

    # Advances
    lwidths = advances_grp.survivors/6000
    points = np.array([advances_grp.long, advances_grp.lat]).T.reshape(-1, 1, 2)
    advance_segments = np.concatenate([points[:-1], points[1:]], axis=1)
    lc = LineCollection(advance_segments, linewidth= lwidths, color=advance_colors[grp-1], capstyle='round', zorder=2, label=f"Group_Advance {grp}")
    ax1.add_collection(lc)

    # Retreats
    lwidths = retreats_grp.survivors/6000
    points = np.array([retreats_grp.long, retreats_grp.lat]).T.reshape(-1, 1, 2)
    retreat_segments = np.concatenate([points[:-1], points[1:]], axis=1)
    lc = LineCollection(retreat_segments, linewidth= lwidths, color=retreat_colors[grp-1], capstyle='round', zorder=1, label=f"Group_Retreat {grp}")
    ax1.add_collection(lc)

# Annotate cities
for x, y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf.city):
    ax1.annotate(label, xy=(x, y), xytext=(0, 0), textcoords="offset points", zorder=3, fontsize=12, weight='bold')

# Set axes
ax1.set_xlim(23, 38)
ax1.set_ylim(54, 57)

ax1.annotate(r"Napolean's March to Moscow", (23.75, 56.5), fontsize=60)
ax1.annotate("A reproduction of Charles Minard's visualization", (23.75, 56.25), fontsize=20, weight='bold')
ax1.set_ylabel("Latitude", fontsize=14)

# Survivor legend
legend_dict = {'Advance Group 1':advance_colors[0], 'Advance Group 2':advance_colors[1], 'Advance Group 3':advance_colors[2],
               'Retreat Group 1':retreat_colors[0], 'Retreat Group 2':retreat_colors[1], 'Retreat Group 3':retreat_colors[2]}
survivor_sizes = [10000, 20000, 50000, 100000]
legend_lines = [Line2D([0], [0], color='black', linewidth=s/6000, label=s) for s in survivor_sizes]
legend1 = ax1.legend(handles=legend_lines, title="Survivors", title_fontsize=16, fontsize=16, frameon=False)

# Group legend
patchList = []
for key in legend_dict:
    data_key = mpatches.Patch(color=legend_dict[key], label=key)
    patchList.append(data_key)
legend2 = ax1.legend(handles=patchList, ncol=2, bbox_to_anchor=(1, 0.2), fontsize=16, frameon=False)
ax1.add_artist(legend1)

# Temperature
ax2.plot(temps.long, temps.temp, color='grey', linewidth=2, marker='o', markersize=5, label='Temperature')
for x, y, label in zip(temps.long, temps.temp, temps.date):
    ax2.annotate(label, xy=(x, y), xytext=(0, -10), textcoords="offset points", 
                 ha='center', fontsize=12, color='black', weight='bold')
# Formatting
ax2.set_xlim(23, 38)
ax2.set_ylim(temps.temp.max() + 5, temps.temp.min() - 5)
ax2.invert_yaxis()
ax2.set_xlabel("Longitude", fontsize=14)
ax2.set_ylabel("Temperature (°C)", fontsize=14)
ax2.axhline(0, color='gray', linestyle='dashed', linewidth=1)
ax2.legend(bbox_to_anchor=(0.13, 0.9), fontsize=16)
ax2.grid(True, linestyle='dashed', alpha=0.6)

plt.show()