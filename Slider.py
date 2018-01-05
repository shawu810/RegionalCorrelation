# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 15:54:41 2017

@author: Fei Wu
"""
import numpy as np
from ktau_p import ktau_p

class Slider:
    
    def __init__(self, data, NULL_FLAG, SKIP_THRES, min_lng, max_lng, min_lat, max_lat, w_size, step_size):
        self.data = data   
        self.NULL_FLAG = NULL_FLAG
        self.SKIP_THRES = SKIP_THRES
        self.min_x = min_lng
        self.max_x = max_lng
        self.min_y = min_lat
        self.max_y = max_lng
        self.w_size = w_size
        self.step_size = step_size
        
        # Initialization     
        index_step = self.w_size // self.step_size
        bound_min_x = min_lng - w_size
        bound_max_x = max_lng + w_size
        bound_min_y = min_lat - w_size
        bound_max_y = max_lat + w_size
        
        self.step_coor_x = np.arange(bound_min_x, bound_max_x, step_size)
        self.step_coor_y = np.arange(bound_min_y, bound_max_y, step_size)
        self.matrix_x_len = len(self.step_coor_x) 
        self.matrix_y_len = len(self.step_coor_y)
        self.result_matrix =  np.zeros((self.matrix_x_len, self.matrix_y_len)) # * self.NULL_FLAG * index_step**2
        self.has_data_matrix = np.zeros((self.matrix_x_len, self.matrix_y_len))
        self.x_index, self.xcen_index, self.y_index, self.ycen_index = 2, 3, 4, 5
        
    def get_coor_matrix(self):
        return np.transpose(self.result_matrix[:,::-1])
   
    def get_data_count_matrix(self):
        return np.transpose(self.has_data_matrix[:,::-1])
   
    def comput_heatmap(self):
        index_step = self.w_size // self.step_size
        for i in range(self.matrix_x_len):
            ori_x = self.step_coor_x[i]
            for j in range(self.matrix_y_len):
                if i % 10 == 0 and j % 10 == 0:
                    print '{} out of {}, and {} out of {}'.format(i, self.matrix_x_len, j, self.matrix_y_len)
                ori_y = self.step_coor_y[j]
                inwindow_data = self.get_data_within_window(ori_x, ori_y, self.w_size, self.data)
                
                if len(inwindow_data) < self.SKIP_THRES:
                    continue
                
                view = self.result_matrix[i:i+index_step+1, j:j+index_step+1]
                has_data_view = self.has_data_matrix[i:i+index_step+1, j:j+index_step+1] 
                has_data_view += 1
                #view[np.where(view ==  self.NULL_FLAG)] = 0.0
                v, p = ktau_p(inwindow_data[:, self.x_index], inwindow_data[:, self.xcen_index], 
                              inwindow_data[:, self.y_index], inwindow_data[:, self.ycen_index])
                    
                if p >= 0.05:
                    continue
                if v > 0:
                    view += 1
                elif v < 0:
                    view -= 1
                    
        self.result_matrix = self.result_matrix[index_step+1:-index_step+1, 
                                          index_step+1:-index_step+1] # crop
        self.has_data_matrix = self.has_data_matrix[index_step+1:-index_step+1, 
                                          index_step+1:-index_step+1]
        self.result_matrix /= float(index_step**2) 
        #self.result_matrix = np.transpose(self.result_matrix[:,::-1])
        #return self.result_matrix
        
    
    def inbox(self, x, y, ori_x, ori_y, w_size):
        return (x >= ori_x and x < ori_x + w_size and y >= ori_y and y <= ori_y + w_size) ## x in the matrix, left inclusive            
    
    def get_data_within_window(self, ori_x, ori_y, w_size, data):
        # calling filter for linear scanning
        return np.array(filter(lambda x: self.inbox(x[0], x[1], ori_x, ori_y, w_size), data))
    
            