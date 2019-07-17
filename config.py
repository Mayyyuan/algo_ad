class Config(object):
	"""docstring for Config"""
	def __init__(self):
		self.params = {
			'objective': 'regression',   ## 目标函数， 枚举类型，默认是regression
			'boosting': 'gbdt',		     ## 默认是gbdt
			# 'num_iterations': 100,     ## 默认是100, 对于多分类，内部会构造num_class * num_iterations科树
			'metric': {'l2', 'l1'},      ## 测量标准
			'num_leaves': 31,            ## 叶子数，必须大于1， 太大容易过拟合
			'learning_rate': 0.05,       ## 学习率也可以是一个lambda
			'feature_fraction': 0.9,     ## 默认是1， 每次迭代会随机选择的特征比例。
			'bagging_fraction': 0.8,     ## 默认是1， 会随机选择部分数据
			'bagging_freq': 5,     		 ## 没多少次迭代重新bagging数据， 0代表不bagging
			'lambda_l1': 0,
			'lambda_l2': 5,
			'verbose': 0,                ##  < 0: Fatal, = 0: Error (Warning), = 1: Info, > 1: Debug
			'device': 'cpu',
			# 'gpu_device_id': 1,
			'num_thread': 6              ## 最好等于服务器的核数
		}


		#########  IO   参数 #######
		self.max_bin = 255
		self.min_data_in_bin = 3
		self.early_stop_round = 50
		self.max_round = 3000
		self.cv_folds = None
		self.seed = 3
		self.n_splits = 5
		self.save_model_path = "model/model.txt"
		self.feature_importance_path = "model/feature_importance.jpg"


