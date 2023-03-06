"""
Author: symlpigeon
Date: 2022-11-09 14:12:40
LastEditTime: 2022-11-24 09:44:40
LastEditors: symlpigeon
Description: 伪距计算
FilePath: /bds-Sim/bdsTx/satellite_info/pseudorange.py
"""

import json
import logging
from typing import Tuple

import numpy as np

from .constants import *
from .eccentric_anomaly import calculate_eccentric_anomaly
from .ionosphere.bdgim_non_broadcast_coefficients import (
    BDGIM_NON_BROADCAST_COEFFICIENTS,
)
from .ionosphere_corr_bdgim import get_iono_delay_bdgim
from .ionosphere_corr_klobuchar import get_iono_delay_klobuchar
from .position_calculate_by_ephemeris import get_stellite_position_by_ephemeris
from .time_system import utc2bds


def get_space_geometry_distance(
    rx_pos: Tuple[float, float, float], sat_pos: Tuple[float, float, float]
) -> float:
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


def get_clock_bias(
    a0: float, a1: float, a2: float, refer_time: float, curr_time: float
) -> float:
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
            return 0
    if ephemeris["support_type"] & 0b10 != 0:
        # 使用B1C/B2A星历
        A_0 = A_ref - ephemeris["deltaA"]
        # 计算长半轴
        A_0 += ephemeris["A_DOT"] * t_k
    else:
        A_0 = pow(ephemeris["sqrtA"], 2)
    sqrtA = np.sqrt(A_0)
    # 计算参考时刻平均角速度
    n_0 = np.sqrt(GEOCENTRIC_GRAVITATIONAL_CONSTANT / np.power(A_0, 3))
    if ephemeris["support_type"] & 0b10 != 0: # 使用B1C/B2A星历
        # 计算平均角速度偏差
        Delta_n_A = ephemeris["delta_n0"] + ephemeris["delta_n0_dot"] * 0.5 * t_k
        # 计算改正后的平均角速度
        n_A = n_0 + Delta_n_A
    else: # 使用B1I/B3I星历
        n_A = n_0 + ephemeris["delta_n0"]
    # 计算平近点角
    M_k = ephemeris["M0"] + n_A * t_k
    # 迭代计算偏近点角
    E_k = calculate_eccentric_anomaly(ephemeris["e"], M_k)
    return RELATIVITY_CONSTANT * e * sqrtA * np.sin(E_k)


def get_pseudo_range_impl(
    ephemeris: dict,
    iono_data: dict,
    carrier_freq: float,
    rx_pos: Tuple[float, float, float],
    curr_time: float,
    iono_corr_model: str = "bdgim"
) -> float:
    """计算伪距

    Args:
        ephemeris (dict): 星历文件
        rx_pos (Tuple[float, float, float]): 接收机位置
        curr_time (float): 当前时刻 UTC

    Returns:
        float: 伪距
    """
    # 计算卫星钟差
    clock_bias = get_clock_bias(
        ephemeris["a0"], ephemeris["a1"], ephemeris["a2"], ephemeris["toc"], curr_time
    )
    # 计算相对论修正
    relativity_corr = get_relativity_corr(ephemeris, curr_time)
    # 计算卫星位置
    sat_pos = get_stellite_position_by_ephemeris(ephemeris, curr_time)
    # 计算空间几何距离
    space_geometry_distance = get_space_geometry_distance(rx_pos, sat_pos)
    # 电离层延迟
    if iono_corr_model == "bdgim":
        iono_non_broadcast = iono_data["iono_non_broadcast"]
        iono_corr = iono_data["iono_corr"]
        iono_delay = get_iono_delay_bdgim(
            rx_pos, sat_pos, iono_non_broadcast, iono_corr, curr_time, carrier_freq
        )
        # 计算码伪距
        code_rho = (
            (space_geometry_distance + iono_delay) / LIGHT_SPEED
            + clock_bias
            + relativity_corr
        )
    elif iono_corr_model == "klobuchar":
        iono_corr = iono_data["iono_corr"]
        alpha = iono_corr["alpha"]
        beta = iono_corr["beta"]
        iono_delay = get_iono_delay_klobuchar(rx_pos, sat_pos, curr_time, alpha, beta)
        code_rho = space_geometry_distance / LIGHT_SPEED + clock_bias + relativity_corr + iono_delay
    else:
        # Invalid Iono Correction Model
        logging.error(f"Invalid Iono Correction Model: {iono_corr_model}")
        code_rho = space_geometry_distance / LIGHT_SPEED + clock_bias + relativity_corr
    return code_rho





def get_pseudo_range(
    ephemeris: dict,
    iono_data: dict | list,
    carrier_freq: float,
    rx_pos: Tuple[float, float, float],
    curr_time: float,
    iono_corr_model: str = "bdgim"
) -> float:
    """_summary_

    Args:
        ephemeris (dict): _description_
        iono_data (dict | list): _description_
        carrier_freq (float): _description_
        rx_pos (Tuple[float, float, float]): _description_
        curr_time (float): _description_
        iono_corr_model (str, optional): _description_. Defaults to "bdgim".

    Returns:
        float: _description_
    """
    iono = {
        "iono_corr": iono_data,
        "iono_non_broadcast": BDGIM_NON_BROADCAST_COEFFICIENTS
    }
    return get_pseudo_range_impl(ephemeris, iono, carrier_freq, rx_pos, curr_time, iono_corr_model)