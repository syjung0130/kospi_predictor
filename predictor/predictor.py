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

    # 0~1 사이로 스케일링, min_max 정규화를 사용.. 확률 분포와 관련된 data가 아니므로 표준편차보다는 min_max정규화가 적절
    def normalize(self, coloumn_name):
        rows = self.dataframe[coloumn_name].values
        max = np.max(rows)
        min = np.min(rows)
        divide_num = max - min
        rows = (rows - min) / divide_num
        self.dataframe[coloumn_name] = pd.Series(rows)

    def customize_dataframe(self):
        self.normalize('Gradient')
        self.normalize('Open')
        self.normalize('Close')
        self.normalize('Volume')

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
        return copy.deepcopy((self.train_dataset, self.test_dataset))
    
    def get_gradient_labels(self):
        return copy.deepcopy(self.customizer.get_gradient_labels())
    
    def get_pricestatus_labels(self):
        return copy.deepcopy(self.customizer.get_pricestatus_labels())

    def build_model(self):
        '''
        [reference]
        tf.keras.layers.Dense   : https://www.tensorflow.org/api_docs/python/tf/keras/layers/Dense
        model.compile, metrics  : https://keras.io/models/sequential/
        tf keras optimizer      : https://www.tensorflow.org/api_docs/python/tf/keras/optimizers
        keras optimizer         : https://keras.io/optimizers/
        tensorflow              : https://www.tensorflow.org/api_docs/python/tf/train/Optimizer
        '''
        model = keras.Sequential([
            layers.Dense(64, activation=tf.nn.relu, input_shape=[3]),
            layers.Dense(64, activation=tf.nn.relu),
            layers.Dense(1)
        ])

        model.compile(
            loss='mean_squared_error',
            optimizer=tf.keras.optimizers.RMSprop(0.001),
            metrics=['mean_absolute_error', 'mean_squared_error']
        )

        return model

    def check_predictor(self):
        (train_data, test_data) = self.load_data()
        gradient_labels = self.get_gradient_labels()
        price_labels = self.get_pricestatus_labels()
        model = self.build_model()
        model.summary()

        row_length = gradient_labels.shape[0]
        train_dataset_length = int(row_length * 0.8)
        np_train_gradient_labels = gradient_labels[:train_dataset_length]

        EPOCHS = 1000
        history = model.fit(
            train_data,
            np_train_gradient_labels,
            epochs=EPOCHS,
            validation_split=0.2,
            verbose=0,
            callbacks=[PrintDot()]
        )

# 에포크가 끝날 때마다 점(.)을 출력해 훈련 진행 과정을 표시합니다
class PrintDot(keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs):
    if epoch % 100 == 0: print('')
    print('.', end='')

if __name__ == '__main__':
    print(tf.__version__)
