import lightgbm as lgb
from config import *
from sklearn.model_selection import train_test_split, KFold
import os

class CVModel:
	def __init__(self, X=None, y=None):		
		self.best_model_list = []
		self.best_round_list = []
		self.best_auc_list = []

		self.config = Config()
		self.X = X
		self.y = y
		pass

	def kf_train(self, save_model=True):
		num_boost_round = self.config.max_round
		cv_folds = self.config.cv_folds
		early_stop_round = self.config.early_stop_round
		seed = self.config.seed
		save_model_directory = self.config.save_model_directory
		params = self.config.params
		feature_importance_directory = self.config.feature_importance_directory
		n_splits = self.config.n_splits

		kf = KFold(n_splits=n_splits, shuffle=False)
		for train_index, test_index in kf.split(self.X):
			## pandas dataframe 读取数据
			X_train = self.X.loc[train_index]
			y_train = self.y.loc[train_index]
			X_test = self.X.loc[test_index]
			y_test = self.y.loc[test_index]

			lgb_train = lgb.Dataset(X_train, y_train)
			lgb_test = lgb.Dataset(X_test, y_test, reference=lgb_train)

			## 开始训练
			watchlist = [lgb_train, lgb_test]
			best_model = lgb.train(params, lgb_train, num_boost_round=num_boost_round, valid_sets=watchlist, early_stopping_rounds=early_stop_round)
			best_round = best_model.best_iteration
			best_auc = best_model.best_score

			self.best_model_list.append(best_model)
			self.best_round_list.append(best_round)
			self.best_auc_list.append(best_auc)

			## 保存模型， 保存特征的重要性
			if save_model:
				self.save_models(save_model_directory)

			plot = False if feature_importance_directory is None else True
			self.deal_with_feature_importance(plot, feature_importance_directory)


	def save_models(self, directory):
		'''
		保存到文件夹， 文件名格式为 model_index.txt
		'''
		# 这里用的是相对路径, 获得当前的工作路径
		if not os.path.exists(directory):
			raise IOError(directory + ' is not exists')

		print('saving models in ', directory, ' ......................')
 
		filename = 'model_{}.txt'
		for index in range(0, len(self.best_model_list)):
			abs_path = os.path.join(directory, filename.format(index))
			self.best_model_list[index].save_model(abs_path)

		print('completed saving models in ', directory, ' ..............')
		pass

	def load_models(self, directory):
		if not os.path.exists(directory):
			raise IOError(directory + ' is not exists')

		print('loading models from ', directory, '  ...................')
		# 这里只是简单地把一个文件夹下所有的model文件都读取进来，日后可能会有改动
		for files in os.listdir(directory):
			model_file_path = os.path.join(directory, files)
			if os.path.isfile(model_file_path):				
				best_model = lgb.Booster(model_file=model_file_path)
				self.best_model.append(best_model)
				self.best_round_list.append(best_model.best_iteration)

		print('completed loading models from ', directory, '  ..........')


	def deal_with_feature_importance(self, plot=False, feature_importance_directory=None):
		'''
		这个也是保存到文件夹， 
		'''
		print('saving feature_importance in ', feature_importance_directory, ' ......................')

		if plot:
			import matplotlib
			matplotlib.use('Agg')
			import matplotlib.pyplot as plt

			# 这里用的是相对路径, 获得当前的工作路径
			if not os.path.exists(feature_importance_directory):
				raise IOError(feature_importance_directory + ' is not exists')

			filename = 'model_{}_feature_importance.jpg'
		for index in range(0, len(self.best_model_list)):
			print('computing feature_importance of : model ' , index)
			print('Feature importances:', list(self.best_model_list[index].feature_importance()))
			print('Feature importances gains:', list(self.best_model_list[index].feature_importance("gain")))
			if plot:
				abs_path = os.path.join(feature_importance_directory, filename.format(index))
				lgb.plot_importance(self.best_model_list[index], max_num_features=1000)
				plt.savefig(abs_path)

		## 是否还需要打印树的结构， 有需求再加
		
		pass

	def predict(self, X_test):
		if len(self.best_model_list) == 0:
			raise Exception('the best_model_list is empty !!!') 

		score = 0.

		for index in range(0, len(self.best_model_list)):
			score += self.best_model_list[index].predict(X_test, num_iteration=self.best_round_list[index])

		score_avg = score / len(self.best_model_list)
		pass

