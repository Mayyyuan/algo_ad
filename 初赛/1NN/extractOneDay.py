import time
import json
import datetime
import pandas as pd


# 提取日志中某天所有曝光的数据
def extract0319ofLog():
	filename = '../ad_CPC_in_log.dat'
	with open(filename, 'r') as file:
		for line in file:
			line2 = line.split()
			timestamp = line2[1]
			timeArray = time.localtime(int(timestamp))
			otherStyleTime = time.strftime("%Y%m%d", timeArray)
			if otherStyleTime == '20190318':
				with open('logOf0318.dat', 'a') as file:
					file.write(line)


# 将曝光的数据统计各id日曝光量
def groupby0319():
	path1 = '../testA/test_sample.dat'
	oper_data = pd.read_table(path1, header=None, sep='\s+')
	# print(oper_data)
	data = oper_data.groupby([2])[2].value_counts()
	print(data)
	data = pd.DataFrame(data)
	data.to_csv('groupbytestSample.csv', index=True, header=False)

	with open('groupbytestSample.csv', 'r') as file:
		for line in file:
			line = line.split(',')
			timeArray = time.localtime(int(line[1]))
			otherStyleTime = time.strftime("%Y%m%d", timeArray)
			with open('testSampleDate.josn', 'a') as file:
				file.write(json.dumps([otherStyleTime, line[2]])+'\n')


def groupby0319_2():
	path1 = 'logOf0318.dat'
	idDict = {}
	with open(path1, 'r') as file:
		for line in file:
			line = line.split()
			if line[4] in idDict:
				idDict[line[4]] += 1
			else:
				idDict[line[4]] = 1
	# with open('count0319.json', 'a') as file:
	# 	file.write(json.dumps(idDict))
	return idDict


# 在log日志中提取广告id 素材尺寸 出价bid 日曝光 特征
def extractKeyItem(idDict):
	path1 = 'logOf0318.dat'
	featureDict = {}
	with open(path1, 'r') as file:
		for line in file:
			line = line.split()
			if line[4] in idDict and idDict[line[4]] != 0:
				temp = []
				temp += [line[5], line[6], idDict[line[4]]]
				featureDict[line[4]] = []
				featureDict[line[4]] += temp
				idDict[line[4]] = 0
	with open('keyInformation18.json', 'a') as file:
		file.write(json.dumps(featureDict))


# 提取静态数据中 商品id 广告行业id两个特征
def otherFeatures():
	f = open('keyInformation18.json', 'r')
	for i in f:
		idDict = json.loads(i)
	with open('../ad_static_feature.dat', 'r') as file:
		for line in file:
			line = line.split()
			if line[0] in idDict:
				if len(line) == 7:
					idDict[line[0]] += [line[3], line[5]]
				elif len(line) == 6:
					idDict[line[0]] += [0, line[4]]
	with open('feature0318.json', 'a') as file:
		file.write(json.dumps(idDict))


# 提取操作中 投放时长 特征 缺失的补为24
def otherFeatures2():
	f = open('feature0318.json', 'r')
	for i in f:
		idDict = json.loads(i)
	featureDict = {}
	with open('../ad_operation.dat', 'r') as file:
		for line in file:
			line = line.split()
			if line[0] in idDict:
				if line[2] == '2' and line[3] == '4':
					timestamp = line[4].split(',')
					stamp = int(timestamp[1])
					stamp_bin=bin(stamp)
					period = int(stamp_bin.count('1')*0.5)
					idDict[line[0]].append(period)
	for key in idDict:
		if len(idDict[key]) == 5:
			featureDict[key] = idDict[key][:]
			featureDict[key].append(24)
		else:
			featureDict[key] = idDict[key][:]

	with open('featuresOf0318.json', 'a') as file:
		file.write(json.dumps(featureDict))


# 提取未曝光数据部分
def noExposureFeature():
	noexposeDict = {}
	with open('../not_inLogNo_expose.txt', 'r') as file:
		for line in file:
			line = line.split(' ')
			if line[1] == '20190318':
				noexposeDict[line[0]] = 1

	with open('../ad_static_feature.dat', 'r') as file:
		for line in file:
			line = line.split()
			if line[0] in noexposeDict:
				noexposeDict[line[0]] = []
				if len(line) == 7:
					noexposeDict[line[0]] += [line[6], line[3], line[5]]
				elif len(line) == 6:
					noexposeDict[line[0]] += [line[5], 0, line[4]]

	featureDict0 = {}
	for key in noexposeDict:
		if noexposeDict[key] != 1:
			featureDict0[key] = noexposeDict[key][:]
	
	featureDict = {}
	with open('../ad_operation.dat', 'r') as file:
		for line in file:
			line = line.split()
			if line[0] in featureDict0:
				if line[2] == '2' and line[3] == '4':
					timestamp = line[4].split(',')
					stamp = int(timestamp[1])
					stamp_bin=bin(stamp)
					period = int(stamp_bin.count('1')*0.5)
					featureDict0[line[0]].append(period)
	for key in featureDict0:
		if len(featureDict0[key]) == 3:
			featureDict[key] = featureDict0[key][:]
			featureDict[key].append(24)
		else:
			featureDict[key] = featureDict0[key][:]

	featureDict2 = {}
	with open('../ad_operation.dat', 'r') as file:
		for line in file:
			line = line.split()
			if line[0] in featureDict:
				if line[2] == '2' and line[3] == '2':
					featureDict[line[0]].append(line[4])
	for key in featureDict:
		if len(featureDict[key]) == 4:
			featureDict2[key] = featureDict[key][:]
			featureDict2[key].append(0)
		else:
			featureDict2[key] = featureDict[key][:]
	# print(featureDict2)

	with open('noExpose0318_Feature.json', 'a') as file:
		file.write(json.dumps(featureDict2))


# extract0319ofLog()
# groupby0319()
# idDict = groupby0319_2()
# extractKeyItem(idDict)
# otherFeatures()
# otherFeatures2()
noExposureFeature()