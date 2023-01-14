"""
Author: symlpigeon
Date: 2022-11-09 16:43:46
LastEditTime: 2022-11-09 22:05:35
LastEditors: symlpigeon
Description: 电离层参数修正
FilePath: /sim_bds/python/satellite_info/ionosphere_corr.py
"""

import json
import math
from typing import Annotated, List, Tuple

import numpy as np
from constants import *
from coordinate_system import ecef2lla
from time_system import mjd2mdj_odd_hour, utc2mjd
from visible_satellite_searcher import calc_azimuth_angle, calc_elevation_angle

_N_I = [0, 1, 1, 1, 2, 2, 2, 2, 2]
_M_i = [0, 0, 1, -1, 0, 1, -1, 2, -2]


def get_solar_mean_longitude(mjd: float) -> float:
    """计算平太阳地理经度, 单位: 弧度

    Args:
        mjd (float): 需要计算的日期,儒略日

    Returns:
        float: 平太阳地理经度S_lon
    """
    return np.pi * (1 - 2 * (mjd - int(mjd)))


def get_iono_pierce_point(
    sat_position: Tuple[float, float, float],
    user_position: Tuple[float, float, float],
    curr_time: float,
) -> Tuple[float, float]:
    """获取电离层穿刺点

    Args:
        sat_position (Tuple[float,float,float]): 卫星位置,ECEF
        user_position (Tuple[float,float,float]): 接收机位置, ECEF
        curr_time (float): 当前时间, UTC

    Returns:
        float: 电离层穿刺点
    """
    lbd_u, phi_u, _ = map(np.rad2deg, ecef2lla(*user_position))
    elevation_angle = calc_elevation_angle(user_position, sat_position)
    azimuth_angle = calc_azimuth_angle(user_position, sat_position)
    elevation_angle = np.deg2rad(elevation_angle)
    azimuth_angle = np.deg2rad(azimuth_angle)
    # 计算地心张角
    Phi = (
        np.pi / 2
        - elevation_angle
        - np.arcsin(
            EARTH_RADIUS
            / (EARTH_RADIUS + IONOSPHERE_SINGLE_LAYER_ALTITUDE)
            * np.cos(elevation_angle)
        )
    )
    # 计算电离层穿刺点地理经纬度
    phi_g = np.arcsin(
        np.sin(phi_u) * np.cos(Phi)
        + np.cos(phi_u) * np.sin(Phi) * np.cos(azimuth_angle)
    )
    lbd_g = lbd_u + np.arctan2(
        np.sin(Phi) * np.sin(azimuth_angle) * np.cos(phi_u),
        np.cos(Phi) - np.sin(phi_u) * np.sin(phi_g),
    )
    # 转换到地固坐标系
    phi_m = np.arcsin(
        np.sin(GEO_MAGNETIC_NORTH_POLE_LATITUDE) * np.sin(phi_g)
        + np.cos(GEO_MAGNETIC_NORTH_POLE_LATITUDE)
        * np.cos(phi_g)
        * np.cos(lbd_g - GEO_MAGNETIC_NORTH_POLE_LONGITUDE)
    )
    lbd_m = np.arctan2(
        np.cos(phi_g)
        * np.sin(lbd_g - GEO_MAGNETIC_NORTH_POLE_LONGITUDE)
        * np.cos(phi_m),
        np.sin(phi_m) * np.sin(phi_m) - np.sin(phi_g),
    )
    # 转换到日固坐标系
    S_lon = get_solar_mean_longitude(utc2mjd(curr_time))
    phi_ = phi_m
    lbd_ = lbd_m + np.arctan2(
        np.sin(S_lon - lbd_m), np.sin(phi_m) * np.cos(S_lon - lbd_m)
    )
    return lbd_, phi_


def iono_regularize(n: int, m: int) -> float:
    """正则化函数

    Args:
        n (int): 阶
        m (int): 阶

    Returns:
        float: 函数值
    """
    delta_0m = 1 if m == 0 else 0
    return np.sqrt(
        math.factorial(n - m) * (2 * n - 1) * (2 - delta_0m) / math.factorial(n + m)
    )


def norm_legendre_func(n: int, m: int, sin_phi: float) -> float:
    """计算标准Legendre函数

    Args:
        n (int): _description_
        m (int): _description_
        sin_phi (float): _description_

    Returns:
        float: _description_
    """
    if n == 0 and m == 0:
        return 1
    if n == m:
        ans = 1
        for i in range(1, 2 * n + 1, 2):
            ans *= i
        return pow(1 - pow(sin_phi, 2), n / 2) * ans
    if n == m + 1:
        return sin_phi * (2 * m + 1) * norm_legendre_func(m, m, sin_phi)
    return (
        (2 * n - 1) * sin_phi * norm_legendre_func(n - 1, m, sin_phi)
        - (n + m - 1) * norm_legendre_func(n - 2, m, sin_phi)
    ) / (n - m)


def get_A_i(lbd: float, phi: float) -> Annotated[List[float], 9]:
    """电离层延迟的系数

    Args:
        lbd (float): 经度
        phi (float): 纬度

    Returns:
        Annotated[List[float], 3]: 系数值A1-A9
    """
    A_i = []
    for i in range(1, 10, 1):
        n = _N_I[i - 1]
        m = _M_i[i - 1]
        if m >= 0:
            A_i.append(norm_legendre_func(n, m, np.sin(phi)) * np.cos(m * lbd))
        else:
            A_i.append(norm_legendre_func(n, m, np.sin(phi)) * np.sin(-m * lbd))
    return A_i


