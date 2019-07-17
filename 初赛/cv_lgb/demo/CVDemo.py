import pandas as pd
import lightgbm as lgb
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from CVModel import CVModel
from config import *

df_train = pd.read_csv('/home/xiaoyang/ml/lgb/lgb_example/regression/regression.train', header=None, sep='\t')
df_test = pd.read_csv('/home/xiaoyang/ml/lgb/lgb_example/regression/regression.test', header=None, sep='\t')

y_train = df_train[0]
y_test = df_test[0]
X_train = df_train.drop(0, axis=1)
X_test = df_test.drop(0, axis=1)


cv_model = CVModel(X_train, y_train)
cv_model.kf_train()

cv_model.predict(X_test)
