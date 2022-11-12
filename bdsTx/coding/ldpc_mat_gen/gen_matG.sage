"""
Author: symlpigeon
Date: 2022-11-11 16:05:42
LastEditTime: 2022-11-11 16:05:56
LastEditors: symlpigeon
Description: Sagemath LDPC矩阵生成
FilePath: /bdsTx/coding/ldpc_mat_gen/gen_matG.sage
"""

import json
import numpy as np

gf.<x> = GF(64, modulus=x^6+x+1)
k.<x> = gf
f = lambda x: k(x.digits(base=2))

H = np.array(json.load(open("ldpc_mat_100_200.json", "r")), dtype=np.uint8)
H1 = matrix(H[:, 0:100].tolist())
H2 = matrix(H[:, 100:200].tolist())
H1 = H1.apply_map(f)
H2 = H2.apply_map(f)
H2_ = H2.inverse()
H_ = (H2_ * H1).transpose()
H_ = list(H_)
H_int = []
for row in H_:
    H_int.append([x.integer_representation() for x in row])
with open("ldpc_matG_100_200.json", "w") as f:
    json.dump(H_int, f)


