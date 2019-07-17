import numpy as np
import pandas as pd
from tqdm import tqdm
import json
import gc
import random
import pickle
from scipy import sparse
import matplotlib.pyplot as plt

user_fea = pd.read_csv('/home/hetongze/python_project/tencent2019/data/user_fea.csv')
dic = pickle.load(open('/home/hetongze/python_project/tencent2019/crowd_ori/dic.pkl', 'rb'))

uid_done = []
with open('/home/hetongze/python_project/tencent2019/crowd_ori/done.txt','r') as f:
    for uid in f.readlines():
        uid = uid.strip()
        uid_done.append(int(uid))

def convert_dict(crowd):
    d = {}
    crowd = crowd.split('|')
    for i in range(len(crowd)):
        crowd_i = crowd[i].split(':')
        fea = crowd_i[0]
        if fea == 'connectionType':
            fea = 'connection_type'
        if fea == 'consuptionAbility':
            fea = 'consuption_ability'
        value = list(map(int, crowd_i[1].strip(',').split(',')))
        d[fea] = value
    return d

def check(row, crowd_dic):
    for fea in crowd_dic.keys():
        if fea in ['age','gender','education','consuption_ability','device','connection_type']:
            if row[fea] not in crowd_dic[fea]:
                return 0
        else:
            if fea in ['area','status','work','behavior']:
                value = row[fea].strip(',').split(',')
                value = list(map(int, value))
                if len(set(value) & set(crowd_dic[fea])) == 0:
                    return 0
    return 1

with open('/home/hetongze/python_project/tencent2019/crowd_ori/done.txt','a+') as f:
    crowd_ori_all_uid = {}
    for co in dic.keys():
        if dic[co] in uid_done:
            continue
        print(dic[co])
        if co == 'all':
            continue
        dic_temp = convert_dict(co)
        user_fea['flag'] = user_fea.apply(check, args=(dic_temp,), axis = 1)
        match_uid = list(user_fea.loc[user_fea.flag == 1,'uid'].values)
        crowd_ori_all_uid[co] = len(match_uid)
        pickle.dump(match_uid, open('/home/hetongze/python_project/tencent2019/crowd_ori/crowd_ori_uid_'+str(dic[co])+'.pkl', 'wb'))
        gc.collect()
        f.write(str(dic[co])+'\n')
    pickle.dump(crowd_ori_all_uid, open('/home/hetongze/python_project/tencent2019/crowd_ori/crowd_ori_uid_num.pkl', 'wb'))