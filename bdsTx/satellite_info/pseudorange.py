'''
Author: symlpigeon
Date: 2022-11-09 14:12:40
LastEditTime: 2022-11-09 16:42:50
LastEditors: symlpigeon
Description: 伪距计算
FilePath: /sim_bds/python/satellite_info/pseudorange.py
'''

import numpy as np
from typing import Tuple


def space_geometry_distance(rx_pos: Tuple[float, float, float], sat_pos: Tuple[float, float, float]) -> float:
    """计算空间几何距离

    Args:
        rx_pos (Tuple[float, float, float]): 接收机位置
        sat_pos (Tuple[float, float, float]): 卫星位置

    Returns:
        float: 空间几何距离
    """
    rx_x, rx_y, rx_z = rx_pos
    sat_x, sat_y, sat_z = sat_pos
    return np.sqrt((rx_x - sat_x) ** 2 + (rx_y - sat_y) ** 2 + (rx_z - sat_z) ** 2)
