##  这个主要是用个点搜索来调试最佳参数的

import pandas as pd
from sklearn.grid_search import GridSearchCV
import lightgbm as lgb 

train_path = '/home/xiaoyang/competetion/data/train_data_simple.dat'
train_data = pd.read_csv(train_path, sep='\t')
# test_path = '/home/xiaoyang/competetion/data/test_data_simple.dat'
# test_data = pd.read_csv(test_path, sep='\t')

y_train = train_data['exposure_mean']
X_train = train_data.drop(['exposure_mean'], axis=1)
X_train['AIid'] = X_train['AIid'].map(lambda x: int(x.split(",")[0]))


category_columns = ["Aid", "AAid", "AIid", "Size"]
X_train[category_columns].astype('category')


parmas_search = {
				'max_depth': list(range(3, 8, 1)), 
				'num_leaves': list(range(10, 800, 10)), 
				'learning_rate': [0.1, 0.05, 0.01, 0.005]
				# 'reg_alpha': [0.1, 0.3, 0.5, 1],
				# 'reg_lambda': [0.1, 0.3, 0.5, 1]
				}


gsearch = GridSearchCV(estimator=lgb.LGBMRegressor(
	boosting_type='gbdt', objective='regression', 
	n_estimators=1000, bagging_fraction=0.8,feature_fraction=0.8), 
	param_grid=parmas_search, cv=5)


gsearch.fit(X_train, y_train)
print('gsearch.grid_scores_ : ', gsearch.grid_scores_)
print('gsearch.best_params_ : ', gsearch.best_params_)
print('gsearch.best_score_ : ', gsearch.best_score_)







