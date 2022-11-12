"""
Author: symlpigeon
Date: 2022-11-11 11:53:39
LastEditTime: 2022-11-11 11:54:12
LastEditors: symlpigeon
Description: 预处理LDPC矩阵
FilePath: /sim_bds/python/coding/ldpc_mat_gen/create_ldpc_meta_data.py
"""

import json
import numpy as np


idx_file1 = "ldpc_mat_idx_100_200.txt"
ele_file1 = "ldpc_mat_ele_100_200.txt"
out_file1 = "ldpc_mat_meta_data_100_200.json"
idx_file2 = "ldpc_mat_idx_44_88.txt"
ele_file2 = "ldpc_mat_ele_44_88.txt"
out_file2 = "ldpc_mat_meta_data_44_88.json"

idx_mat = np.zeros((100, 4), dtype=np.uint8)
with open(idx_file1, "r") as f:
    data = f.read()
data = data.split("\n")
while "" in data:
    data.remove("")
assert len(data) % 16 == 0, "Invalid number of lines!"

for line_idx in range(0, len(data), 16):
    for col_idx in range(4):
        for element in range(4):
            idx_mat[line_idx // 16 + 25 * col_idx][element] = int(
                data[line_idx + col_idx * 4 + element]
            )


ele_mat = np.zeros((100, 4), dtype=np.uint8)
with open(ele_file1, "r") as f:
    data = f.read()
data = data.split("\n")
while "" in data:
    data.remove("")
assert len(data) % 16 == 0, "Invalid number of lines!"
for line_idx in range(0, len(data), 16):
    for col_idx in range(4):
        for element in range(4):
            ele_mat[line_idx // 16 + 25 * col_idx][element] = int(
                data[line_idx + col_idx * 4 + element]
            )


with open(out_file1, "w") as f:
    json.dump({"idx": idx_mat.tolist(), "ele": ele_mat.tolist()}, f, indent=4)


idx_mat = np.zeros((44, 4), dtype=np.uint8)
with open(idx_file2, "r") as f:
    data = f.read()
data = data.split("\n")
while "" in data:
    data.remove("")
assert len(data) % 16 == 0, "Invalid number of lines!"

for line_idx in range(0, len(data), 16):
    for col_idx in range(4):
        for element in range(4):
            idx_mat[line_idx // 16 + 11 * col_idx][element] = int(
                data[line_idx + col_idx * 4 + element]
            )


ele_mat = np.zeros((44, 4), dtype=np.uint8)
with open(ele_file2, "r") as f:
    data = f.read()
data = data.split("\n")
while "" in data:
    data.remove("")
assert len(data) % 16 == 0, "Invalid number of lines!"
for line_idx in range(0, len(data), 16):
    for col_idx in range(4):
        for element in range(4):
            ele_mat[line_idx // 16 + 11 * col_idx][element] = int(
                data[line_idx + col_idx * 4 + element]
            )


with open(out_file2, "w") as f:
    json.dump({"idx": idx_mat.tolist(), "ele": ele_mat.tolist()}, f, indent=4)
