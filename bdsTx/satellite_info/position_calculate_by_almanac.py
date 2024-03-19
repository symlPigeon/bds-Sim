"""
Author: symlpigeon
Date: 2022-11-08 15:48:10
LastEditTime: 2023-01-16 15:15:01
LastEditors: symlpigeon
Description: 用来通过星历数据计算卫星的位置
FilePath: /bds-Sim/bdsTx/satellite_info/position_calculate_by_almanac.py
"""

import json
from typing import Tuple

import numpy as np

from .constants import *
from .detect_sat_type import detect_sat_type
from .eccentric_anomaly import calculate_eccentric_anomaly
from .time_system import utc2bds


def get_satellite_position_by_almanac(
    almanac: dict, curr_time: float, sat_type: int
) -> Tuple[float, float, float]:
    """从历书文件获取卫星位置

    Args:
        almanac (dict): 历书数据
        curr_time (float): 当前UTC时间

    Returns:
        Tuple[float, float, float]: ECEF坐标系下卫星位置
    """

    t_a = almanac["TimeOfApplicability"]
    sqrt_a = almanac["SquareRootOfSemiMajorAxis"]
    e = almanac["Eccentricity"]
    M0 = almanac["MeanAnomaly"]
    omega = almanac["ArgumentOfPerigee"]
    delta_i = almanac["OrbitalInclination"]
    Omega0 = almanac["RightAscenAtWeek"]
    Omega_dot = almanac["RateOfRightAscension"]
    i0 = 0.3 * np.pi
    # 计算长半轴
    A = np.power(sqrt_a, 2)
    # 计算平均运动角速度
    n0 = np.sqrt(GEOCENTRIC_GRAVITATIONAL_CONSTANT / np.power(A, 3))
    # 计算与参考时刻的时间差
    bds_time = utc2bds(curr_time)
    t_k = bds_time[1] - t_a
    if t_k > 302400:
        t_k -= 604800
    elif t_k < -302400:
        t_k += 604800
    # 计算平近点角
    M_k = M0 + n0 * t_k
    # 计算偏近点角
    E_k = calculate_eccentric_anomaly(e, M_k)
    # 计算真近点角
    v_k = np.arctan2(np.sqrt((1 + e) / (1 - e)) * np.sin(E_k), (np.cos(E_k) - e))
    # 计算纬度幅角
    phi_k = v_k + omega
    # 计算径向距离
    r_k = A * (1 - e * np.cos(E_k))
    # 计算卫星位置
    x_k = r_k * np.cos(phi_k)
    y_k = r_k * np.sin(phi_k)
    # 计算改正后的升交点经度
    Omega_k = (
        Omega0 + (Omega_dot - EARTH_ROTATION_RATE) * t_k - EARTH_ROTATION_RATE * t_a
    )
    # 计算参考时刻轨道倾角
    if sat_type == 1:  # GEO
        i_k = i0
    else:
        i_k = i0 + np.pi * 0.3
    # 计算ECEF坐标
    X_k = x_k * np.cos(Omega_k) - y_k * np.cos(i_k) * np.sin(Omega_k)
    Y_k = x_k * np.sin(Omega_k) + y_k * np.cos(i_k) * np.cos(Omega_k)
    Z_k = y_k * np.sin(i_k)
    return X_k, Y_k, Z_k


if __name__ == "__main__":
    import calendar
    import os
    import sys

    import matplotlib.pyplot as plt
    from mpl_toolkits.basemap import Basemap

    from .coordinate_system import ecef2lla

    filepath = sys.argv[1]

    with open(filepath, "r") as f:
        data = f.read()
    almanac = json.loads(data)
    B = []
    L = []
    H = []
    tags = []
    for ids in almanac:
        stellite = almanac[ids]
        sat_type = detect_sat_type(ids)
        x, y, z = get_satellite_position_by_almanac(
            stellite, float(calendar.timegm((2023, 1, 16, 6, 0, 0))), sat_type
        )
        b, l, h = ecef2lla(x, y, z)
        B.append(b)
        L.append(l)
        H.append(h)
        print(b, l, h, ids)
        tags.append(ids)
    world_map = Basemap(
        projection="cea",
        llcrnrlat=-90,
        urcrnrlat=90,
        llcrnrlon=-180,
        urcrnrlon=180,
        resolution="c",
    )
    world_map.drawcoastlines()
    world_map.fillcontinents(color="coral", lake_color="aqua")
    # draw parallels and meridians.
    world_map.drawparallels(np.arange(-90.0, 91.0, 30.0))
    world_map.drawmeridians(np.arange(-180.0, 181.0, 60.0))
    world_map.drawmapboundary(fill_color="aqua")
    x, y = world_map(B, L)
    plt.scatter(x, y)
    for i in range(len(tags)):
        plt.annotate(
            tags[i],
            (x[i], y[i]),
        )
    plt.show()
