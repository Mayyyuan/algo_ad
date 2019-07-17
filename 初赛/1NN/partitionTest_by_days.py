import time
import json


# 将测试集中的数据按天划分 20号之前 20 21 22 23 24
def extractTest_Sample():
	with open('../testA/test_sample.dat', 'r') as file:
		for line in file:
			line = line.split()
			time_array = time.localtime(int(line[2]))
			otherStyleTime = time.strftime("%Y%m%d", time_array)
			if otherStyleTime < '20190320':
				temp = []
				temp += [line[0], line[1], otherStyleTime, line[3], line[10], line[6], line[4]]
				timestamp = line[8].split(',')
				stamp = int(timestamp[2])
				stamp_bin = bin(stamp)
				period = int(stamp_bin.count('1')*0.5)
				temp.append(period)
				with open('testSample_before20.json', 'a') as file_0319:
					file_0319.write(json.dumps(temp)+'\n')
			if otherStyleTime == '20190320':
				temp = []
				temp += [line[0], line[1], otherStyleTime, line[3], line[10], line[6], line[4]]
				timestamp = line[8].split(',')
				stamp = int(timestamp[3])
				stamp_bin = bin(stamp)
				period = int(stamp_bin.count('1')*0.5)
				temp.append(period)
				with open('testSample_20.json', 'a') as file_0320:
					file_0320.write(json.dumps(temp)+'\n')
			if otherStyleTime == '20190321':
				temp = []
				temp += [line[0], line[1], otherStyleTime, line[3], line[10], line[6], line[4]]
				timestamp = line[8].split(',')
				stamp = int(timestamp[4])
				stamp_bin = bin(stamp)
				period = int(stamp_bin.count('1')*0.5)
				temp.append(period)
				with open('testSample_21.json', 'a') as file_0321:
					file_0321.write(json.dumps(temp)+'\n')
			if otherStyleTime == '20190322':
				temp = []
				temp += [line[0], line[1], otherStyleTime, line[3], line[10], line[6], line[4]]
				timestamp = line[8].split(',')
				stamp = int(timestamp[5])
				stamp_bin = bin(stamp)
				period = int(stamp_bin.count('1')*0.5)
				temp.append(period)
				with open('testSample_22.json', 'a') as file_0322:
					file_0322.write(json.dumps(temp)+'\n')
			if otherStyleTime == '20190323':
				temp = []
				temp += [line[0], line[1], otherStyleTime, line[3], line[10], line[6], line[4]]
				timestamp = line[8].split(',')
				stamp = int(timestamp[6])
				stamp_bin = bin(stamp)
				period = int(stamp_bin.count('1')*0.5)
				temp.append(period)
				with open('testSample_23.json', 'a') as file_0323:
					file_0323.write(json.dumps(temp)+'\n')
			if otherStyleTime == '20190324':
				temp = []
				temp += [line[0], line[1], otherStyleTime, line[3], line[10], line[6], line[4]]
				timestamp = line[8].split(',')
				stamp = int(timestamp[0])
				stamp_bin = bin(stamp)
				period = int(stamp_bin.count('1')*0.5)
				temp.append(period)
				with open('testSample_24.json', 'a') as file_0324:
					file_0324.write(json.dumps(temp)+'\n')


extractTest_Sample()
