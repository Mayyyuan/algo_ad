import pandas as pd

f = open('../data/result.txt', 'w')
f.write("date" + '\t' + "age202_count" + '\t' + "gender2_count" + '\t' + "status2_count" + '\t' + "edu2_count" + '\t' +
        "cons2_count" + '\t' + "device3_count" + '\t' + "work2_count" + '\t' + "connect3_count" + '\t' + "all_count" +
        '\n')

# 用户数据信息
user = pd.read_table("../data/user_data", header=None, names=["UserId", "Age", "Gender", "Area", "Status", "Education",
                                                              "Cons", "Device", "Work", "Connect", "Behavior"])

# 日志数据信息
log_date = ["02-16", "02-17", "02-18", "02-19", "02-20", "02-21", "02-22", "02-23", "02-24", "02-25", "02-26",
            "02-27", "02-28", "03-01", "03-02", "03-03", "03-04", "03-05", "03-06", "03-07", "03-08", "03-09",
            "03-10", "03-11", "03-12", "03-13", "03-14", "03-15", "03-16", "03-17", "03-18", "03-19"]
# log_date = ["02-16"]

for l_date in log_date:
    log = pd.read_table("../data/2019-"+l_date+".csv", header=None,
                        names=["ReqId", "ReqTime", "ALid", "UserId", "Aid", "Size",
                               "Bid", "Pctr", "Ecpm", "TEcpm", "Date"])
    # 计数并追加写入文件：统计当天gender=2，cons=2,connect=3的曝光人群的数量
    age202_count = 0
    gender2_count = 0
    status2_count = 0
    edu2_count = 0
    cons2_count = 0
    device3_count = 0
    work2_count = 0
    connect3_count = 0
    all_count = 0
    for uid in log['UserId']:
        if user['Age'][user['UserId'] == uid].item() == 202:
            age202_count += 1
        if user['Gender'][user['UserId'] == uid].item() == 2:
            gender2_count += 1
        for s in user['Status'][user['UserId'] == uid].str.split(","):
            for ss in s:
                if ss == '2':
                    status2_count += 1
        if user['Education'][user['UserId'] == uid].item() == 2:
            edu2_count += 1
        if user['Cons'][user['UserId'] == uid].item() == 2:
            cons2_count += 1
        if user['Device'][user['UserId'] == uid].item() == 3:
            device3_count += 1
        for s in user['Work'][user['UserId'] == uid].str.split(","):
            for ss in s:
                if ss == '2':
                    work2_count += 1
        if user['Connect'][user['UserId'] == uid].item() == 3:
            connect3_count += 1
        all_count += 1
        print(all_count)
    f.write(str(log['Date'][0])+'\t' + str(age202_count) + '\t' + str(gender2_count) + '\t' + str(status2_count) + '\t'
            + str(edu2_count) + '\t' + str(cons2_count) + '\t' + str(device3_count) + '\t' + str(work2_count) + '\t'
            + str(connect3_count) + '\t' + str(all_count)+'\n')
f.close()
