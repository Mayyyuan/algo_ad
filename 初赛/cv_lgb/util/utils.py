import numpy as ny
import pandas as pd
import time
from sklearn.model_selection import train_test_split

def create_data(X, y):
	X_train = None
	y_train = None
	X_test = None
	y_test = None

	# load and deal with your data
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=100)

	return X_train, y_train, X_test, y_test


def time_format(timestamp, format=None):
	'''
	timestamp : 传入时间戳
	format : "%Y-%m-%d"  , "%Y-%m-%d %H:%M:%S",  "%H:%M:%S"
	'''
	if format is None:
		format = "%Y-%m-%d %H:%M:%S"

	time_local = time.localtime(timestamp)
	dt = time.strftime(format, time_local)
	return dt


## 自定义的各种工具函数，比如 时间戳转换等




