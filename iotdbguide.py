import sys
sys.path.append("./utils")
from utils.IoTDBConstants import *
from utils.Tablet import Tablet
from Session import Session


# creating session connection.
ip = "127.0.0.1"
port_ = "6667"
username_ = 'root'
password_ = 'root'
session = Session(ip, port_, username_, password_)
session.open(False)

# set and delete storage groups
session.set_storage_group("root.sg_test_01")
session.set_storage_group("root.sg_test_02")
session.set_storage_group("root.sg_test_03")
session.set_storage_group("root.sg_test_04")
session.delete_storage_group("root.sg_test_02")
session.delete_storage_groups(["root.sg_test_03", "root.sg_test_04"])

# setting time series.
session.create_time_series("root.sg_test_01.d_01.s_01", TSDataType.BOOLEAN, TSEncoding.PLAIN, Compressor.SNAPPY)
session.create_time_series("root.sg_test_01.d_01.s_02", TSDataType.INT32, TSEncoding.PLAIN, Compressor.SNAPPY)
session.create_time_series("root.sg_test_01.d_01.s_03", TSDataType.INT64, TSEncoding.PLAIN, Compressor.SNAPPY)

# setting multiple time series once.
ts_path_lst_ = ["root.sg_test_01.d_01.s_04", "root.sg_test_01.d_01.s_05", "root.sg_test_01.d_01.s_06",
                "root.sg_test_01.d_01.s_07", "root.sg_test_01.d_01.s_08", "root.sg_test_01.d_01.s_09"]
data_type_lst_ = [TSDataType.FLOAT, TSDataType.DOUBLE, TSDataType.TEXT,
                  TSDataType.FLOAT, TSDataType.DOUBLE, TSDataType.TEXT]
encoding_lst_ = [TSEncoding.PLAIN for _ in range(len(data_type_lst_))]
compressor_lst_ = [Compressor.SNAPPY for _ in range(len(data_type_lst_))]
session.create_multi_time_series(ts_path_lst_, data_type_lst_, encoding_lst_, compressor_lst_)

# delete time series
session.delete_time_series(["root.sg_test_01.d_01.s_07", "root.sg_test_01.d_01.s_08", "root.sg_test_01.d_01.s_09"])

# insert one record into the database.
measurements_ = ["s_01", "s_02", "s_03", "s_04", "s_05", "s_06"]
values_ = [False, 10, 11, 1.1, 10011.1, "test_record"]
data_types_ = [TSDataType.BOOLEAN, TSDataType.INT32, TSDataType.INT64,
               TSDataType.FLOAT, TSDataType.DOUBLE, TSDataType.TEXT]
session.insert_record("root.sg_test_01.d_01", 1, measurements_, data_types_, values_)

# insert multiple records into database
measurements_list_ = [["s_01", "s_02", "s_03", "s_04", "s_05", "s_06"],
                      ["s_01", "s_02", "s_03", "s_04", "s_05", "s_06"]]
values_list_ = [[False, 22, 33, 4.4, 55.1, "test_records01"],
                [True, 77, 88, 1.25, 8.125, "test_records02"]]
data_type_list_ = [data_types_, data_types_]
device_ids_ = ["root.sg_test_01.d_01", "root.sg_test_01.d_01"]
session.insert_records(device_ids_, [2, 3], measurements_list_, data_type_list_, values_list_)

# close session connection.
session.close()
print("All executions done!!")