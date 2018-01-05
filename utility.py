# -*- coding: utf-8 -*-
"""
Created on Fri Jan 05 16:28:58 2018

@author: fxw133-admin
"""

import ConfigParser
import numpy as np


def generate_default_config():
    config = ConfigParser.RawConfigParser()
    
    config.add_section('IO Parameter')
    config.set('IO Parameter', 'input_path', 'data/data.csv')
    config.set('IO Parameter', 'output_folder', 'output/')
    config.set('IO Parameter', 'output_prefix', 'test')    
    
    config.add_section('Sliding Parameter')
    config.set('Sliding Parameter', 'step_size', 0.002)
    config.set('Sliding Parameter', 'w_size', 0.05)
    config.set('Sliding Parameter', 'measure', 'cenken')
    config.set('Sliding Parameter', 'min_lng', -76.85)
    config.set('Sliding Parameter', 'max_lng', -76.15)
    config.set('Sliding Parameter', 'min_lat', 41.492)
    config.set('Sliding Parameter', 'max_lat', 42.008)
    config.set('Sliding Parameter', 'SKIP_THRES', 10)    
    
    config.add_section('Drawing Parameter')
    config.set('Drawing Parameter', 'tick_number', 10)
    config.set('Drawing Parameter', 'tick_label_precision', 2)
    config.set('Drawing Parameter', 'dpi', 500)
    
    
    
    config.add_section('FLAGS')
    config.set('FLAGS', 'NULL_FLAG', -10000000)
    config.write(open('sample.cfg', 'wb'))
    return config
    

def unpack_method_param(cfg):
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

def unpack_drawing_param(cfg):
    #  data, NULL_FLAG, SKIP_THRES, min_lng, max_lng, min_lat, max_lat, w_size, step_size)
    return {
        'PRECISION': cfg.getint('Drawing Parameter', 'tick_label_precision'),
        'TICK_NUM': cfg.getint('Drawing Parameter', 'tick_number'),
        'DPI': cfg.getint('Drawing Parameter', 'dpi'),
        'OUTPUT_FOLDER': cfg.get('IO Parameter', 'output_folder'),
        'OUTPUT_PREFIX': cfg.get('IO Parameter', 'output_prefix')
    }
###############################################################################
# PARA
###############################################################################
def load_data(cfg):
    INPUT_PATH = cfg.get('IO Parameter', 'input_path')
    data = np.loadtxt(INPUT_PATH, dtype=str, delimiter=',')
    data = np.array(data, dtype=float)  
    return data
    