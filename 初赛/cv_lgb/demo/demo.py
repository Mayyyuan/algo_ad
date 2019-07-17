import pandas as pd
import lightgbm as lgb
from sklearn.metrics import mean_squared_error
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from Model import Model
from config import *

# iris = load_iris()
# data = iris.data
# target = iris.target

# X_train, X_test, y_train, y_test = train_test_split(data, target, test_size = 0.2)

df_train = pd.read_csv('/home/xiaoyang/ml/lgb/lgb_example/regression/regression.train', header=None, sep='\t')
df_test = pd.read_csv('/home/xiaoyang/ml/lgb/lgb_example/regression/regression.test', header=None, sep='\t')


y_train = df_train[0]
y_test = df_test[0]
X_train = df_train.drop(0, axis=1)
X_test = df_test.drop(0, axis=1)


gbm = Model(X_train, y_train, X_test, y_test)
best_model, best_auc, best_round, cv_result = gbm.train()

print("##############################")
print('best auc: ', best_auc)
print('best_round: ', best_round)
print('cv_result: ', cv_result)

gbm.save_model(Config().save_model_path)
	
###  读取模型， 
gbm = Model(X_train, X_test, y_train, y_test)
gbm.load_model(Config().save_model_path)

gbm.predict(X_test)
