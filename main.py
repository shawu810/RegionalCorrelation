# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 16:53:34 2017

@author: Fei Wu
"""


import ConfigParser
import numpy as np
import sys
import os
from Slider import Slider
from drawing import draw_heat_map

from utility import unpack_drawing_param
from utility import unpack_method_param
from utility import load_data

if __name__ == '__main__':
    cfg = ConfigParser.RawConfigParser()
    if len(sys.argv) == 1:
        print 'loading default'
        cfg.read('sample.cfg')
    else:
        cfg.read(sys.argv[1])
         
    
    OUTPUT_FOLDER = cfg.get('IO Parameter', 'output_folder')
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)    
    OUTPUT_PREFIX = cfg.get('IO Parameter', 'output_prefix')
    
    slider = Slider()
    slider.set_data(load_data(cfg))
    slider.set_param(**unpack_method_param(cfg))
    slider.compute_heatmap()
    
    heatmap = slider.get_coor_matrix()
    datamap = slider.get_data_count_matrix()
    
    np.savetxt(OUTPUT_FOLDER + OUTPUT_PREFIX + '_corr_matrix.csv', 
               heatmap, delimiter=',', fmt='%s')
    np.savetxt(OUTPUT_FOLDER + OUTPUT_PREFIX + '_data_count_matrix.csv', 
               datamap, delimiter=',', fmt='%s')
    
    ## drawing
    draw_heat_map(slider, **unpack_drawing_param(cfg))
