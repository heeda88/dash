#%%

import pandas as pd
from sklearn.model_selection import train_test_split
from torch import feature_alpha_dropout

import tensorflow as tf
from tensorflow.keras import models
from tensorflow.keras import layers
import tensorflow.keras as keras
from tensorflow import keras 
from tensorflow.keras.utils import to_categorical
URL = '../../data/train.csv'
df = pd.read_csv(URL)
ml_df= pd.get_dummies(df)

## 데이터정제
columns_list=ml_df.columns.tolist()
columns_list

print(columns_list)

feature_list=[ 'Overall Qual', 'Gr Liv Area', 'Garage Cars', 'Garage Area', 'Total Bsmt SF', '1st Flr SF',
'Full Bath', 'Year Built', 'Year Remod/Add', 'Garage Yr Blt', 'Exter Qual_Ex', 'Exter Qual_Fa', 
'Exter Qual_Gd', 'Exter Qual_TA', 'Kitchen Qual_Ex', 'Kitchen Qual_Fa', 'Kitchen Qual_Gd',
'Kitchen Qual_TA', 'Bsmt Qual_Ex', 'Bsmt Qual_Fa', 'Bsmt Qual_Gd', 'Bsmt Qual_Po', 'Bsmt Qual_TA']
#%%
X=ml_df[feature_list]
y=ml_df['target']

x_train, x_test, train_labels, test_labels = train_test_split(X, y , test_size=0.1)

x_train=pd.get_dummies(x_train)
x_test=pd.get_dummies(x_test)

# #%%
# from sklearn.preprocessing import OneHotEncoder

# ohe = OneHotEncoder(sparse=False)
# for index in feature_list:
#   c_type=str(type(x_train[index].tolist()[0]))
#   if 'str' in c_type:
#     print(index, c_type)
#     one_hot_list= x_train[index].unique().tolist()
#     ohe_result = ohe.fit_transform(x_train[[index]])
#     x_train.loc[:,index]=pd.Series(ohe_result.tolist())



#%%

import numpy as np
# 순수 인덱싱
def vectorize_sequences(sequences, dimension):
    results = np.zeros((len(sequences), dimension))
    for i, sequence in enumerate(sequences):
      for j, seq in enumerate(sequence):
        results[i, j] = seq
    return results



# 훈련 데이터 벡터 변환
x_vector_train = vectorize_sequences(x_train.to_numpy().astype('int'), dimension=len(x_train.columns))
# 테스트 데이터 벡터 변환
x_vector_test = vectorize_sequences(x_test.to_numpy().astype('int'), dimension=len(x_test.columns))

#%%
len(x_train.columns)
#%%
x_vector_train.shape
#%%
# one_hot_train_labels = to_categorical(train_labels.to_numpy().astype('int'))
# one_hot_test_labels = to_categorical(test_labels.to_numpy().astype('int'))
one_hot_train_labels = train_labels.to_numpy().astype('int')
one_hot_test_labels = test_labels.to_numpy().astype('int')


#%%
from tensorflow.python.client import device_lib
device_lib.list_local_devices()
#%%
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  # 텐서플로가 첫 번째 GPU에 1GB 메모리만 할당하도록 제한
  try:
    tf.config.experimental.set_virtual_device_configuration(
        gpus[0],
        [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024)])
  except RuntimeError as e:
    # 프로그램 시작시에 가상 장치가 설정되어야만 합니다
    print(e)

#%%
strategy = tf.distribute.MirroredStrategy()
with strategy.scope():
  model = models.Sequential()
  model.add(layers.Dense(512, activation='relu', input_shape=(23,)))
  model.add(layers.Dense(512, activation='relu'))
  model.add(layers.Dense(64, activation='relu'))
  model.add(layers.Dense(1))
  model.compile(optimizer='rmsprop', loss='mse', metrics=['mae','mse'])
  # model.add(layers.Dense(101, activation='softmax'))
  # model.compile(optimizer='adagrad',
  #               loss='categorical_crossentropy',
  #               metrics=keras.metrics.CategoricalCrossentropy())


#%%
val_num=int(len(x_vector_train)/10)
print(val_num)
#%%
x_val = x_vector_train[:val_num]
partial_x_train = x_vector_train[val_num:]

y_val = one_hot_train_labels[:val_num]
partial_y_train = one_hot_train_labels[val_num:]


#%%
history = model.fit(partial_x_train,
                    partial_y_train,
                    epochs=2000,
                    batch_size=512,
                    validation_data=(x_val, y_val))

#%%
x_vector_test

#%%
predictions = model.predict(x_vector_test)


#%%
predictions[:5]


#%%
test_labels[:5]
#%%
model.summary()