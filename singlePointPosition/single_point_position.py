"""
Author: symlPigeon 2163953074@qq.com
Date: 2023-05-24 23:59:05
LastEditTime: 2024-02-26 10:31:01
LastEditors: symlPigeon 2163953074@qq.com
Description: SPP
FilePath: /bds-Sim/singlePointPosition/single_point_position.py
"""

import numpy as np


def simple_SPP_SVD(sat_pos, pseudorange):
    R = 6378137
    A = []
    for m in range(0, len(sat_pos)):
        x = sat_pos[m][0]
        y = sat_pos[m][1]
        z = sat_pos[m][2]
        Am = -2 * x
        Bm = -2 * y
        Cm = -2 * z
        Dm = R * R + (pow(x, 2) + pow(y, 2) + pow(z, 2)) - pow(pseudorange[m], 2)
        A += [[Am, Bm, Cm, Dm]]
    A = np.array(A)
    (_, _, v) = np.linalg.svd(A)
    w = v[3, :]
    w /= w[3]
    return w


if __name__ == "__main__":
    from bdsTx.satellite_info.coordinate_system import ecef2lla
    from singlePointPosition.load_range import *

    # sat_pos1 = [
    #     -6110591.5315955505,
    #     39268198.54905198,
    #     -13654951.054403083
    # ]
    # sat_pos2 = [
    #     -9063806.22679317,
    #     25784964.29781798,
    #     32144269.425759535
    # ]
    # sat_pos3 = [
    #     -20286236.795862414,
    #     30541523.682453774,
    #     -20977410.873297542
    # ]
    # sat_pos4 = [
    #     -512938.13691326976,
    #     41657498.42239846,
    #     -3744446.881240455
    # ]

    sat_pos = [
        [-1541460.9388363883, 30224149.692202177, 29498390.258974653],
        # [-17617438.292633787, 28844094.20427601, -25266876.988612313],
        [-12124036.663952267, 40274828.72201677, -862776.9444051579],
        [6391047.515815537, 34750078.60955605, 23829421.90263068],
        [-6994578.167874805, 41060743.01465158, 5779119.601933156],
    ]
    dists = [
        # 36628907.792815715,
        0.12220767656044551 * 299792458,
        # 40100030.486772105,
        36921766.37691232,
        37528162.75403043,
        36612052.519362174,
    ]
    # dists = [
    #     1.2651e+07,
    #     1.3002e+07,
    #     1.3551e+07,
    #     1.2681e+07
    # ]

    filepath = "/home/syml/Sources/bds/gnss-sdr/observables.mat"
    mat = get_mat(filepath)
    prange = get_avg_pseudorange(mat)

    # ans = simple_SPP_SVD([sat_pos1, sat_pos2, sat_pos3, sat_pos4], [prange[6.0], prange[7.0], prange[8.0], prange[9.0]])
    # ans = simple_SPP([sat_pos1, sat_pos2, sat_pos3, sat_pos4], [38453252, 36376413, 39565215, 37814234])
    ans = simple_SPP_SVD(sat_pos, dists)
    # ans = simple_SPP_SVD(sat_pos, dist)
    print(ans[0], ans[1], ans[2])
    print(ecef2lla(ans[0], ans[1], ans[2]))
