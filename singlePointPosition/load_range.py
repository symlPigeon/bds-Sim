'''
Author: symlPigeon 2163953074@qq.com
Date: 2023-05-24 23:43:08
LastEditTime: 2023-05-25 00:31:02
LastEditors: symlPigeon 2163953074@qq.com
Description: Load Pseudorange from Mat file
FilePath: /bds-Sim/singlePointPosition/load_range.py
'''

import h5py
import numpy as np


def get_pseudorange(mat):
    return np.array(mat.get("Pseudorange_m"))

def get_PRN(mat):
    return np.array(mat.get("PRN"))

def get_mat(filepath):
    f = h5py.File(filepath, "r")
    return f

def get_avg_pseudorange(mat):
    dists = {}
    prn = get_PRN(mat)
    pseudorange = get_pseudorange(mat)
    X, Y = pseudorange.shape
    for row in range(X):
        for col in range(Y):
            if prn[row][col] != 0:
                if prn[row][col] not in dists:
                    dists[prn[row][col]] = []
                if pseudorange[row][col] != 0:
                    dists[prn[row][col]].append(pseudorange[row][col])
    avg_dist = {}
    for key in dists:
        avg_dist[key] = np.mean(dists[key])
    return avg_dist