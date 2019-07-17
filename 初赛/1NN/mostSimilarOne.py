import json
import kNN
from numpy import *
import re
import csv


# 将19号曝光未曝光数据进行组合
def combineFeature():
	f = open('featuresOf0318.json', 'r')
	for i in f:
		featureDict = json.loads(i)

	features = []
	for key in featureDict:
		feature = []
		feature.append(key)
		feature += [featureDict[key][0], featureDict[key][1], featureDict[key][3], featureDict[key][4], featureDict[key][5], featureDict[key][2]]
		with open('combineFeature18.json', 'a') as file:
			file.write(json.dumps(feature) + '\n')

	f2 = open('noExpose0318_Feature.json', 'r')
	for i in f2:
		feature2Dict = json.loads(i)

	for key in feature2Dict:
		feature = []
		feature.append(key)
		feature += [feature2Dict[key][0], feature2Dict[key][4], feature2Dict[key][1], feature2Dict[key][2], feature2Dict[key][3], 0]
		with open('combineFeature18.json', 'a') as file:
			file.write(json.dumps(feature) + '\n')


# 将数据中不合理的多值进行清洗 合理的多值拆分 并整理为 素材尺寸-商品id-广告行业id-投放时段 格式
def filterFeature():
	with open('combineFeature18.json', 'r') as file:
		for line in file:
			line = json.loads(line)
			feature = []
			if not re.findall(',', line[4]):
				if not re.findall(',', line[1]):
					label = str(line[2]) + '-' + str(line[6])
					feature += [int(line[1]), int(line[3]), int(line[4]), int(line[5])]
					with open('Train18.json', 'a') as file:
						file.write(json.dumps(feature) + '\n')
					with open('trainLabel18.json', 'a') as file:
						file.write(json.dumps(label)+'\n')
	with open('combineFeature18.json', 'r') as file:
		for line in file:
			line = json.loads(line)
			
			if not re.findall(',', line[4]):
				if re.findall(',', line[1]):
					size = line[1].split(',')
					for i in size:
						feature = []
						label = str(line[2]) + '-' + str(line[6])
						feature += [int(i), int(line[3]), int(line[4]), int(line[5])]
						with open('Train18.json', 'a') as file:
							file.write(json.dumps(feature) + '\n')
						with open('trainLabel18.json', 'a') as file:
							file.write(json.dumps(label)+'\n')


# 将测试集整理成相同的格式 id 尺寸 商品id 广告行业id 投放时段 出价
def buildTest():
	with open('testSample_24.json', 'r') as file:
		for line in file:
			line = json.loads(line)
			feature = []
			bid = int(line[4])
			feature += [int(line[0]), int(line[3]), int(line[5]), int(line[6]), int(line[7])]
			with open('test_24.json', 'a') as file:
				file.write(json.dumps(feature) + '\n')
			with open('testLabel_24.json', 'a') as file:
				file.write(json.dumps(bid)+'\n')


# 预测与测试集在0319最邻近的那个值 1NN方法 输出为 bid-exposure
def kNNtest():
	# 生成数据集和类别标签
	dataSet, labels = kNN.createDataSet()
	# 定义一个未知类别的数据
	with open('test_24.json', 'r') as file:
		for line in file:
			line = json.loads(line)
			testid = line[0]
			testtarget = line[1:]
			testX = array([testtarget])
			# 调用分类函数对未知数据分类
			outputLabel = kNN.kNNClassify(testX, dataSet, labels, 1)
			result = [outputLabel, testid]
			with open('testPredict24.json', 'a') as file:
				file.write(json.dumps(result) + '\n')
			# print(testX, outputLabel)


# 按照比例计算出最终的结果
def predictSample():
	predict = []
	bid_B = []
	result = []
	test_id = []
	with open('testPredict24.json', 'r') as file:
		for line in file:
			line = json.loads(line)
			testid = line[1]
			target = line[0].split('-')
			test_id.append(testid)
			predict.append(target)
	with open('testLabel_24.json', 'r') as file:
		for line in file:
			line = json.loads(line)
			bid_B.append(line)
	# print(bid_B)

	for i in range(len(predict)):
		if int(predict[i][0]) != 0:
			exp_B = int(predict[i][1])*(bid_B[i]/(int(predict[i][0])))
			exp_B = int(exp_B*10000)
			result.append(exp_B/10000)
		else:
			result.append(0)

	out = open('submission5.csv', 'a', newline='')
	# writer=csv.writer(f)与下面一行等价，delimiter默认是逗号
	writer = csv.writer(out, delimiter=',')

	for i in range(len(result)):
		writer.writerow([test_id[i], result[i]])


# combineFeature()
# filterFeature()
# buildTest()
# kNNtest()
predictSample()


