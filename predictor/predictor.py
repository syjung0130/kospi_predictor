from __future__ import absolute_import, division, print_function, unicode_literals, unicode_literals

import pathlib

import matplotlib.pyplot as plt
import pandas as pd
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
        # TODO: 종목코드 관리, DB인스턴스 관리하는 싱글톤 클래스 구현 필요
        pd = dbManager.get_pd_db()
        print(pd.head)

if __name__ == '__main__':
    print(tf.__version__)
    g_predictor = Predictor()
    g_predictor.get_dataset()
