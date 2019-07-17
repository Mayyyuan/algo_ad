import time
import pandas as pd


def join_log_user():
    log_names=["ReqId", "ReqTime", "ALid", "UserId", "Aid", "Size", "Bid", "Pctr", "Ecpm", "TEcpm", "Date"]
    user_names=["UserId", "Age", "Gender", "Area", "Status", "Education", "Cons", "Device", "Work", "Connect", "Behavior"]
    user_data_path = "../data/user_data"
    log_data_directory = "../data/totalExposureLog/"

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
        del log
