# -*- coding: utf-8 -*-
"""
Created on Fri Jan 05 13:16:37 2018

@author: fxw133-admin
"""
import matplotlib as mpl
mpl.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import ConfigParser

from Slider import Slider
from utility import unpack_drawing_param
from utility import unpack_method_param


def draw_heat_map(slider, 
                  TICK_NUM, PRECISION, DPI, OUTPUT_FOLDER, OUTPUT_PREFIX):
    min_x = slider.min_x
    max_x = slider.max_x
    
    min_y = slider.min_y
    max_y = slider.max_y
    

    matrix = slider.get_coor_matrix()
    data_matrix = slider.get_data_count_matrix()
    
    y_v_length, x_v_length = matrix.shape
    index_x = np.linspace(1,x_v_length,TICK_NUM)
    index_y = np.linspace(1,y_v_length,TICK_NUM)
    value_x = np.around(min_x + (index_x-1)/x_v_length*(max_x-min_x), decimals=PRECISION)
    value_y = np.around(max_y - (index_y-1)/y_v_length*(max_y-min_y), decimals=PRECISION)
    
    
    
    norm = mpl.colors.Normalize(vmin=-1.,vmax=1.)
    norm2 = mpl.colors.Normalize(vmin=0.,vmax=1.)
    
    
    handler = plt.imshow(matrix, cmap ='bwr_r', norm=norm)
    handler.axes.set_xticks(index_x)
    handler.axes.set_xticklabels(value_x)
    handler.axes.set_yticks(index_y)
    handler.axes.set_yticklabels(value_y)
    
    plt.colorbar()
    plt.imshow(data_matrix==0, cmap='binary', norm=norm2, alpha=0.1)
    plt.savefig(OUTPUT_FOLDER + OUTPUT_PREFIX + '_heatmap.pdf',dpi=DPI)



if __name__ == '__main__':
    cfg = ConfigParser.RawConfigParser()
    if len(sys.argv) == 1:
        print 'loading default for drawing'
        cfg.read('sample.cfg')
    else:
        cfg.read(sys.argv[1])
         
    
    OUTPUT_FOLDER = cfg.get('IO Parameter', 'output_folder')
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)    
    OUTPUT_PREFIX = cfg.get('IO Parameter', 'output_prefix')
    
    slider = Slider()
    heatmap = np.loadtxt(OUTPUT_FOLDER + OUTPUT_PREFIX + '_corr_matrix.csv', 
                         dtype=float, delimiter=',')
    datamap = np.loadtxt(OUTPUT_FOLDER + OUTPUT_PREFIX + '_data_count_matrix.csv', 
                         dtype=float, delimiter=',')
    slider.set_param(**unpack_method_param(cfg))
    slider.set_result(heatmap, datamap)
    
    ## drawing
    draw_heat_map(slider, **unpack_drawing_param(cfg))
