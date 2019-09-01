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

class Predictor:
    def __init__(self):
        print(tf.__version__)

    def get_dataset(self):
        dbManager = KospiDBManager("035420")
        return copy.deepcopy(dbManager.get_pd_db())

    # 정규화, 수치를 스케일링
    def norm(self, dataset):
        # print('type {0}, {1}'.format(type(dataset), type(dataset['Gradient'])))
        # print('type {0}'.format(type(dataset['Gradient'].values)))
        
        max = np.max(dataset['Gradient'])
        min = np.min(dataset['Gradient'])        
        devide_num = 0.0
        if(abs(max) > abs(min)):
            devide_num = abs(max)
        else:
            devide_num = abs(min)
            
        dataset['Gradient'] = (dataset['Gradient'].values) / devide_num
        return dataset

    def customize_dataset(self, dataset):
        origin = dataset.pop('Adj Close')
        return dataset
    
    def devide_dataset(self, dataset):# TODO:
        return dataset

    def check_predictor(self):
        predictor = Predictor()
        dataframe = predictor.get_dataset()
        dataframe = self.norm(dataframe)
        dataframe = self.customize_dataset(dataframe)
        print(dataframe.head)

if __name__ == '__main__':
    print(tf.__version__)
    g_predictor = Predictor()
    dataframe = g_predictor.get_dataset()
    print(dataframe.head)
