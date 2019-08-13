
# https://www.tensorflow.org/tutorials/keras/basic_regression?hl=ko

'''
회귀(regression)는 가격이나 확률 같이 연속된 출력 값을 예측하는 것이 목적입니다. 
이와는 달리 분류(classification)는 여러개의 클래스 중 하나의 클래스를 선택하는 것이 목적입니다
(예를 들어, 사진에 사과 또는 오렌지가 포함되어 있을 때 어떤 과일인지 인식하는 것).
이 노트북은 Auto MPG 데이터셋을 사용하여 1970년대 후반과 1980년대 초반의 자동차 연비를 예측하는 모델을 만듭니다. 
이 기간에 출시된 자동차 정보를 모델에 제공하겠습니다. 이 정보에는 실린더 수, 배기량, 마력(horsepower), 공차 중량 같은 속성이 포함됩니다.
이 예제는 tf.keras API를 사용합니다. 자세한 내용은 케라스 가이드를 참고하세요.
seaborn 패키지가 설치되어있지 않다면 설치 필요(산점도 행렬을 그리는데 사용)
'''

from __future__ import absolute_import, division, print_function, unicode_literals, unicode_literals

import pathlib

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

print(tf.__version__)

def get_dataset():
    dataset_path = keras.utils.get_file("auto-mpg.data", "http://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data")
    print("dataset_path: {}".format(dataset_path))
    # 판다스를 사용하여 데이터를 읽습니다.
    column_names = ['MPG','Cylinders','Displacement','Horsepower','Weight',
                    'Acceleration', 'Model Year', 'Origin']
    raw_dataset = pd.read_csv(dataset_path, names=column_names,
                        na_values = "?", comment='\t',
                        sep=" ", skipinitialspace=True)
    dataset = raw_dataset.copy()
    print('dataset : {}'.format(dataset.tail()))
    return dataset

# 데이터 정제하기
def customize_dataset(dataset):
    # 이 데이터셋은 일부 데이터가 누락되어 있습니다.
    print(dataset.isna().sum())
    # 문제를 간단하게 만들기 위해서 누락된 행을 삭제하겠습니다.
    dataset = dataset.dropna()
    # "Origin" 열은 수치형이 아니고 범주형이므로 원-핫 인코딩(one-hot encoding)으로 변환하겠습니다:
    origin = dataset.pop('Origin')

    dataset['USA'] = (origin == 1)*1.0
    dataset['Europe'] = (origin == 2)*1.0
    dataset['Japan'] = (origin == 3)*1.0
    return dataset

# 훈련, 테스트 세트로 분할
def devide_dataset(dataset):
    # 데이터셋을 훈련 세트와 테스트 세트로 분할하기
    # 이제 데이터를 훈련 세트와 테스트 세트로 분할합니다.
    # 테스트 세트는 모델을 최종적으로 평가할 때 사용합니다.
    train_dataset = dataset.sample(frac=0.8,random_state=0)
    test_dataset = dataset.drop(train_dataset.index)
    return train_dataset, test_dataset

# 데이터 조사하기
def get_data_stats(dataset):
    # 훈련 세트에서 몇 개의 열을 선택해 산점도 행렬을 만들어 살펴 보겠습니다.
    sns.pairplot(dataset[["MPG", "Cylinders", "Displacement", "Weight"]], diag_kind="kde")
    data_stats = dataset.describe()
    data_stats.pop("MPG")
    data_stats = data_stats.transpose()
    # print('data stats: {}'.format(data_stats))
    return data_stats

# 특성과 레이블 분리하기
def get_labels(dataset):
    # 특성에서 타깃 값 또는 "레이블"을 분리합니다. 이 레이블을 예측하기 위해 모델을 훈련시킬 것입니다.
    return dataset.pop('MPG')

# 정규화, 수치를 스케일링
def norm(dataset, stats):
    return (dataset - stats['mean']) / stats['std']

def build_model():
    model = keras.Sequential([
        layers.Dense(64, activation=tf.nn.relu, input_shape=[9]),
        layers.Dense(64, activation=tf.nn.relu),
        layers.Dense(1)
    ])

    model.compile(loss='mean_squared_error',
        optimizer=tf.keras.optimizers.RMSprop(0.001),
        metrics=['mean_absolute_error', 'mean_squared_error']
    )

    return model

dataset = get_dataset()
dataset = customize_dataset(dataset)
print("dataset: {}".format(dataset.tail()))

(train_dataset, test_dataset) = devide_dataset(dataset)
# print("train dataset: {}".format(train_dataset))
# print("test  dataset: {}".format(test_dataset))

train_stats = get_data_stats(train_dataset)
test_stats = get_data_stats(test_dataset)

# 특성에서 타깃 값 또는 "레이블"을 분리합니다. 이 레이블을 예측하기 위해 모델을 훈련시킬 것입니다.
train_labels = get_labels(train_dataset)
test_labels = get_labels(test_dataset)

normed_train_data = norm(train_dataset, train_stats)
normed_test_data = norm(test_dataset, test_stats)
print('normalized train data: {}'.format(normed_train_data))
print('normalized test data : {}'.format(normed_test_data))

model = build_model()
model.summary()