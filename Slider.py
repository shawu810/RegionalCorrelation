# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 15:54:41 2017

@author: Fei Wu
"""
import numpy as np
from ktau_p import ktau_p



class Slider:
    def __init__(self):
        self.result_matrix = None
        self.has_data_matrix = None
    
    def set_data(self, data):
        self.data = data
        
    def set_result(self, result_matrix, has_data_matrix):
        self.has_data_matrix = has_data_matrix
        self.result_matrix = result_matrix        
        
    def set_param(self, NULL_FLAG, SKIP_THRES, min_lng, max_lng, min_lat, max_lat, w_size, step_size):   
        self.NULL_FLAG = NULL_FLAG
        self.SKIP_THRES = SKIP_THRES
        self.min_x = min_lng
        self.max_x = max_lng
        self.min_y = min_lat
        self.max_y = max_lat
        self.w_size = w_size
        self.step_size = step_size
        self.x_index, self.xcen_index, self.y_index, self.ycen_index = 2, 3, 4, 5        
                     
                
    def get_coor_matrix(self):
        return self.result_matrix
   
    def get_data_count_matrix(self):
        return self.has_data_matrix
   
    def compute_heatmap(self):
        #### para initial
        # Initialization     
        w_size = self.w_size
        step_size = self.step_size
        index_step = int(self.w_size // self.step_size)
        bound_min_x = self.min_x - w_size
        bound_max_x = self.max_x + w_size
        bound_min_y = self.min_y - w_size
        bound_max_y = self.max_y + w_size
        
        step_coor_x = np.arange(bound_min_x, bound_max_x, step_size)
        step_coor_y = np.arange(bound_min_y, bound_max_y, step_size)
        matrix_x_len = len(step_coor_x) 
        matrix_y_len = len(step_coor_y)
        self.result_matrix =  np.zeros((matrix_x_len, matrix_y_len)) # * self.NULL_FLAG * index_step**2
        self.has_data_matrix = np.zeros((matrix_x_len, matrix_y_len))
        

        for i in range(matrix_x_len):
            ori_x = step_coor_x[i]
            for j in range(matrix_y_len):
                if i % 10 == 0 and j % 10 == 0:
                    print '{} out of {}, and {} out of {}'.format(i, matrix_x_len, j, matrix_y_len)
                ori_y = step_coor_y[j]
                inwindow_data = self.get_data_within_window(ori_x, ori_y, w_size, self.data)
                
                if len(inwindow_data) < self.SKIP_THRES:
                    continue
                
                view = self.result_matrix[i:int(i+index_step+1), 
                                          j:int(j+index_step+1)]
                has_data_view = self.has_data_matrix[i:int(i+index_step+1), j:int(j+index_step+1)] 
                has_data_view += 1
                #view[np.where(view ==  self.NULL_FLAG)] = 0.0
                v, p = ktau_p(inwindow_data[:, self.x_index], 
                                inwindow_data[:, self.xcen_index], 
                              inwindow_data[:, self.y_index], 
                                inwindow_data[:, self.ycen_index])
                    
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
        

        self.result_matrix = np.transpose(self.result_matrix[:,::-1])
        self.has_data_matrix = np.transpose(self.has_data_matrix[:,::-1])
                

        
    
    def inbox(self, x, y, ori_x, ori_y, w_size):
        return (x >= ori_x and x < ori_x + w_size and y >= ori_y and y <= ori_y + w_size) ## x in the matrix, left inclusive            
    
    def get_data_within_window(self, ori_x, ori_y, w_size, data):
        # calling filter for linear scanning
        return np.array(filter(lambda x: self.inbox(x[0], x[1], ori_x, ori_y, w_size), data))
    
            