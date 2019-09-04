from __future__ import absolute_import, division, print_function, unicode_literals, unicode_literals

import pathlib

import matplotlib.pyplot as plt
import pandas as pd
import copy
import seaborn as sns
import numpy as np

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from collector.kospi_db_manager import KospiDBManager

class DataCustomizer:
    def __init__(self):
        print(tf.__version__)
    
    def initialize(self):
        self.dbManager = KospiDBManager("035420")
        self.dataframe = copy.deepcopy(self.dbManager.get_pd_db())
        self.to_numpy_array()
        self.norm()
    
    def to_numpy_array(self):
        self.np_dataset = np.transpose(
                            np.array([self.dataframe['Open'].values, 
                            self.dataframe['Close'].values,
                            self.dataframe['Volume'].values,
                            self.dataframe['Gradient'].values,
                            self.dataframe['PriceStatus'].values]))

    def norm(self):
        gradients = self.np_dataset[3]
        max = np.max(gradients)
        min = np.min(gradients)
        devide_num = 0.0
        if(abs(max) > abs(min)):
            devide_num = abs(max)
        else:
            devide_num = abs(min)
            
        self.np_dataset[3] = gradients / devide_num
        return self.np_dataset

    def divide_dataset(self):#TODO: return train, test dataset
        pass
    
    def print_pd_dataframe(self):
        print(self.dataframe.head)

    def load_data(self):
        self.initialize()
        return copy.deepcopy(self.np_dataset)

class Predictor:
    def __init__(self):
        print(tf.__version__)
    
    def load_data(self):
        self.customizer = DataCustomizer()
        self.dataset = self.customizer.load_data()
        self.customizer.print_pd_dataframe()
        print(self.dataset.shape)
        print(self.dataset)

    def check_predictor(self):
        self.load_data()

if __name__ == '__main__':
    print(tf.__version__)
