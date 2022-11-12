"""
Author: symlpigeon
Date: 2022-11-09 14:29:47
LastEditTime: 2022-11-09 23:11:41
LastEditors: symlpigeon
Description: 可见星搜寻
FilePath: /sim_bds/python/satellite_info/visible_satellite_searcher.py
"""

from typing import List, Tuple
import numpy as np

from coordinate_system import ecef2enu
from position_calculate_by_ephemeris import get_stellite_position_by_ephemeris


def calc_elevation_angle(
    rx_pos: Tuple[float, float, float], sat_pos: Tuple[float, float, float]
) -> float:
    """计算卫星的仰角

    Args:
        rx_pos (Tuple[float, float, float]): 接收机位置,ECEF
        sat_pos (Tuple[float, float, float]): 卫星位置,ECEF

    Returns:
        float: 仰角
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
        float: 方位角
    """
    rx_x, rx_y, rx_z = rx_pos
    sat_x, sat_y, sat_z = sat_pos
    sat_pos_enu = ecef2enu(rx_x, rx_y, rx_z, sat_x, sat_y, sat_z)
    return np.arctan2(sat_pos_enu[0], sat_pos_enu[1]) * 180 / np.pi


def get_visible_satellite(
    ephemeris: dict,
    rx_pos: Tuple[float, float, float],
    curr_time: float,
    threshold: float = 10,
) -> dict:
    """获取可见卫星

    Args:
        ephemeris (List[dict]): 卫星星历
        rx_pos (Tuple[float, float, float]): 接收机位置
        curr (float): 当前UTC时间
        threshold (float, optional): 仰角阈值. Defaults to 10.

    Returns:
        List[dict]: 可见卫星的星历
    """
    visible_satellite = {}
    for eph in ephemeris:
        # 选择最新的一个版本
        time_keys = list(ephemeris[eph].keys())
        time_keys.sort()
        time_index = time_keys[-1]
        sat_pos = get_stellite_position_by_ephemeris(
            ephemeris[eph][time_index], curr_time
        )
        if calc_elevation_angle(rx_pos, sat_pos) > threshold:
            visible_satellite[eph] = ephemeris[eph][time_index]
    return visible_satellite


if __name__ == "__main__":
    import sys
    import json
    from coordinate_system import lla2ecef, ecef2lla

    eph_file = sys.argv[1]
    with open(eph_file, "r") as f:
        ephemeris = json.load(f)
    rx_pos_blh = (108, 34, 0)
    rx_pos = lla2ecef(*rx_pos_blh)

    import time

    curr_time = time.time()
    visible_satellite = get_visible_satellite(ephemeris, rx_pos, curr_time)
    print(visible_satellite.keys())

    B, L, H = [], [], []
    tags = []
    pos = []
    for eph in visible_satellite:
        x, y, z = get_stellite_position_by_ephemeris(visible_satellite[eph], curr_time)
        print(x, y, z)
        l, b, h = ecef2lla(x, y, z)
        E, A = calc_elevation_angle(rx_pos, (x, y, z)), calc_azimuth_angle(
            rx_pos, (x, y, z)
        )
        A = A if A > 0 else A + 360
        B.append(b)
        L.append(l)
        H.append(h)
        tags.append(f"{eph}({E},{A})")
    for b, l in zip(B, L):
        print(l, b)
    import matplotlib.pyplot as plt
    from mpl_toolkits.basemap import Basemap

    m = Basemap(projection="ortho", lat_0=rx_pos_blh[1], lon_0=rx_pos_blh[0])
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
