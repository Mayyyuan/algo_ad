import numpy as np
import pandas as pd
# import keras.utils as ku
import time 
import datetime
import os
	

def split_by_days(file, timestamp_index, sep='\t', header=None, feature_name='date', save_directory='./'):
	'''
	这个函数主要用来将数据根据时间戳划分成每一天的数据集
	默认情况下，是划分为一天一天的。

	file : 数据文件
	timestamp_index : 时间戳所在的列索引
	feature_name : 函数会根据时间戳新生成特征，特征为年月日等，这个是用户自定义的特征名，
	save_directory ： 数据划分后，保存的文件夹路径
	'''
	if not os.path.exists(save_directory):
		raise IOError(save_directory + ' is not exists')

	data = pd.read_csv(file, sep=sep, header=header)
	
	format = "%Y-%m-%d"
	data[feature_name] = [time.strftime(format, time.localtime(x)) for x in data[timestamp_index]]

	date_set = set(data[feature_name])
	for date in date_set:
		# 得到这一天的数据
		data_in_date = data[data[feature_name] == date]
		# 保存划分数据结果
		filename = os.path.join(save_directory, str(date)+'.csv')
		data_in_date.to_csv(filename, sep='\t', index=0)

	print('######    split into file by dates is completed   ########')

def get_CRC_data(save_file):
	'''
	这个就是为了从 log 中得到与 test_sample 测试数据 类型一致的CPC数据， 
	这时，需要从操作日志中获得ad_id， 因为 CPC 类型的数据一定会得到与训练数据所有的特征
	'''
	total_Exposure_log_path = '/home/xiaoyang/competetion/data/totalExposureLog.out'
	ad_operation_path = '/home/xiaoyang/competetion/data/ad_operation.dat'

	totalExposureLog = pd.read_csv(total_Exposure_log_path, header=None, sep='\t')
	ad_operation = pd.read_csv(ad_operation_path, header=None, sep='\t')
	ad_id = set(ad_operation[0])

	filtered_log = totalExposureLog[totalExposureLog[4].isin(ad_id)]
	## 保存数据
	filtered_log.to_csv(save_file, sep='\t', index=0)

def deal_with_test_sample(save_file):
	'''
	这个函数只是为了 处理 test_sample.dat, 根据创建的时间，得到具体的投放时间。
	'''
	test_sample_path = '/home/xiaoyang/competetion/data/test_sample.dat'
	ad_operation_path = '/home/xiaoyang/competetion/data/ad_operation.dat'
	ad_operation = pd.read_csv(ad_operation_path, header=None, sep='\t')
	test_sample = pd.read_csv(test_sample_path, header=None, sep='\t')

	format = "%Y-%m-%d"
	test_sample['create_date'] = [time.strftime(format, time.localtime(x)) for x in test_sample[2]]

	change = lambda x: datetime.datetime.strptime(x, format)
	compare_date = change('2019-03-20')
	after_one_day = lambda x: datetime.datetime.strptime(x, format)+datetime.timedelta(days=1)

	test_sample['pre_date'] = [compare_date if change(x) < compare_date else after_one_day(x) for x in test_sample['create_date']]
	test_sample['pre_weekday'] = [x.weekday() for x in test_sample['pre_date']]
	test_sample['deliver_time'] = [ x.split(',')[y]  for x, y in zip(test_sample[8], test_sample['pre_weekday'])]
	# 保存有header，
	test_sample.to_csv(save_file, index=0, sep='\t')


