"""
Author: symlpigeon
Date: 2023-01-14 16:01:28
LastEditTime: 2023-01-14 16:43:56
LastEditors: symlpigeon
Description: 电离层校正模型，Klobuchar模型 
FilePath: /bds-Sim/bdsTx/satellite_info/ionosphere_corr_klobuchar.py
"""


from typing import List, Tuple

import numpy as np
from constants import *
from coordinate_system import ecef2lla
from time_system import utc2bds
from visible_satellite_searcher import calc_azimuth_angle, calc_elevation_angle


def get_iono_pierce_point(
    user_pos: Tuple[float, float, float], sat_pos: Tuple[float, float, float]
) -> Tuple[float, float]:
    """计算电离层穿刺点

    Args:
        user_pos (Tuple[float, float, float]): 用户所处位置，ECEF坐标系
        sat_pos (Tuple[float, float, float]): 卫星所处位置，ECEF坐标系
        curr_time (float): 当前时间， UTC time

    Returns:
        Tuple[float, float]: 电离层穿刺点的经纬度，单位：弧度
    """
    user_lon, user_lat, _ = ecef2lla(*user_pos)
    A = calc_azimuth_angle(user_pos, sat_pos)
    E = calc_elevation_angle(user_pos, sat_pos)
    psi = (
        np.pi / 2
        - E
        - np.arcsin(
            EARTH_RADIUS / (EARTH_RADIUS + IONOSPHERE_SINGLE_LAYER_ALTITUDE) * np.cos(E)
        )
    )
    lat_M = np.arcsin(
        np.sin(user_lat) * np.cos(psi) + np.cos(user_lat) * np.sin(psi) * np.cos(A)
    )
    lon_M = user_lon + np.arcsin((np.sin(psi) * np.sin(A)) / np.cos(lat_M))
    return lon_M, lat_M


def get_A2(lat_M: float, alpha: List[float]) -> float:
    """计算日间电离层延迟余弦曲线幅度A2

    Args:
        lat_M (float): 电离层穿刺点的纬度，单位：弧度
        alpha (List[float]): 模型参数

    Returns:
        float: 日间电离层延迟余弦曲线幅度A2
    """
    assert len(alpha) == 4, "Invalid Parameter Alpha for Klobuchar Model!"
    A2 = 0
    for i in range(4):
        A2 += alpha[i] * pow(np.cos(lat_M) / np.pi, i)
    if A2 >= 0:
        return A2
    return 0


def get_A4(lat_M: float, beta: List[float]) -> float:
    """计算余弦曲线周期A4

    Args:
        lat_M (float): 电离层穿刺点纬度，单位：弧度
        beta (List[float]): 模型参数

    Returns:
        float: 余弦曲线周期A4
    """
    assert len(beta) == 4, "Invalid Parameter Beta for Klobuchar Model!"
    A4 = 0
    for i in range(4):
        A4 += beta[i] * pow(np.cos(lat_M) / np.pi, i)
    if A4 > 172800:
        return 172800
    elif A4 < 72000:
        return 72000
    return A4


def get_preice_point_localtime(curr_time: float, lon_M: float) -> float:
    """计算电离层穿刺点地方时间

    Args:
        curr_time (float): 当前时间，UTC
        lon_M (float): 电离层穿刺点经度，单位：弧度

    Returns:
        float: 电离层穿刺点地方时间
    """
    _, t_E = utc2bds(curr_time)
    return (t_E + lon_M / np.pi * 43200) % 86400


def get_iono_vert_fix(pp_time: float, A2: float, A4: float) -> float:
    """计算电离层垂直改正数

    Args:
        pp_time (float): 电离层穿刺点当地时间，s
        A2 (float): A2
        A4 (float): A4

    Returns:
        float: 电离层垂直改正，单位？
    """
    if np.abs(pp_time - 50400) >= A4 / 4:
        return 5e-9
    return 5e-9 + A2 * np.cos(2 * np.pi * (pp_time - 50400) / A4)


def get_iono_delay(I_z: float, E: float) -> float:
    """利用电离层垂直改正I'_z计算电离层延迟（秒）

    Args:
        I_z (float): 电离层垂直改正
        E (float): 卫星高度角，单位弧度

    Returns:
        float: 电离层延迟，秒
    """
    return I_z / np.sqrt(
        1
        - pow(
            (EARTH_RADIUS / (EARTH_RADIUS + IONOSPHERE_SINGLE_LAYER_ALTITUDE))
            * np.cos(E),
            2,
        )
    )


def get_iono_delay_klobuchar(
    user_pos: Tuple[float, float, float],
    sat_pos: Tuple[float, float, float],
    curr_time: float,
    alpha: List[float],
    beta: List[float],
) -> float:
    """计算Klobuchar模型下的电离层延迟

    Args:
        user_pos (Tuple[float, float, float]): 用户所在的位置，ECEF坐标系下的坐标，单位：米
        sat_pos (Tuple[float, float, float]): 卫星所在的位置，ECEF坐标系下的坐标，单位：米
        curr_time (float): 当前时间，UTC，单位：秒
        alpha (List[float]): 电离层模型参数
        beta (List[float]): 电离层模型参数

    Returns:
        float: 电离层延迟，秒
    """
    # 计算卫星高度角
    E = calc_elevation_angle(user_pos, sat_pos)
    # 计算电离层穿刺点位置
    lon_M, lat_M = get_iono_pierce_point(user_pos, sat_pos)
    # 计算电离层穿刺点本地时间
    pp_time = get_preice_point_localtime(curr_time, lon_M)
    # 计算A2和A4
    A2, A4 = get_A2(lat_M, alpha), get_A4(lat_M, beta)
    # 计算电离层垂直改正
    I_z = get_iono_vert_fix(pp_time, A2, A4)
    # 计算电离层延迟
    delay = get_iono_delay(I_z, E)

    return delay


if __name__ == "__main__":
    import sys
    import time

    from coordinate_system import lla2ecef

    alpha = [
                3.353e-08,
                1.49e-07,
                -1.43e-06,
                2.205e-06
            ]
    beta = [
                124900.0,
                -32770.0,
                -720900.0,
                1311000.0
            ]
    user_pos = lla2ecef(120, 30, 0)
    sat_pos = 13515983.005496845, 10990355.209924806, 21780086.766416024
    curr_time = time.time()
    carrier_freq = 1575.42e6

    print(get_iono_delay_klobuchar(user_pos, sat_pos, curr_time, alpha, beta))