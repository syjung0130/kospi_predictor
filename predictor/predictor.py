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
    
    def load_dataframe(self):
        self.dbManager = KospiDBManager("035420")
        self.dataframe = copy.deepcopy(self.dbManager.get_pd_db())

    def normalize(self):
        gradients = self.dataframe['Gradient'].values
        max = np.max(gradients)
        min = np.min(gradients)
        devide_num = 0.0
        if(abs(max) > abs(min)):
            devide_num = abs(max)
        else:
            devide_num = abs(min)
        
        gradients = gradients / devide_num
        self.dataframe['Gradient'] = pd.Series(gradients)

    def customize_dataframe(self):
        self.normalize()

    def to_numpy_dataset_array(self):
        self.np_dataset = np.transpose(
                            np.array([
                            self.dataframe['Open'].values, 
                            self.dataframe['Close'].values,
                            self.dataframe['Volume'].values,
                            ]))
    
    def to_numpy_label_array(self):
        self.np_gradient_label = np.transpose(
                            np.array([
                            self.dataframe['Gradient'].values
                            ]))
        self.np_pricestatus_label = np.transpose(
                            np.array([
                            self.dataframe['PriceStatus'].values
                            ]))

    def to_numpy_array(self):
        self.to_numpy_dataset_array()
        self.to_numpy_label_array()
    
    def print_pd_dataframe(self):
        print(self.dataframe.head)

    def load_data(self):
        self.load_dataframe()
        self.customize_dataframe()
        self.to_numpy_array()
        dim = self.np_dataset.shape
        print("0: {0}, 1: {1}".format(dim[0], dim[1]))
        print("0: {0}, 1: {1}".format(self.np_dataset.shape[0], self.np_dataset.shape[1]))
        
        # divide dataset
        row_length = self.np_dataset.shape[0]
        train_dataset_length = int(row_length * 0.8)
        return (self.np_dataset[:train_dataset_length], self.np_dataset[train_dataset_length:])
    
    def get_gradient_labels(self):
        print("gradient_labels: ({0})\n{1}".format(self.np_gradient_label.shape, self.np_gradient_label))
        return self.np_gradient_label

    def get_pricestatus_labels(self):
        print("pricestatus_labels: ({0})\n{1}".format(self.np_pricestatus_label.shape, self.np_pricestatus_label))
        return self.np_pricestatus_label

class Predictor:
    def __init__(self):
        print(tf.__version__)
    
    def load_data(self):
        self.customizer = DataCustomizer()
        (self.train_dataset, self.test_dataset) = self.customizer.load_data()
        self.customizer.print_pd_dataframe()
        print("train, test shape: ({0}, {1})".format(self.train_dataset.shape, self.test_dataset.shape))
        print("train dataset: \n {0}".format(self.train_dataset))
        print("train dataset: \n {0}".format(self.test_dataset))
        return copy.deepcopy((self.train_dataset, self.test_dataset))
    
    def get_gradient_labels(self):
        return copy.deepcopy(self.customizer.get_gradient_labels())
    
    def get_pricestatus_labels(self):
        return copy.deepcopy(self.customizer.get_pricestatus_labels())

    def check_predictor(self):
        (train_data, test_data) = self.load_data()
        gradient_labels = self.get_gradient_labels()
        price_labels = self.get_pricestatus_labels()

if __name__ == '__main__':
    print(tf.__version__)
