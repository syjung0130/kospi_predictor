
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

def plot_history(history):
    hist = pd.DataFrame(history.history)
    hist['epoch'] = history.epoch

    plt.figure(figsize=(8,12))

    plt.subplot(2,1,1)
    plt.xlabel('Epoch')
    plt.ylabel('Mean Abs Error [MPG]')
    plt.plot(hist['epoch'], hist['mean_absolute_error'],
            label='Train Error')
    plt.plot(hist['epoch'], hist['val_mean_absolute_error'],
            label = 'Val Error')
    plt.ylim([0,5])
    plt.legend()

    plt.subplot(2,1,2)
    plt.xlabel('Epoch')
    plt.ylabel('Mean Square Error [$MPG^2$]')
    plt.plot(hist['epoch'], hist['mean_squared_error'],
            label='Train Error')
    plt.plot(hist['epoch'], hist['val_mean_squared_error'],
            label = 'Val Error')
    plt.ylim([0,20])
    plt.legend()
    plt.show()

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

'''
모델 훈련
이 모델을 1000번 정도 훈련시켜 보자.
훈련 정확도와 검증 정확도는 history 객체에 저장된다.
'''

# 에포크가 끝날 때마다 점(.)을 출력해 훈련 진행 과정을 표시합니다
class PrintDot(keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs):
    if epoch % 100 == 0: print('')
    print('.', end='')

EPOCHS = 1000

# keras.callbacks.Callback클래스를 상속한 클래스 객체를 
# fit()함수의 전달인자로 넘겨주면 매 에포크마다 사용자가 정의한 콜백을 수행할 수 있다.
# 리스트로 전달하는 걸로 봐서, 콜백을 여러개 전달할 수 있는 것으로 보인다.
history = model.fit(
    normed_train_data,
    train_labels,
    epochs=EPOCHS,
    validation_split=0.2,
    verbose=0,
    callbacks=[PrintDot()]
)

# model.fit()을 하면 history객체가 반환되는데
# 이 객체에는 모델의 훈련 과정이 저장되어 있고
# pandas를 통해 시각화할 수 있다.
pd_history = pd.DataFrame(history.history)
pd_history['epoch'] = history.epoch
print("===== history =====")
print(pd_history.tail)

plot_history(history)

'''
에러값이 크가 줄어들다가 0~200 사이의 값에서는 더이상 줄어들지 않고 있다.
이 지점부터 모델이 거의 향상되지 않고 있다.
model.fit 메서드를 수정하여 검증 점수가 향상되지 않으면 자동으로 훈련을 멈추도록 만들어 보죠. 
에포크마다 훈련 상태를 점검하기 위해 EarlyStopping 콜백(callback)을 사용하겠습니다. 
지정된 에포크 횟수 동안 성능 향상이 없으면 자동으로 훈련이 멈춥니다.
'''

model = build_model()

# patience 매개변수는 성능 향상을 체크할 에포크 횟수입니다
early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)

history = model.fit(normed_train_data, train_labels, epochs=EPOCHS,
                    validation_split = 0.2, verbose=0, callbacks=[early_stop, PrintDot()])

plot_history(history)

# 이 그래프를 보면 검증 세트의 평균 오차가 약 +/- 2 MPG입니다. 좋은 결과인가요? 이에 대한 평가는 여러분에게 맡기겠습니다.
# 모델을 훈련할 때 사용하지 않았던 테스트 세트에서 모델의 성능을 확인해 보죠. 이를 통해 모델이 실전에 투입되었을 때 모델의 성능을 짐작할 수 있습니다:
loss, mae, mse = model.evaluate(normed_test_data, test_labels, verbose=0)
print("테스트 세트의 평균 절대 오차: {:5.2f} MPG".format(mae))

# 예측
# 테스트 세트의 샘플을 사용해서 MPG 값을 예측해보자
test_predictions = model.predict(normed_test_data).flatten()

plt.scatter(test_labels, test_predictions)
plt.xlabel('True Values [MPG]')
plt.ylabel('Predictions [MPG]')
plt.axis('equal')
plt.axis('square')
plt.xlim([0, plt.xlim()[1]])
plt.ylim([0, plt.ylim()[1]])
_ = plt.plot([-100, 100], [-100, 100])
plt.show()

error = test_predictions - test_labels
plt.hist(error, bins = 25)
plt.xlabel("Prediction Error [MPG]")
_ = plt.ylabel("Count")
plt.show()