'''
Author: symlpigeon
Date: 2022-11-08 10:52:12
LastEditTime: 2022-11-08 15:23:08
LastEditors: symlpigeon
Description: PRN主码参数的预处理脚本
FilePath: /sim_bds/python/coding/prn_data/process_copied_data.py
'''


import json

print("This script is used to process the PRN data copied from BDS ICD file!")

filename = input("input the data master code file name:")

with open(filename, "r") as f:
    data = f.read()

data = data.split("\n")
while "" in data:
    data.remove("")

json_data = {"data": [], "pilot": [], "sub_pilot": []}
assert len(data) % 5 == 0, "Invalid lines!"

for line_idx in range(len(data)):
    data[line_idx] = data[line_idx].replace(" ", "")

for i in range(0, len(data), 5):
    prn = int(data[i])
    w = int(data[i + 1])
    p = int(data[i + 2])
    first_24bit = data[i + 3]
    last_24bit = data[i + 4]
    json_data["data"].append({
        "prn": prn,
        "w": w,
        "p": p,
        "first_24bit": first_24bit,
        "last_24bit": last_24bit
    })

filename = input("input the pilot master code file name:")

with open(filename, "r") as f:
    data = f.read()

data = data.split("\n")
while "" in data:
    data.remove("")

assert len(data) % 5 == 0, "Invalid lines!"

for line_idx in range(len(data)):
    data[line_idx] = data[line_idx].replace(" ", "")

for i in range(0, len(data), 5):
    prn = int(data[i])
    w = int(data[i + 1])
    p = int(data[i + 2])
    first_24bit = data[i + 3]
    last_24bit = data[i + 4]
    json_data["pilot"].append({
        "prn": prn,
        "w": w,
        "p": p,
        "first_24bit": first_24bit,
        "last_24bit": last_24bit
    })


filename = input("input the pilot sub code file name:")

with open(filename, "r") as f:
    data = f.read()

data = data.split("\n")
while "" in data:
    data.remove("")

assert len(data) % 5 == 0, "Invalid lines!"

for line_idx in range(len(data)):
    data[line_idx] = data[line_idx].replace(" ", "")

for i in range(0, len(data), 5):
    prn = int(data[i])
    w = int(data[i + 1])
    p = int(data[i + 2])
    first_24bit = data[i + 3]
    last_24bit = data[i + 4]
    json_data["sub_pilot"].append({
        "prn": prn,
        "w": w,
        "p": p,
        "first_24bit": first_24bit,
        "last_24bit": last_24bit
    })


with open("b1c_prn_data.json", "w") as f:
    f.write(json.dumps(json_data, indent=4))
