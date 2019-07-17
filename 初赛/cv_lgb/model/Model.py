import lightgbm as lgb
from config import *
class Model:
	def __init__(self, X_train=None, y_train=None, X_test=None, y_test=None):		
		self.gbm = None
		self.config = Config()

		if (X_train is not None) and (y_train is not None):
			self.load_X_train(X_train, y_train)
		if (X_test is not None) and (y_test is not None):
			self.load_X_test(X_test, y_test)
		pass


	def load_X_train(self, X_train, y_train):
		self.lgb_train = lgb.Dataset(X_train, y_train)
		pass


	def load_X_test(self, X_test, y_test):
		assert self.lgb_train is not None, "train data should be loaded before, because there is a reference to it"
		self.lgb_test = lgb.Dataset(X_test, y_test, reference=self.lgb_train)
		pass

	def train(self):
		num_boost_round = self.config.max_round
		cv_folds = self.config.cv_folds
		early_stop_round = self.config.early_stop_round
		seed = self.config.seed
		save_model_path = self.config.save_model_path
		params = self.config.params
		feature_importance_path = self.config.feature_importance_path

		## 模型一开始默认是auc
		if cv_folds is not None:
			## 如果提供日志框架， 就在这打印日志信息
			cv_result = lgb.cv(params, self.lgb_train, num_boost_round=num_boost_round, nfold=cv_folds, seed=seed, 
				stratified=False, verbose_eval=True, metrics='auc', early_stopping_rounds=early_stop_round, show_stdv=False)
			# 最优模型， 最优迭代模型
			best_round = len(cv_result['auc-mean'])
			best_auc = cv_result['auc-mean'][-1]  #最好的auc值
			best_model = lgb.train(params, self.lgb_train, best_round)	

		else:
			watchlist = [self.lgb_train, self.lgb_test]
			best_model = lgb.train(params, self.lgb_train, num_boost_round=num_boost_round, valid_sets=watchlist, early_stopping_rounds=early_stop_round)
			best_round = best_model.best_iteration
			best_auc = best_model.best_score
			cv_result = None

		## 保存模型
		self.gbm = best_model
		## 处理特征重要性
		plot = False if feature_importance_path is None else True
		self.deal_with_feature_importance(plot, feature_importance_path)

		return best_model, best_auc, best_round, cv_result

	def save_model(self, filepath):
		'''
		save the model into a txt format file:
			filepath:  should be a valid path
		'''
		assert self.gbm is not None, "There isn't a model before training or loading a model"
		self.gbm.save_model(filepath)
		pass

	def load_model(self, filepath):
		'''
		load the model from a specific file
		'''
		self.gbm = lgb.Booster(model_file=filepath)
		pass

	def deal_with_feature_importance(self, plot=False, feature_importance_path=None):
		## 输出特征的重要程度
		## 计算特征的重要性
		print('Calculate feature importances...')
		# feature importances
		print('Feature importances:', list(self.gbm.feature_importance()))
		print('Feature importances gains:', list(self.gbm.feature_importance("gain")))

		if plot:
			import matplotlib
			matplotlib.use('Agg')
			import matplotlib.pyplot as plt

			lgb.plot_importance(self.gbm, max_num_features=1000)
			plt.savefig(feature_importance_path)

		## 是否还需要打印树的结构， 有需求再加
		pass

	def predict(self, Xtest):
		'''
		use the model to predict your test data, before this, you should train a data, or load a trained data 
		'''
		## 是否要选择模型
		y_pred = self.gbm.predict(Xtest)

		### to do 根据对应的评估标准写 ，现在还没办法定义
		pass