def deal_with_train_data_on_time(save_file):
	'''
	这个函数主要是用来 根据操作记录ad_operation，来获取对应的投放时段信息，规则如下：
	1. 如果只创建不修改，那么直接使用创建的时段信息
	2. 如果进行了修改，那么，比较修改的时间和逆序后请求时间，
	   只要请求时间大于某个修改时间，这次的修改就是对应的最终修改。
	'''
	log_names = ["ReqId", "ReqTime", "ALid", "UserId", "Aid", "Size", "Bid", "Pctr", "Ecpm", "TEcpm"]
	## Create Or Modify Time=COMTime, OpType=Operation Time, ModField, ValAfterOp= Value After Operation
	ad_operation_names = ["Aid", "COMTime", "OpType", "ModField", "ValAfterOp"]

	train_data_path = '/home/xiaoyang/competetion/data/ad_CPC_in_log.dat'
	ad_operation_path = '/home/xiaoyang/competetion/data/ad_operation.dat'
	ad_operation = pd.read_csv(ad_operation_path, header=None, sep='\t', names=ad_operation_names)
	train_data = pd.read_csv(train_data_path, sep='\t')
	train_data.columns = log_names

	# 处理请求时间
	format = "%Y-%m-%d"
	train_data['query_date'] = [time.strftime(format, time.localtime(x)) for x in train_data['ReqTime']]
	ad_operation = ad_operation[ad_operation['ModField'] == 4]

	# merge_table = pd.merge(train_data, ad_operation)
	# 因为需要排序，所有还不能这样做，merge之后
	
	count = 0
	length = train_data.shape[0]
	print('CRC length = ', length, '    ..........')
	deliver_time = [0] * length
	for index, row in train_data.iterrows():
		# 表连接
		temp = ad_operation[ad_operation['Aid'] == row['Aid']]
		# 根据修改/操作事件排序
		temp = temp.sort_values(by='COMTime', axis=0, ascending=False)
		# 根据请求时间，获得对应的日期的 weekday ， 然后选出投放时段
		weekday = datetime.datetime.strptime(row['query_date'], format).weekday()

		for i, t_row in temp.iterrows():
			if t_row['COMTime'] == 0:
				deliver_time[index]= int(t_row['ValAfterOp'].split(',')[weekday])
				break

			t = datetime.datetime.strptime(str(t_row['COMTime']), '%Y%m%d%H%M%S')
			# 如果请求时间大于 t,因为是逆序，所以说明这一定是最终的 
			if row['ReqTime'] > int(t.timestamp()):
				deliver_time[index] = int(t_row['ValAfterOp'].split(',')[weekday])
				break
		count += 1
		if count % 1000 == 0:
			print('finish {} datas ....'.format(count))

	train_data['deliver_time'] = deliver_time
	print('train data extract deliver_time over   ..................')
	print('saving data into ', save_file , '  .................')
	train_data.to_csv(save_file, index=0, sep='\t')


def join_log_user():
	'''
	这个函数是用来将每天的 log 和 user_data 的信息进行 join 关联，方便统计每一行的特征值
	'''
	log_names=["ReqId", "ReqTime", "ALid", "UserId", "Aid", "Size", "Bid", "Pctr", "Ecpm", "TEcpm", "Date"]
	user_names=["UserId", "Age", "Gender", "Area", "Status", "Education", "Cons", "Device", "Work", "Connect", "Behavior"]
	user_data_path = "/home/xiaoyang/competetion/data/user_data"
	log_data_directory = "/home/xiaoyang/competetion/data/totalExposureLog/"

	# 日志数据信息
	log_date = ["02-16", "02-17", "02-18", "02-19", "02-20", "02-21", "02-22", "02-23", "02-24", "02-25", "02-26",
				"02-27", "02-28", "03-01", "03-02", "03-03", "03-04", "03-05", "03-06", "03-07", "03-08", "03-09",
				"03-10", "03-11", "03-12", "03-13", "03-14", "03-15", "03-16", "03-17", "03-18", "03-19"]

	user_data = pd.read_csv(user_data_path, sep='\t', names=user_names)
	user_data = user_data.drop(["Area", "Behavior"], axis=1)
	for l_date in log_date:
		now = time.time()
		log = pd.read_csv(log_data_directory+"2019-"+l_date+".csv", sep='\t')
		log.columns = log_names

		merge_table = pd.merge(log, user_data, on={'UserId'})
		save_file = log_data_directory + "2019-" + l_date + "_join_user.csv"
		merge_table.to_csv(save_file, index=0, sep='\t')
		print(l_date, ' 这一天已经完成与 user_data 的 join 连接， 正在写入文件')
		print("总共耗时： ", time.time()-now)
		del(log)


def deal_with_deliver_time(file, save_file, columns=None, deliver_time_index="deliver_time"):
	'''
	这个函数主要是用来将定投时间转为48位二进制数的。， 然后连接原始的 DataFrame 进行保存
	'''
	data = pd.read_csv(file, sep='\t')
	if columns is not None:
		data.columns = columns
	t_name = ['t_' + str(i) for i in range(48)]
	bin_array = []

	for t in data[deliver_time_index]:
		t_bin = list(bin(t)[2:])
		t_bin = [0]*(48-len(t_bin)) + t_bin
		bin_array.append(t_bin)

	bin_dt = pd.DataFrame(bin_array, columns=t_name)

	final_data = pd.concat([data, bin_dt], axis=1)
	final_data.to_csv(save_file, sep='\t', index=0)

