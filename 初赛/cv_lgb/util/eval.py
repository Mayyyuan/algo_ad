## 这个文件是 定义的评估函数和目标函数

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



def SMAPE(Ft, At):
	'''
	Ft : 为预估的广告曝光值
	At ： 为真是的曝光值
	return ： SMAPE 值，该值越小越好
	'''
	sum_by_2 = (Ft + At) * 0.5
	sub = np.abs(Ft - At)
	_SMAPE = np.mean(sub / sum_by_2)
	return _SMAPE


def score(bid_true, y_true, bid_n_test, y_n_test):
	'''
	这个函数主要是用来求单挑性分数的
	bid_true ： 原来的 bid, 对应一个数
	y_true : 原来的标签值，一个数
	bid_n_test ： 变化的 bid_n_test, 这个是一个list
	y_n_test ： 同理，这个是对应的 bid 变化后得到的预测值

	return : 返回单调得分，这个得分越高越好
	'''

	bid_n_sub = bid_n_test - bid_true
	y_n_sub = y_n_test - bid_true

	bid_n_sub = bid_n_sub >= 0
	y_n_sub = y_n_sub >= 0

	_score = np.mean(bid_n_sub == y_n_sub)
	return _score