def load_non_broadcast_coefficient(filepath: str) -> dict:
    """从文件中加载非播发系数

    Args:
        filepath (str): 文件路径

    Returns:
        dict: 非播发系数数据,见具体json文件
    """
    with open(filepath, "r") as f:
        data = json.load(f)
    return data


def get_beta_j(
    iono_non_broadcast_coeff: dict, curr_time: float
) -> Annotated[List[float], 17]:
    """计算参数beta_j

    Args:
        iono_non_broadcast_coeff (dict): 非播发系数json
        curr_time (float): 当前时间

    Returns:
        Annotated[List[float], 17]: 系数beta,17个
    """
    period = iono_non_broadcast_coeff["period"]
    coeff = iono_non_broadcast_coeff["coefficients"]
    curr_time = mjd2mdj_odd_hour(utc2mjd(curr_time))

    beta = []
    for j in range(17):
        beta_j = coeff[j][0]
        for k in range(1, 13):
            omega_k = 2 * np.pi / period[k - 1]
            a_kj = coeff[j][k * 2 - 1]
            b_kj = coeff[j][k * 2]
            beta_j += a_kj * np.cos(omega_k * curr_time) + b_kj * np.sin(
                omega_k * curr_time
            )
            beta.append(beta_j)
    return beta


def get_A0(
    iono_non_broadcast_coeff: dict, lbd: float, phi: float, curr_time: float
) -> float:
    """电离层延迟预报值A0

    Args:
        iono_non_broadcast_coeff (dict): 电离层非播发数据
        lbd (float): 经度
        phi (float): 纬度
        curr_time (float): 当前时间UTC

    Returns:
        float: 电离层延迟预报值A0
    """
    beta = get_beta_j(iono_non_broadcast_coeff, curr_time)
    B = []
    for j in range(17):
        nj, mj = iono_non_broadcast_coeff["n/m"][j]
        if mj >= 0:
            B.append(norm_legendre_func(nj, mj, np.sin(phi)) * np.cos(mj * lbd))
        else:
            B.append(norm_legendre_func(nj, mj, np.sin(phi)) * np.sin(-mj * lbd))

    A0 = 0
    for i in range(17):
        A0 += beta[i] * B[i]
    return A0


def get_IPP_VTEC(
    A0: float, alpha: Annotated[List[float], 9], A_i: Annotated[List[float], 9]
) -> float:
    """穿刺点处垂直方向电离层延迟

    Args:
        A0 (float): 电离层延迟预报系数
        alpha (float): BDGIM播发的系数
        A_i (float): 电离层延迟的参数

    Returns:
        float: 穿刺点处垂直方向的电离层延迟,单位TECu
    """
    VTEC = A0
    for i in range(9):
        VTEC += alpha[i] * A_i[i]
    return VTEC


def get_IPP_mapping_func(
    sat_position: Tuple[float, float, float], user_position: Tuple[float, float, float]
) -> float:
    E = np.deg2rad(calc_elevation_angle(user_position, sat_position))
    M_F = 1 / np.sqrt(
        1
        - pow(
            EARTH_RADIUS
            * np.cos(E)
            / (EARTH_RADIUS + IONOSPHERE_SINGLE_LAYER_ALTITUDE),
            2,
        )
    )
    return M_F


def get_iono_delay_bdgim(
    user_pos: Tuple[float, float, float],
    sat_pos: Tuple[float, float, float],
    iono_non_broadcast_coeff: dict,
    alpha: List[float],
    curr_time: float,
    carrier_freq: float,
) -> float:
    """计算电离层延迟改正值

    Args:
        user_pos (Tuple[float, float, float]): 用户位置, ECEF坐标系
        sat_pos (Tuple[float, float, float]): 卫星位置, ECEF坐标系
        iono_non_broadcast_coeff (dict): 电离层非播发数据
        alpha (List[float]): 播发的修正数据
        curr_time (float): 当前UTC时间
        carrier_freq (float): 载波频率

    Returns:
        float: 电离层延迟改正值,米
    """
    lbd_, phi_ = get_iono_pierce_point(sat_pos, user_pos, curr_time)
    A_i = get_A_i(lbd_, phi_)
    A0 = get_A0(iono_non_broadcast_coeff, lbd_, phi_, curr_time)
    VTEC = get_IPP_VTEC(A0, alpha, A_i)
    M_F = get_IPP_mapping_func(sat_pos, user_pos)

    return M_F * 40.28e16 / pow(carrier_freq, 2) * VTEC


if __name__ == "__main__":
    import sys
    import time

    from coordinate_system import lla2ecef

    filepath = sys.argv[1]
    iono_dict = load_non_broadcast_coefficient(filepath)

    alpha = [33.25, -3.625, 13.25, 8.25, -13.13, 1.125, -0.375, 3.5, -0.125]
    user_pos = lla2ecef(120, 30, 0)
    sat_pos = 13515983.005496845, 10990355.209924806, 21780086.766416024
    curr_time = time.time()
    carrier_freq = 1575.42e6

    print(get_iono_delay_bdgim(user_pos, sat_pos, iono_dict, alpha, curr_time, carrier_freq))
