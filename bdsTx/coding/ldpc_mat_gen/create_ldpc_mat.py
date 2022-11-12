"""
Author: symlpigeon
Date: 2022-11-11 12:06:15
LastEditTime: 2022-11-11 12:06:17
LastEditors: symlpigeon
Description: 生成LDPC矩阵
FilePath: /sim_bds/python/coding/ldpc_mat_gen/create_ldpc_mat.py
"""

import numpy as np
import json


filepath = "ldpc_mat_meta_data_100_200.json"
with open(filepath, "r") as f:
    data = json.load(f)

mat = np.zeros((100, 200), dtype=np.uint8)
mat_idx = data["idx"]
mat_ele = data["ele"]

i = 0
while i < 100:
    j = 0
    while j < 4:
        mat[i, mat_idx[i][j]] = mat_ele[i][j]
        j += 1
    i += 1


with open("ldpc_mat_100_200.json", "w") as f:
    json.dump(mat.tolist(), f)


filepath = "ldpc_mat_meta_data_44_88.json"
with open(filepath, "r") as f:
    data = json.load(f)

mat = np.zeros((44, 88), dtype=np.uint8)
mat_idx = data["idx"]
mat_ele = data["ele"]

i = 0
while i < 44:
    j = 0
    while j < 4:
        mat[i, mat_idx[i][j]] = mat_ele[i][j]
        j += 1
    i += 1


with open("ldpc_mat_44_88.json", "w") as f:
    json.dump(mat.tolist(), f)
