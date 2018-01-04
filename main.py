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

def load_default_config():
    config = ConfigParser.RawConfigParser()
    
    config.add_section('IO Parameter')
    config.set('IO Parameter', 'input_path', 'data/data.csv')
    config.set('IO Parameter', 'output_path_prefix', 'output/')
    
    config.add_section('Sliding Parameter')
    config.set('Sliding Parameter', 'step_size', 0.002)
    config.set('Sliding Parameter', 'w_size', 0.05)
    config.set('Sliding Parameter', 'measure', 'cenken')
    config.set('Sliding Parameter', 'min_lng', -76.85)
    config.set('Sliding Parameter', 'max_lng', -76.15)
    config.set('Sliding Parameter', 'min_lat', 41.492)
    config.set('Sliding Parameter', 'max_lat', 42.008)
    config.set('Sliding Parameter', 'SKIP_THRES', 10)    
    
    
    config.add_section('FLAGS')
    config.set('FLAGS', 'NULL_FLAG', -10000000)
    config.write(open('sample.cfg', 'wb'))
    return config
    

def unpack_param(cfg):
    #  data, NULL_FLAG, SKIP_THRES, min_lng, max_lng, min_lat, max_lat, w_size, step_size)
    return {
        'NULL_FLAG': cfg.getint('FLAGS', 'NULL_FLAG'), 
        'SKIP_THRES': cfg.getint('Sliding Parameter', 'SKIP_THRES'),
        'min_lng': cfg.getfloat('Sliding Parameter', 'min_lng'),
        'max_lng': cfg.getfloat('Sliding Parameter', 'max_lng'), 
        'min_lat': cfg.getfloat('Sliding Parameter', 'min_lat'), 
        'max_lat': cfg.getfloat('Sliding Parameter', 'max_lat'), 
        'w_size': cfg.getfloat('Sliding Parameter', 'w_size'), 
        'step_size': cfg.getfloat('Sliding Parameter', 'step_size')        
    }

###############################################################################
# PARA
###############################################################################


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'loading default'
        cfg = load_default_config()
    else:
        cfg = ConfigParser.RawConfigParser().read(sys.argv[1]) 
         
    INPUT_PATH = cfg.get('IO Parameter', 'input_path')
    OUTPUT_PATH_PREFIX = cfg.get('IO Parameter', 'output_path_prefix')
    if not os.path.exists(OUTPUT_PATH_PREFIX):
        os.makedirs(OUTPUT_PATH_PREFIX)    
    
    data = np.loadtxt(INPUT_PATH, dtype=str, delimiter=',')
    
    data = np.array(data, dtype=float)
    slider = Slider(data, **unpack_param(cfg))
    slider.comput_heatmap()
    heatmap = slider.get_result_matrix()
    np.savetxt(OUTPUT_PATH_PREFIX + 'test', heatmap, delimiter=',', fmt='%s')