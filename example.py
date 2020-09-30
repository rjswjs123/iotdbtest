import sys
sys.path.append("./utils")
from utils.IoTDBConstants import *
from utils.Tablet import Tablet
from Session import Session
import os, re

directory=os.listdir('DataforIoTDB/normal/flexible/1')
os.chdir('DataforIoTDB/normal/flexible/1')
value_list=[]
for file in directory:
    with open(file) as f:
        data=f.read().splitlines()
        floats = []
        for elem in data:
            try:
                floats.append(float(elem))
            except ValueError:
                pass
    value_list.append(floats)



# creating session connection.
ip = "127.0.0.1"
port_ = "6667"
username_ = 'root'
password_ = 'root'
session = Session(ip, port_, username_, password_)
session.open(False)

# set and delete storage groups
session.set_storage_group("root.normalT")
#
# setting time series.
session.create_time_series("root.normalT.flexible", TSDataType.DOUBLE, TSEncoding.PLAIN, Compressor.SNAPPY)
session.create_time_series("root.normalT.rigid", TSDataType.DOUBLE, TSEncoding.PLAIN, Compressor.SNAPPY)


# setting multiple time series once.
ts_path_lst_ = ["root.normalT.flexible.x1.p1.s1", "root.normalT.flexible.x1.p1.s2", "root.normalT.flexible.x1.p1.s3","root.normalT.flexible.x1.p1.s4",
                "root.normalT.flexible.x1.p2.s1", "root.normalT.flexible.x1.p2.s2","root.normalT.flexible.x1.p2.s3","root.normalT.flexible.x1.p2.s4",
                "root.normalT.flexible.x1.p3.s1","root.normalT.flexible.x1.p3.s2","root.normalT.flexible.x1.p3.s3","root.normalT.flexible.x1.p3.s4",
                "root.normalT.flexible.x1.p4.s1","root.normalT.flexible.x1.p4.s2","root.normalT.flexible.x1.p4.s3","root.normalT.flexible.x1.p4.s4",
                "root.normalT.flexible.x1.p5.s1","root.normalT.flexible.x1.p5.s2","root.normalT.flexible.x1.p5.s3","root.normalT.flexible.x1.p5.s4"]
data_type_lst_=[]
for _ in range(20):
    data_type_lst_.append(TSDataType.DOUBLE)

encoding_lst_ = [TSEncoding.PLAIN for _ in range(len(data_type_lst_))]
compressor_lst_ = [Compressor.SNAPPY for _ in range(len(data_type_lst_))]
session.create_multi_time_series(ts_path_lst_, data_type_lst_, encoding_lst_, compressor_lst_)

#
# with open('nor11.dat') as file:
#     data = file.read().splitlines()
#     floats=[]
#     for elem in data:
#         try:
#             floats.append(float(elem))
#         except ValueError:
#             pass
data_types_ =[TSDataType.DOUBLE]
measurements_ = ["s1"]


# for time in range(len(floats)):
#     values = [floats[time]]
#     session.insert_record("root.testdat", time, measurements_, data_types_, values)

floats=value_list[0]
for time in range(len(floats)):
    values = [floats[time]]
    session.insert_record("root.testdat", time, measurements_, data_types_, values)


# insert multiple records into database
measurements_list_ = [["s1"], ["s2"]]
values_list_ = [[float(data[0])],[floats[1]]]
data_type_list_ = [data_types_, data_types_]
device_ids_ = ["root.testdat", "root.testdat"]
session.insert_records(device_ids_, [4, 5], measurements_list_, data_type_list_, values_list_)
