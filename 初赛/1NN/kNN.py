from numpy import *
import json


# 建立训练集的向量集合和label集合
def createDataSet():
	train_X = []
	train_Y = []

	with open('Train1.json', 'r') as file:
		for line in file:
			line = json.loads(line)
			train_X.append(line)
	with open('trainLabel1.json', 'r') as file:
		for line in file:
			line = json.loads(line)
			train_Y.append(line)

	group = array(train_X)
	# 4个样本分别所属的类别
	labels = train_Y
	return group, labels


# 返回最邻近结果
def kNNClassify(newInput, dataSet, labels, k):
	numSamples = dataSet.shape[0]
	print(numSamples)
	diff = tile(newInput, (numSamples, 1)) - dataSet  # 按元素求差值
	squaredDiff = diff ** 2  # 将差值平方
	squaredDist = sum(squaredDiff, axis = 1)   # 按行累加
	distance = squaredDist ** 0.5  # 将差值平方和求开方，即得距离

	sortedDistIndices = argsort(distance)
	voteLabel = labels[sortedDistIndices[0]]
	# classCount = {} # define a dictionary (can be append element)
	# for i in xrange(k):
	# 	# # step 3: 选择k个最近邻
	# 	voteLabel = labels[sortedDistIndices[i]]
	# 	classCount[voteLabel] = classCount.get(voteLabel, 0) + 1

	# maxCount = 0
	# for key, value in classCount.items():
	# 	if value > maxCount:
	# 		maxCount = value
	# 		maxIndex = key

	return voteLabel