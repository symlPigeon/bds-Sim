'''
Author: symlpigeon
Date: 2022-11-09 14:12:40
LastEditTime: 2022-11-23 16:06:43
LastEditors: symlpigeon
Description: 伪距计算
FilePath: /bds-Sim/bdsTx/satellite_info/pseudorange.py
'''

import logging
from typing import Tuple

import numpy as np
from constants import *
from eccentric_anomaly import calculate_eccentric_anomaly
from ionosphere_corr import get_iono_delay
from position_calculate_by_ephemeris import get_stellite_position_by_ephemeris
from time_system import utc2bds


def get_space_geometry_distance(rx_pos: Tuple[float, float, float], sat_pos: Tuple[float, float, float]) -> float:
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


def get_clock_bias(a0: float, a1: float, a2: float, refer_time: float, curr_time: float) -> float:
    """计算卫星钟差（未包含相对论修正）

    Args:
        a0 (float): 卫星钟差
        a1 (float): 卫星钟漂
        a2 (float): 卫星钟漂速率
        refer_time (float): 参考时刻
        curr_time (float): 当前时刻 UTC

    Returns:
        float: 卫星钟差（未包含相对论修正）
    """
    _, curr_time = utc2bds(curr_time)
    return a0 + a1 * (curr_time - refer_time) + a2 * ((curr_time - refer_time) ** 2)


def get_relativity_corr(ephemeris: dict, curr_time: float) -> float:
    """计算相对论效应修正

    Args:
        ephemeris (dict): 星历文件
        
    Returns:
        float: 相对论效应修正
    """
    e = ephemeris["e"]
    sqrtA = ephemeris["deltaA/sqrtA"]
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
            logging.warn("GEO Stellite Position Prediction is not implemented yet")
            return 0
        case 0b10:  # IGSO
            A_ref = IGSO_SEMI_MAJOR_AXIS
        case 0b11:  # MEO
            A_ref = MEO_SEMI_MAJOR_AXIS
        case _:
            logging.error(f"Unknown Satellite Type: {ephemeris['sat_type']}")
            return 0
    A_0 = A_ref - ephemeris["deltaA/sqrtA"]
    # 计算长半轴
    A_k = A_0 + ephemeris["A_DOT/EMPTY"] * t_k
    # 计算参考时刻平均角速度
    n_0 = np.sqrt(GEOCENTRIC_GRAVITATIONAL_CONSTANT / np.power(A_0, 3))
    # 计算平均角速度偏差
    Delta_n_A = ephemeris["delta_n0"] + ephemeris["delta_n0_dot"] * 0.5 * t_k
    # 计算改正后的平均角速度
    n_A = n_0 + Delta_n_A
    # 计算平近点角
    M_k = ephemeris["M0"] + n_A * t_k
    # 迭代计算偏近点角
    E_k = calculate_eccentric_anomaly(ephemeris["e"], M_k)
    return RELATIVITY_CONSTANT * e * sqrtA * np.sin(E_k)


def get_pesudo_range(ephemeris: dict, iono_non_broadcast: dict, iono_corr: list, carrier_freq: float, rx_pos: Tuple[float, float, float], curr_time: float) -> Tuple[float, float]:
    """计算伪距

    Args:
        ephemeris (dict): 星历文件
        rx_pos (Tuple[float, float, float]): 接收机位置
        curr_time (float): 当前时刻 UTC

    Returns:
        Tuple[float]: 载波伪距，码字伪距
    """
    # 计算卫星钟差
    clock_bias = get_clock_bias(ephemeris["a0"], ephemeris["a1"], ephemeris["a2"], ephemeris["Toc"], curr_time)
    # 计算相对论修正
    relativity_corr = get_relativity_corr(ephemeris, curr_time)
    # 计算卫星位置
    sat_pos = get_stellite_position_by_ephemeris(ephemeris, curr_time)
    # 计算空间几何距离
    space_geometry_distance = get_space_geometry_distance(rx_pos, sat_pos)
    # 电离层延迟
    iono_delay = get_iono_delay(rx_pos, sat_pos, iono_non_broadcast, iono_corr, curr_time, carrier_freq)
    # 计算载波伪距
    carri_rho = (space_geometry_distance + iono_delay) / LIGHT_SPEED + clock_bias + relativity_corr
    # 计算码伪距
    code_rho = (space_geometry_distance - iono_delay) / LIGHT_SPEED + clock_bias + relativity_corr
    return carri_rho, code_rho