"""
Author: symlpigeon
Date: 2022-11-11 11:44:09
LastEditTime: 2022-11-11 11:48:43
LastEditors: symlpigeon
Description: LDPC矩阵
FilePath: /sim_bds/python/coding/ldpc_mat.py
"""

import json
import numpy as np
import galois
from typing import List, Tuple


def singleton(cls):
    instances = {}

    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return getinstance


def gen_matG(matH: List[List[int]]) -> np.ndarray:
    """生成矩阵G

    Args:
        matH (_type_): _description_

    Returns:
        _type_: _description_
    """
    Poly = galois.Poly([1, 0, 0, 0, 0, 1, 1])
    GF = galois.GF(2**6, irreducible_poly=Poly)
    H = np.array(matH)
    k, _ = H.shape
    H1 = GF(H[:, :k])
    H2 = GF(H[:, k:])
    H2_1 = np.linalg.inv(H2)
    H_ = H2_1 @ H1
    I_k = GF(np.eye(k, dtype=np.uint8))
    return np.concatenate((I_k, H_.T), axis=1)


@singleton
class ldpcMat_100_200:
    def __init__(self, filepath="ldpc_mat_gen/ldpc_mat_100_200.json"):
        self._mat = gen_matG(json.load(open(filepath, "r")))

    def mat(self):
        return self._mat


@singleton
class ldpcMat_44_88:
    def __init__(self, filepath="ldpc_mat_gen/ldpc_mat_44_88.json"):
        self._mat = gen_matG(json.load(open(filepath, "r")))

    def mat(self):
        return self._mat
