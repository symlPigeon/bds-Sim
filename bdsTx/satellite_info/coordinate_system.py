"""
Author: symlpigeon
Date: 2022-11-08 18:15:47
LastEditTime: 2022-11-09 22:16:22
LastEditors: symlpigeon
Description: 坐标系互转
FilePath: /sim_bds/python/satellite_info/coordinate_system.py
"""

# Reference: https://en.wikipedia.org/wiki/Geographic_coordinate_conversion

from typing import Tuple

import numpy as np

from bdsTx.satellite_info.constants import *


def lla2ecef(L: float, B: float, H: float) -> Tuple[float, float, float]:
    """大地坐标系转地心地固坐标系

    Args:
        L (_type_): 经度
        B (_type_): 纬度
        H (_type_): 高程

    Returns:
        _type_: _description_
    """
    L = np.deg2rad(L)
    B = np.deg2rad(B)
    e2 = 1 - pow(WGS84_SEMI_MINOR_AXIS / WGS84_SEMI_MAJOR_AXIS, 2)
    N = WGS84_SEMI_MAJOR_AXIS / np.sqrt(1 - e2 * pow(np.sin(B), 2))
    x = (N + H) * np.cos(B) * np.cos(L)
    y = (N + H) * np.cos(B) * np.sin(L)
    z = (N * (1 - e2) + H) * np.sin(B)
    return x, y, z


def ecef2lla(x: float, y: float, z: float) -> Tuple[float, float, float]:
    """地固坐标系转大地坐标系

    Args:
        x (_type_): 指向本初子午线与赤道的交点为x轴正方向
        y (_type_): 东经90度与赤道交点为y轴正方向
        z (_type_): 指向北极点为z轴正方向

    Returns:
        _type_: 经度L, 纬度B, 高程H
    """
    # a = WGS84_SEMI_MAJOR_AXIS
    # b = WGS84_SEMI_MINOR_AXIS
    # e2 = 1 - (b / a) ** 2
    # p = np.sqrt(x**2 + y**2)
    # theta = np.arctan(z * a / (p * b))
    # L = np.arctan2(y, x)
    # B = np.arctan(
    #     (z + e2 / (1 - e2) * b * np.sin(theta) ** 3) / (p - e2 * a * np.cos(theta) ** 3)
    # )
    # N = a / np.sqrt(1 - e2 * np.sin(B) ** 2)
    # H = p / np.cos(B) - N
    # return np.rad2deg(L), np.rad2deg(B), H
    p = np.sqrt(pow(x, 2) + pow(y, 2))
    e2 = 1 - pow(WGS84_SEMI_MINOR_AXIS / WGS84_SEMI_MAJOR_AXIS, 2)
    e2_ = pow(WGS84_SEMI_MAJOR_AXIS / WGS84_SEMI_MINOR_AXIS, 2) - 1
    F = 54 * pow(WGS84_SEMI_MINOR_AXIS, 2) * pow(z, 2)
    G = (
        pow(p, 2)
        + (1 - e2) * pow(z, 2)
        - e2
        * (WGS84_SEMI_MAJOR_AXIS + WGS84_SEMI_MINOR_AXIS)
        * (WGS84_SEMI_MAJOR_AXIS - WGS84_SEMI_MINOR_AXIS)
    )
    c = pow(e2, 2) * F * pow(p, 2) / pow(G, 3)
    s = np.cbrt(1 + c + np.sqrt(pow(c, 2) + 2 * c))
    k = s + 1 + 1 / s
    P = F / (3 * pow(k, 2) * pow(G, 2))
    Q = np.sqrt(1 + 2 * pow(e2, 2) * P)
    r0 = (-P * e2 * p) / (1 + Q) + np.sqrt(
        0.5 * WGS84_SEMI_MAJOR_AXIS * WGS84_SEMI_MAJOR_AXIS * (1 + 1 / Q)
        - P * (1 - e2) * pow(z, 2) / (Q * (1 + Q))
        - 0.5 * P * pow(p, 2)
    )
    U = np.sqrt(pow(p - e2 * r0, 2) + pow(z, 2))
    V = np.sqrt(pow(p - e2 * r0, 2) + (1 - e2) * pow(z, 2))
    z0 = pow(WGS84_SEMI_MINOR_AXIS, 2) * z / (WGS84_SEMI_MAJOR_AXIS * V)
    H = U * (1 - pow(WGS84_SEMI_MINOR_AXIS, 2) / (WGS84_SEMI_MAJOR_AXIS * V))
    L = np.arctan2(y, x)
    B = np.arctan2(z + e2_ * z0, p)
    L = np.rad2deg(L)
    B = np.rad2deg(B)
    return L, B, H


def ecef2enu(
    xr: float, yr: float, zr: float, x: float, y: float, z: float
) -> Tuple[float, float, float]:
    """ECEF坐标系转ENU坐标系

    Args:
        xr (float): 接收机X坐标
        yr (float): 接收机Y坐标
        zr (float): 接收机Z坐标
        x (float): 卫星X坐标
        y (float): 卫星Y坐标
        z (float): 卫星Z坐标

    Returns:
        Tuple[float, float, float]: 卫星在ENU坐标系下的位置
    """
    lbd, phi, _ = ecef2lla(xr, yr, zr)
    lbd = np.deg2rad(lbd)
    phi = np.deg2rad(phi)
    delta_x = x - xr
    delta_y = y - yr
    delta_z = z - zr
    x = -np.sin(lbd) * delta_x + np.cos(lbd) * delta_y
    y = (
        -np.sin(phi) * np.cos(lbd) * delta_x
        - np.sin(phi) * np.sin(lbd) * delta_y
        + np.cos(phi) * delta_z
    )
    z = (
        np.cos(phi) * np.cos(lbd) * delta_x
        + np.cos(phi) * np.sin(lbd) * delta_y
        + np.sin(phi) * delta_z
    )
    return x, y, z


def enu2ecef(
    xr: float, yr: float, zr: float, x: float, y: float, z: float
) -> Tuple[float, float, float]:
    """ENU坐标系转ECEF坐标系

    Args:
        xr (float): 接收机X坐标
        yr (float): 接收机Y坐标
        zr (float): 接收机Z坐标
        x (float): 卫星X坐标
        y (float): 卫星Y坐标
        z (float): 卫星Z坐标

    Returns:
        Tuple[float, float, float]: 卫星在ECEF坐标系下的位置
    """
    lbd, phi, _ = ecef2lla(xr, yr, zr)
    lbd = np.deg2rad(lbd)
    phi = np.deg2rad(phi)
    delta_x = (
        -np.sin(lbd) * x - np.sin(phi) * np.cos(lbd) * y + np.cos(phi) * np.cos(lbd) * z
    )
    delta_y = (
        np.cos(lbd) * x - np.sin(phi) * np.sin(lbd) * y + np.cos(phi) * np.sin(lbd) * z
    )
    delta_z = np.cos(phi) * y + np.sin(phi) * z
    x = delta_x + xr
    y = delta_y + yr
    z = delta_z + zr
    return x, y, z


if __name__ == "__main__":
    x, y, z = lla2ecef(116.3, 70.9, 0)
    print(x, y, z)
    L, B, H = ecef2lla(x, y, z)
    print(L, B, H)
    l_, b_, h_ = 39.64981310237203, -7.431278447345754, 21519142.207175188
    x_, y_, z_ = lla2ecef(l_, b_, h_)
    e, n, u = ecef2enu(x, y, z, x_, y_, z_)
    print(e, n, u)
    print(ecef2lla(x_, y_, z_))
