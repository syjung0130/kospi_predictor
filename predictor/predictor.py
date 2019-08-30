from __future__ import absolute_import, division, print_function, unicode_literals, unicode_literals

import pathlib

import matplotlib.pyplot as plt
import pandas as pd
import copy
import seaborn as sns

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

    def check_predictor():
        predictor = Predictor()
        dataframe = predictor.get_dataset()
        print(dataframe.head)

if __name__ == '__main__':
    print(tf.__version__)
    g_predictor = Predictor()
    dataframe = g_predictor.get_dataset()
    print(dataframe.head)
