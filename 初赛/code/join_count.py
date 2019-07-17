import pandas as pd
import time


def write_to_result(file, content):
    with open(file, 'a+') as f:
        f.write(content)


result = '../data/result_after_join_user.txt'
# write header
write_to_result(result,
                "date" + '\t' + "age202_count" + '\t' + "gender2_count" + '\t' + "status2_count" + '\t' + "edu2_count" + '\t' +
                "cons2_count" + '\t' + "device3_count" + '\t' + "work2_count" + '\t' + "connect3_count" + '\t' + "all_count" +
                '\n')
print("write to result is completed ................")

# log_names=["ReqId", "ReqTime", "ALid", "UserId", "Aid", "Size", "Bid", "Pctr", "Ecpm", "TEcpm", "Date",
# 			 "Age", "Gender", "Status", "Education", "Cons", "Device", "Work", "Connect"]

log_data_directory = "/home/xiaoyang/competetion/data/totalExposureLog/"

# 日志数据信息
log_date = ["02-16", "02-17", "02-18", "02-19", "02-20", "02-21", "02-22", "02-23", "02-24", "02-25", "02-26",
            "02-27", "02-28", "03-01", "03-02", "03-03", "03-04", "03-05", "03-06", "03-07", "03-08", "03-09",
            "03-10", "03-11", "03-12", "03-13", "03-14", "03-15", "03-16", "03-17", "03-18", "03-19"]

# log_date = ["02-16"]

for l_date in log_date:
    now = time.time()
    log = pd.read_csv(log_data_directory + "2019-" + l_date + "_join_user.csv", sep='\t')
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

    for index, row in log.iterrows():
        if row['Age'] == 202:
            age202_count += 1

        if row['Gender'] == 2:
            gender2_count += 1

        if '2' in row['Status'].split(","):
            status2_count += 1

        if row['Education'] == 2:
            edu2_count += 1

        if row['Cons'] == 2:
            cons2_count += 1

        if row['Device'] == 3:
            device3_count += 1

        if '2' in row['Work'].split(','):
            work2_count += 1

        if row['Connect'] == 3:
            connect3_count += 1

        all_count += 1
    write_to_result(result, str(log['Date'][0]) + '\t' + str(age202_count) + '\t' + str(gender2_count) + '\t' + str(
        status2_count) + '\t' + str(edu2_count) + '\t' + str(cons2_count) + '\t' + str(device3_count) + '\t' + str(
        work2_count) + '\t' + str(connect3_count) + '\t' + str(all_count) + '\n')

    print(l_date, ' 这一天已经完成， 正在写入 result.txt ..........')
    print("总共耗时： ", time.time() - now)
