"""
Author: symlpigeon
Date: 2022-11-09 10:56:16
LastEditTime: 2022-11-09 12:08:34
LastEditors: symlpigeon
Description: 偏近点角的迭代计算
FilePath: /sim_bds/python/satellite_info/eccentric_anomaly.py
"""

import numpy as np


def calculate_eccentric_anomaly(eccentricity: float, mean_anomaly: float) -> float:
    """迭代法求解开普勒方程，计算偏近点角

    Args:
        eccentricity (float): 离心率
        mean_anomaly (float): 平近点角

    Returns:
        float: 偏近点角
    """
    # 迭代计算
    E = 0
    while True:
        E0 = E
        E = mean_anomaly + eccentricity * np.sin(E0)
        if np.abs(E - E0) < 0.001:
            break
    return E
