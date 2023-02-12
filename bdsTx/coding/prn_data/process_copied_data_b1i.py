'''
Author: symlpigeon
Date: 2023-01-08 14:48:28
LastEditTime: 2023-01-08 14:53:29
LastEditors: symlpigeon
Description: 处理文档中的B1I卫星测距码相位分配数据
FilePath: /bds-Sim/bdsTx/coding/prn_data/processing_copied_data_b1i.py
'''

import json

with open("./b1i_phase_info.txt", "r") as f:
    data = f.read()
data = data.split("\n")
while "" in data:
    data.remove("")
json_data = {"data": []}
assert len(data) == 63,  "Missing some data entries! Expected 63, got {}.".format(len(data))
for idx in range(len(data)):
    json_data_entry = {}
    json_data_entry["prn"] = idx + 1
    json_data_phase_list = []
    data_entry = data[idx].split("⊕")
    for phase in data_entry:
        json_data_phase_list.append(int(phase))
    json_data_entry["phase"] = json_data_phase_list
    json_data["data"].append(json_data_entry)
with open("./b1i_phase_info.json", "w") as f:
    json.dump(json_data, f, indent=4)