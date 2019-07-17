import numpy as np
import pandas as pd
from tqdm import tqdm
import json
import gc
import random
import pickle
from scipy import sparse
import matplotlib.pyplot as plt

his = '2_23'
today = '2019-03-02'

user_fea = pd.read_csv('/home/hetongze/python_project/tencent2019/data/user_fea.csv')
cpc_exp = pd.read_csv('/home/hetongze/python_project/tencent2019/data/cpc_exp.csv')
cpc_exp.rename(columns = {'value_afterop':'crowd_orientation'}, inplace = True)
exp_his = pd.read_csv('/home/hetongze/python_project/tencent2019/exp_day/exp_'+his+'.csv', usecols=['uid'])

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

def helper(row,exp_his_uid, exp_his):
    if row['crowd_orientation'] == 'all':
        return exp_his.shape[0]
    dic_temp = convert_dict(row['crowd_orientation'])
    exp_his_uid['flag'] = exp_his_uid.apply(check, args=(dic_temp,), axis = 1)
    exp_his = pd.merge(exp_his, exp_his_uid.loc[:,['uid','flag']], on = 'uid', how = 'left')
    num = exp_his.loc[exp_his.flag == 1,'uid'].shape[0]
    exp_his.drop(['flag'], axis = 1, inplace = True)
    return num

exp_his_uid = pd.DataFrame({'uid':exp_his.uid.unique()})
exp_his_uid = pd.merge(exp_his_uid, user_fea, on = 'uid', how = 'left')

cpc_exp_today = cpc_exp.loc[cpc_exp.date_time == today,:]
del user_fea, cpc_exp
gc.collect()

temp = pd.DataFrame({'crowd_orientation':list(cpc_exp_today.crowd_orientation.value_counts().index)})
temp['co_his_exp'] = temp.apply(helper, args = (exp_his_uid, exp_his), axis = 1)
temp.to_csv('/home/hetongze/python_project/tencent2019/middle/crowd_ori_exp'+today+'_'+his+'.csv', index = False)