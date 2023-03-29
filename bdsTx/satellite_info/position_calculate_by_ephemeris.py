"""
Author: symlpigeon
Date: 2022-11-08 23:02:16
LastEditTime: 2022-11-09 22:02:21
LastEditors: symlpigeon
Description: 通过星历文件计算卫星位置
FilePath: /sim_bds/python/satellite_info/position_calculate_by_ephemeris.py
"""

import logging
from typing import Tuple

import numpy as np

from bdsTx.satellite_info.constants import *
from bdsTx.satellite_info.eccentric_anomaly import calculate_eccentric_anomaly
from bdsTx.satellite_info.time_system import utc2bds


def get_satellite_position_by_ephemeris(
    ephemeris: dict, curr_time: float
) -> Tuple[float, float, float]:
    """返回ECEF坐标系下的卫星位置

    Args:
        ephemeris (dict): 卫星对应的星历数据
        curr_time (float): 当前UTC时间

    Returns:
        Tuple[float, float, float]: ECEF坐标系下的卫星位置
    """
    # 与参考时刻的时间差
    bdt_curr_time = utc2bds(curr_time)
    t_k = bdt_curr_time[1] - ephemeris["Toe"]
    if t_k > 302400:
        t_k -= 604800
    elif t_k < -302400:
        t_k += 604800
    # 计算参考时刻长半轴
    match ephemeris["sat_type"]:
        case 1:  # GEO
            A_ref = GEO_SEMI_MAJOR_AXIS
        case 0b10:  # IGSO
            A_ref = IGSO_SEMI_MAJOR_AXIS
        case 0b11:  # MEO
            A_ref = MEO_SEMI_MAJOR_AXIS
        case _:
            logging.error(f"Unknown Satellite Type: {ephemeris['sat_type']}")
            return 0, 0, 0
    if ephemeris["support_type"] & 0b10 != 0: # use B1C/B2A
        A_0 = A_ref - ephemeris["deltaA"]
        # 计算长半轴
        A_0 += ephemeris["A_DOT"] * t_k
    else: # use B1I/B3I
        A_0 = pow(ephemeris["sqrtA"], 2)
    # 计算参考时刻平均角速度
    n_0 = np.sqrt(GEOCENTRIC_GRAVITATIONAL_CONSTANT / np.power(A_0, 3))
    if ephemeris["support_type"] & 0b10 != 0: # use B1C/B2A
        # 计算平均角速度偏差
        Delta_n_A = ephemeris["delta_n0"] + ephemeris["delta_n0_dot"] * 0.5 * t_k
        # 计算改正后的平均角速度
        n_A = n_0 + Delta_n_A
    else: # use B1I/B3I
        n_A = n_0 + ephemeris["delta_n0"]
    # 计算平近点角
    M_k = ephemeris["M0"] + n_A * t_k
    # 迭代计算偏近点角
    E_k = calculate_eccentric_anomaly(ephemeris["e"], M_k)
    # 计算真近点角
    v_k = np.arctan2(
        np.sqrt(1 - np.power(ephemeris["e"], 2)) * np.sin(E_k),
        np.cos(E_k) - ephemeris["e"],
    )
    # 计算纬度幅角
    phi_k = v_k + ephemeris["omega"]
    # 计算改正项
    delta_u_k = ephemeris["Cus"] * np.sin(2 * phi_k) + ephemeris["Cuc"] * np.cos(
        2 * phi_k
    )
    delta_r_k = ephemeris["Crs"] * np.sin(2 * phi_k) + ephemeris["Crc"] * np.cos(
        2 * phi_k
    )
    delta_i_k = ephemeris["Cis"] * np.sin(2 * phi_k) + ephemeris["Cic"] * np.cos(
        2 * phi_k
    )
    # 计算改正后的纬度幅角
    u_k = phi_k + delta_u_k
    # 计算改正后的径向距离
    r_k = A_0 * (1 - ephemeris["e"] * np.cos(E_k)) + delta_r_k
    # 计算改正后的轨道倾角
    i_k = ephemeris["i0"] + ephemeris["IDOT"] * t_k + delta_i_k
    # 计算卫星在轨道平面内的坐标
    x_k = r_k * np.cos(u_k)
    y_k = r_k * np.sin(u_k)

    if ephemeris["sat_type"] == 0b10 or ephemeris["sat_type"] == 0b11:
        # 针对MEO和IGSO的算法
        # 计算改正后的升交点经度
        Omega_k = (
            ephemeris["Omega0"]
            + (ephemeris["Omega_dot"] - EARTH_ROTATION_RATE) * t_k
            - EARTH_ROTATION_RATE * ephemeris["Toe"]
        )
        # 计算卫星在ECEF坐标系下的坐标
        X_k = x_k * np.cos(Omega_k) - y_k * np.cos(i_k) * np.sin(Omega_k)
        Y_k = x_k * np.sin(Omega_k) + y_k * np.cos(i_k) * np.cos(Omega_k)
        Z_k = y_k * np.sin(i_k)
    else:
        # 针对GEO的算法
        # 惯性系中历元升交点经度
        Omega_k = (
            ephemeris["Omega0"]
            + ephemeris["Omega_dot"] * t_k
            - EARTH_ROTATION_RATE * ephemeris["Toe"]
        )
        # GEO卫星在自定义坐标系中的坐标
        X_GK = x_k * np.cos(Omega_k) - y_k * np.cos(i_k) * np.sin(Omega_k)
        Y_GK = x_k * np.sin(Omega_k) + y_k * np.cos(i_k) * np.cos(Omega_k)
        Z_GK = y_k * np.sin(i_k)
        rz_arg = ephemeris["Omega_dot"] * t_k
        RX = np.array(
            [
                [1, 0, 0],
                [0, np.cos(rz_arg), np.sin(rz_arg)],
                [0, -np.sin(rz_arg), np.cos(rz_arg)],
            ]
        )
        RZ = np.array(
            [
                [np.cos(5 * np.pi / 180), np.sin(5 * np.pi / 180), 0],
                [-np.sin(5 * np.pi / 180), np.cos(5 * np.pi / 180), 0],
                [0, 0, 1],
            ]
        )
        coor = RZ @ RX @ np.array([X_GK, Y_GK, Z_GK]).T
        X_k, Y_k, Z_k = coor

    return X_k, Y_k, Z_k


if __name__ == "__main__":
    ref_time = "2023-01-14_00:00:00"
    import calendar
    import json
    import sys

    from coordinate_system import ecef2lla

    filepath = sys.argv[1]
    test_time = calendar.timegm((2023, 3, 14, 12, 0, 0))
    with open(filepath, "r") as f:
        ephemeris = json.load(f)
    B = []
    L = []
    H = []
    tags = []
    for stellite_id in ephemeris:
        eph = ephemeris[stellite_id][ref_time]
        x, y, z = get_satellite_position_by_ephemeris(eph, test_time)
        print(x, y, z)
        l, b, h = ecef2lla(x, y, z)
        B.append(b)
        L.append(l)
        H.append(h)
        tags.append(stellite_id)
    import matplotlib.pyplot as plt
    from mpl_toolkits.basemap import Basemap

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
    x, y = world_map(L, B)
    plt.scatter(x, y, c="green")
    for i in range(len(tags)):
        plt.annotate(
            tags[i],
            (x[i], y[i]),
        )
    plt.show()
