import numpy as ny
import pandas as pd
from sklearn.model_selection import train_test_split

def create_data(X, y):
	X_train = None
	y_train = None
	X_test = None
	y_test = None

	# load and deal with your data
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=100)

	return X_train, y_train, X_test, y_test


# self-defined objective function
# preds: 预测值， train_data 是一整条数据， 因为沿用xgboost的一阶二阶导数，是loss对当然preds的导数。
def self_defined_objective(preds, train_data):
	grad = 0
	hess = 0

	return grad, hess	

# slef-defined evaluation
# 自定义评估函数
# f(preds: array, train_data: Dataset) -> name: string, eval_result: float, is_higher_better: bool
def self_defined_eval(preds, train_data):
	name = "name"
	eval_result = 0.
	return name, eval_result, True


## 自定义的各种工具函数，比如 时间戳转换等




