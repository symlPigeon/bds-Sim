'''
Author: symlPigeon 2163953074@qq.com
Date: 2023-02-06 18:39:47
LastEditTime: 2023-04-13 15:33:41
LastEditors: symlPigeon 2163953074@qq.com
Description: 可见星搜寻
FilePath: /bds-Sim/bdsTx/satellite_info/visible_satellite_searcher.py
'''


from typing import Dict, Tuple

import numpy as np

from bdsTx.satellite_info.coordinate_system import ecef2enu, lla2ecef
from bdsTx.satellite_info.position_calculate_by_ephemeris import (
    get_satellite_position_by_ephemeris,
)
from bdsTx.satellite_info.time_system import get_closest_timestamp


def calc_elevation_angle(
    rx_pos: Tuple[float, float, float], sat_pos: Tuple[float, float, float]
) -> float:
    """计算卫星的仰角

    Args:
        rx_pos (Tuple[float, float, float]): 接收机位置,ECEF
        sat_pos (Tuple[float, float, float]): 卫星位置,ECEF

    Returns:
        float: 仰角, Degree
    """
    rx_x, rx_y, rx_z = rx_pos
    sat_x, sat_y, sat_z = sat_pos
    sat_pos_enu = ecef2enu(rx_x, rx_y, rx_z, sat_x, sat_y, sat_z)
    return np.arcsin(sat_pos_enu[2] / np.linalg.norm(sat_pos_enu)) * 180 / np.pi


def calc_azimuth_angle(
    rx_pos: Tuple[float, float, float], sat_pos: Tuple[float, float, float]
) -> float:
    """计算方位角

    Args:
        rx_pos (Tuple[float, float, float]): 接收机位置
        sat_pos (Tuple[float, float, float]): 卫星位置

    Returns:
        float: 方位角, Degree
    """
    rx_x, rx_y, rx_z = rx_pos
    sat_x, sat_y, sat_z = sat_pos
    sat_pos_enu = ecef2enu(rx_x, rx_y, rx_z, sat_x, sat_y, sat_z)
    return np.arctan2(sat_pos_enu[0], sat_pos_enu[1]) * 180 / np.pi


def get_visible_satellite(
    ephemeris: dict,
    rx_pos: Tuple[float, float, float],
    curr_time: float,
    threshold: float = 10.0,
) -> Dict[int, Tuple[float, dict]]:
    """获取可见卫星

    Args:
        ephemeris (dict): 卫星星历文件，整个文件的内容一起扔进来吧
        rx_pos (Tuple[float, float, float]): 卫星的位置，LLH
        curr_time (float): 当前的时间，UTC时间戳就行了
        threshold (float): 一个可见星仰角的阈值，就先设置为10吧

    Returns:
        Dict[int, Tuple[float, dict]]: 返回一个可见卫星的PRN和仰角、星历的对应字典
    """
    visible_sat = {}
    for prn in ephemeris:
        i_prn = int(prn)
        time_keys = list(ephemeris[prn].keys())
        closest_time = get_closest_timestamp(time_keys, curr_time)
        ecef_rx_pos = lla2ecef(*rx_pos)
        ecef_sat_pos = get_satellite_position_by_ephemeris(
            ephemeris[prn][closest_time], curr_time
        )
        elevation = calc_elevation_angle(ecef_rx_pos, ecef_sat_pos)
        if elevation > threshold:
            visible_sat[i_prn] = (elevation, ephemeris[prn][closest_time])
    return visible_sat


if __name__ == "__main__":
    import json
    import sys

    from coordinate_system import ecef2lla, lla2ecef

    eph_file = sys.argv[1]
    with open(eph_file, "r") as f:
        ephemeris = json.load(f)
    rx_pos = (108.8284, 34.1230, 0)

    import calendar
    import time

    curr_time = calendar.timegm((2023, 4, 13, 15, 26, 20))
    visible_satellite = get_visible_satellite(ephemeris, rx_pos, curr_time)
    print(visible_satellite.keys())

    B, L, H = [], [], []
    tags = []
    pos = []
    for key in visible_satellite:
        closest_time = get_closest_timestamp(
            ephemeris["{:02d}".format(key)].keys(), curr_time
        )
        x, y, z = get_satellite_position_by_ephemeris(
            ephemeris["{:02d}".format(key)][closest_time], curr_time
        )
        print(x, y, z)
        l, b, h = ecef2lla(x, y, z)
        E, A = calc_elevation_angle(rx_pos, (x, y, z)), calc_azimuth_angle(
            rx_pos, (x, y, z)
        )
        A = A if A > 0 else A + 360
        B.append(b)
        L.append(l)
        H.append(h)
        tags.append(f"{key}({E},{A})")
    for b, l in zip(B, L):
        print(l, b)
    import matplotlib.pyplot as plt
    from mpl_toolkits.basemap import Basemap

    m = Basemap(projection="ortho", lat_0=rx_pos[1], lon_0=rx_pos[0])
    m.drawmapboundary(fill_color="aqua")
    m.fillcontinents(color="yellow", lake_color="aqua")
    m.drawcoastlines()
    m.drawcountries()
    m.drawmapboundary(fill_color="aqua")
    x, y = m(L, B)
    m.scatter(x, y, marker="o", color="r")
    for tag, x, y in zip(tags, x, y):
        plt.text(x, y, tag)
    plt.show()
