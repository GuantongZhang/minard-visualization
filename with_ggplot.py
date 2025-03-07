import numpy as np
import pandas as pd
from plotnine import (
    ggplot, aes, geom_path, geom_point, geom_text, geom_line, scale_size, scale_color_manual,
    theme_classic, labs, theme, element_text, xlim, ylim, coord_fixed
)

# Load data
cities = pd.read_csv('ggplot2-minard-gallery/cities.txt', sep='\s+')
temps = pd.read_csv('ggplot2-minard-gallery/temps.txt', sep='\s+')
troops = pd.read_csv('ggplot2-minard-gallery/troops.txt', sep='\s+')

# Route plot
combined_plot = (
    ggplot() +
    geom_path(data=troops, mapping=aes(x="long", y="lat", group="group", size="survivors", color="direction")) +
    geom_path(data=troops, mapping=aes(x="long", y="lat", group="group", size="survivors", color="direction")) +
    geom_text(data=cities, mapping=aes(x="long", y="lat", label="city"), ha="left", va="bottom", size=8, nudge_y=0.1) +
    scale_color_manual(
        values={"A": "#F14A37", "R": "#755FD4"},
        labels={"A": "Advance", "R": "Retreat"}
    ) +
    scale_size(range=(0.5, 5), breaks=[10000, 20000, 50000, 100000]) +
    labs(title="Napoleon’s March to Moscow", x="Longitude", y="Latitude", color="Group") +
    theme_classic() +
    coord_fixed(ratio=3.5) +
    xlim(24, 40) +
    ylim(54, 56)
)

# Temperature plot
temp_plot = (
    ggplot(temps, aes(x="long", y="temp")) +
    geom_line(color="grey", size=2) +
    geom_point(color="black", size=3) +
    geom_text(aes(label="date"), ha="center", va="top", size=6, nudge_y=-1) +
    labs(x="Longitude", y="Temperature (°C)") +
    theme(axis_title_y=element_text(size=8), axis_title_x=element_text(size=8)) +
    xlim(24, 43.32)
)

# Save the combined plot
combined_plot.save("napoleon_march.png", dpi=300)

# Save the temperature plot
temp_plot.save("temperature_plot.png", dpi=300)