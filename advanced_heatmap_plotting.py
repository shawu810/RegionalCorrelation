# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 17:06:58 2019

@author: Tao Wen (Penn State University and Syracuse University; jaywen.com)
"""

# need to install geopandas package first
import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

# setting up the prefix of input and output files
prefix = "test"
feature_folder = "mapfeatures/"
output_folder = "output/"

# import sliding window output for plotting
matrix = pd.read_csv("./output/" + prefix + "_corr_matrix.csv")
count_matrix = pd.read_csv("./output/" + prefix + "_data_count_matrix.csv")

# import shapefiles
bradford_boundary = gpd.read_file(feature_folder + "Bradford_County.shp")
bradford_twp = gpd.read_file(feature_folder + "Bradford_Townships.shp")
anticlines = gpd.read_file(feature_folder + "Bradford_Anticlines.shp")
faults = gpd.read_file(feature_folder + "Bradford_Faults.shp")
problematic_wells = gpd.read_file(feature_folder + "Five_shale_gas_wells.shp")

## plot basemap layers
f, ax = plt.subplots(1)
bradford_boundary.to_crs(epsg=4326).plot(ax=ax, facecolor='None', edgecolor="black")
bradford_twp.to_crs(epsg=4326).plot(ax=ax, facecolor="None",edgecolor="gray", alpha=0.5)
anticlines.to_crs(epsg=4326).plot(ax=ax, color="red")
faults.plot(ax=ax, color="black",linestyle="--")
problematic_wells.to_crs(epsg=4326).plot(ax=ax, marker='X', color='green', markersize=100)
plt.xlim(-77,-76)
plt.ylim(41.4,42.1)

## plot heatmap layer
norm = mpl.colors.Normalize(vmin=-1.,vmax=1.)
norm2 = mpl.colors.Normalize(vmin=0.,vmax=1.)

plt.imshow(matrix, extent=[-77, -76, 41.4, 42.1], cmap ='bwr_r', norm=norm)
plt.colorbar()

plt.imshow(count_matrix==0, extent=[-77, -76, 41.4, 42.1], cmap='binary', norm=norm2, alpha=0.1)

## save plot to file
plt.savefig(output_folder + prefix + "_advanced_heatmap.pdf",dpi=300)