def deal_with_label(save_file):
	'''
	本次函数只是采用了一些简单的特征，且对于同一个广告id的不同请求，根据Aid，Size， Bid 做过滤处理。
	'''
	train_data_path = '/home/xiaoyang/competetion/data/my_final_train.dat'
	train_data = pd.read_csv(train_data_path, sep='\t')

	columns_ = ["ALid", "UserId", "Aid", "Size", "Bid", 'query_date']
	t_name = ['t_' + str(i) for i in range(48)]
	select_columns = columns_ + t_name

	train_data = train_data[select_columns]
	train_data['val'] = 1.0
	
	label_count = train_data[['Aid', 'query_date', 'val']].groupby(['Aid', 'query_date']).sum().groupby('Aid').mean()
	label_count.columns = ['exposure_mean']

	final = pd.merge(train_data, label_count, on='Aid')

	print('final feature :')
	print(final.columns)

	final_drop_duplicate = final.drop_duplicates(['Aid', 'Size', 'Bid'], 'first')

	# 读取静态数据
	static_data_path = '/home/xiaoyang/competetion/data/ad_static_feature.out'
	static_data = pd.read_csv(static_data_path, sep='\t', header=None)
	static_columns = ['Aid', 'CreateTime', 'AAid', 'ItemType', 'ItemId', "AIid","Size"]
	static_data.columns = static_columns
	static_data = static_data.drop('Size', axis=1)

	ff = pd.merge(final_drop_duplicate, static_data, on='Aid')
	print('ff feature :')
	print(ff.columns)

	ff.to_csv(save_file, index=0, sep='\t')
	# return ff


if __name__ == '__main__':
	# -------------------------------- 将 曝光日志中 分天存储---------------------------------
	# file_to_splits = '/home/xiaoyang/competetion/data/totalExposureLog.out'
	# save_directory = '/home/xiaoyang/competetion/data/totalExposureLog'

	# file_to_splits = '/home/xiaoyang/competetion/data/ad_static_feature.out'
	# save_directory = '/home/xiaoyang/competetion/data/ad_static_feature'
	# split_by_days(file_to_splits, timestamp_index=1, save_directory=save_directory)



	# -------------------------------- 从 曝光日志中获得 CRC 数据 ---------------------------------
	# get_CRC_data('/home/xiaoyang/competetion/data/ad_CPC_in_log.dat')


	# --------------------- 处理 test_sample 数据 ， 获得每条广告对应的投放时段---------------------
	# deal_with_test_sample('/home/xiaoyang/competetion/data/dealed_test_sample.dat')


	# ---------------------关联每天的曝光数据和user_data信息，为统计而用 ----------------------------
	# join_log_user()


	# ---------------------- 处理 训练CRC的 数据，考虑修改操作后，获得每条广告对应的投放时段------------
	# deal_with_train_data_on_time('/home/xiaoyang/competetion/data/train_with_deliver_time.dat')


	# ---------------------- 对投放时段进行48位的映射， 转化为具体的特征    -------------------------
	# # 对测试数据的文件的投放时段进行二进制映射, Ad Industry  AdAcount,  Audience Target
	# test_columns = ["SampleId", "Aid", "CreateTime", "Size", "AIid", "ItemType", "ItemId", "AAid", 
	# 				"DeliverTime", "AudTarget", "Bid", "create_date", "pre_date", "pre_weekday", "deliver_time"]
	# file = '/home/xiaoyang/competetion/data/dealed_test_sample.dat'
	# save_file = '/home/xiaoyang/competetion/data/my_final_test.dat'

	# deal_with_deliver_time(file, save_file, test_columns, "deliver_time")



	## 对训练数据进行投放时段的处理。
	# file = '/home/xiaoyang/competetion/data/train_with_deliver_time.dat'
	# save_file = '/home/xiaoyang/competetion/data/my_final_train.dat'
	# deal_with_deliver_time(file, save_file)


	#----------------------------- 对训练数据 join 静态数据， 并统计对应的标签 ------------------------
	deal_with_label('/home/xiaoyang/competetion/data/train_static.dat')

	t_name = ['t_' + str(i) for i in range(48)]
	select_columns = ["Aid", "Size", "Bid", "AIid", "AAid"] + t_name

	# 统计
	test_columns = ["SampleId"] + select_columns
	test_data = pd.read_csv('/home/xiaoyang/competetion/data/my_final_test.dat', sep='\t')
	test_data[test_columns].to_csv('/home/xiaoyang/competetion/data/test_data_simple.dat', sep='\t', index=0)

	train_columns = select_columns + ['exposure_mean']
	train_data = pd.read_csv('/home/xiaoyang/competetion/data/train_static.dat', sep='\t')
	train_data[train_columns].to_csv('/home/xiaoyang/competetion/data/train_data_simple.dat', sep='\t', index=0)


	# category_colums = ["ALid", "UserId", "Aid", "Size"]
