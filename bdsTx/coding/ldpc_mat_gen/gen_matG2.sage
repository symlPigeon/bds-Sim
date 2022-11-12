import json
import numpy as np

gf.<x> = GF(64, modulus=x^6+x+1)
k.<x> = gf
f = lambda x: k(x.digits(base=2))

H_2 = np.array(json.load(open("ldpc_mat_44_88.json", "r")), dtype=np.uint8)
H1_2 = matrix(H_2[:, 0:44].tolist())
H2_2 = matrix(H_2[:, 44:88].tolist())
H1_2 = H1_2.apply_map(f)
H2_2 = H2_2.apply_map(f)
H2_2_ = H2_2.inverse()
H_2_ = (H2_2_ * H1_2).transpose()
H_2_ = list(H_2_)
H_int_2 = []
for row in H_2_:
    H_int_2.append([x.integer_representation() for x in row])
with open("ldpc_matG_44_88.json", "w") as f:
    json.dump(H_int_2, f)