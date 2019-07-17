import numpy as np
import pandas as pd
from tqdm import tqdm
import json
import gc
import random
import pickle
from scipy import sparse
import matplotlib.pyplot as plt

ad_op = pd.read_csv('/home/hetongze/python_project/tencent2019/testA/ad_operation.dat',sep = '\t', header = None, names = \
                       ['aid','mod_time','op_type','mod_fields','value_afterop'])
ad_static_fea = pd.read_csv('/home/hetongze/python_project/tencent2019/testA/ad_static_feature.out',sep = '\t', header = None, names = \
                       ['aid','create_time','ad_account_id','product_id','product_cate','ad_hangye_id','ad_size'])

# 2.30关闭广告且3.1再次开启，所以可以直接去掉
ad_op['hour'] = pd.to_datetime(ad_op['mod_time'], format = '%Y%m%d%H%M%S', errors = 'coerce')
ind = list(ad_op.loc[(ad_op.mod_time == '20190230000000') & (ad_op.op_type == 1) & (ad_op.mod_fields == 1) & (ad_op.value_afterop == '0'), :].index)
ad_op.drop(ind, axis = 0, inplace = True)

# 选出创建广告操作，在静态feature中找到创建时间
create_op = ad_op.loc[ad_op.op_type == 2,:]
create_time = ad_static_fea.loc[ad_static_fea.aid.isin(create_op.aid.unique()), ['aid','create_time']]
create_op = pd.merge(create_op, create_time, on = 'aid', how = 'left')
create_op.drop('hour', axis = 1, inplace = True)
create_op.rename(columns = {'create_time':'time'}, inplace = True)

# 选出修改广告操作，把修改时间按小时力度生成‘hour’
mod_op = ad_op.loc[ad_op.op_type == 1,:]
mod_op['h'] = mod_op['mod_time'].map(lambda x: x if x == '0' else x[:10])
mod_op['h'] = pd.to_datetime(mod_op['h'], format = '%Y%m%d%H', errors = 'coerce')
mod_op.rename(columns = {'hour':'time','h':'hour'}, inplace = True)

# 在修改广告操作中选出修改人群定向操作，由于修改是实时记录，需要按小时粒度得到最后的修改结果
crowd_ori_mod = mod_op.loc[mod_op.mod_fields == 3,:]
flag = crowd_ori_mod.groupby(['aid','hour'])['time'].max().reset_index()
flag['f'] = 1
crowd_ori_mod = pd.merge(crowd_ori_mod, flag, on = ['aid','hour','time'], how = 'left')
crowd_ori_mod = crowd_ori_mod.loc[crowd_ori_mod.f == 1, :]
crowd_ori_mod.drop(['f'], axis = 1, inplace = True)
crowd_ori_mod = crowd_ori_mod.loc[:,['aid','op_type','value_afterop','time']]

# 在创建广告操作中选出创建人群定向操作，与修改人群定向操作合并得到人群定向特征
crowd_ori_create = create_op.loc[create_op.mod_fields == 3,['aid','op_type','value_afterop','time']]
crowd_ori = pd.concat([crowd_ori_create, crowd_ori_mod], axis = 0).reset_index(drop = True)