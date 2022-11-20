"""
Author: symlpigeon
Date: 2022-11-16 13:23:35
LastEditTime: 2022-11-16 13:23:37
LastEditors: symlpigeon
Description: B1C subframe3
FilePath: /bds-Sim/bdsTx/frame/b1c/b1c_subframe3.py
"""

import json
import logging

import numpy as np

from bdsTx.coding.crc24q import crc24q_gen
from bdsTx.coding.ldpc import ldpc64, ldpcMat_44_88
from bdsTx.coding.pre_ldpc import pre_ldpc_enc
from bdsTx.frame.util import data2bincomplement


def make_iono_corr_args(bdgim_data: list) -> str:
    """生成BDGIM修正参数

    Args:
        bdgim_data (list): BDGIM修正参数

    Returns:
        str: 二进制串
    """
    ans = ""
    ans += data2bincomplement(bdgim_data[0], 10, pow(2, -3))
    ans += data2bincomplement(bdgim_data[1], 8, pow(2, -3))
    ans += data2bincomplement(bdgim_data[2], 8, pow(2, -3))
    ans += data2bincomplement(bdgim_data[3], 8, pow(2, -3))
    ans += data2bincomplement(bdgim_data[4], 8, -pow(2, -3))
    ans += data2bincomplement(bdgim_data[5], 8, pow(2, -3))
    ans += data2bincomplement(bdgim_data[6], 8, pow(2, -3))
    ans += data2bincomplement(bdgim_data[7], 8, pow(2, -3))
    ans += data2bincomplement(bdgim_data[8], 8, pow(2, -3))
    return ans


def make_sisaioc(ephemeris: dict) -> str:
    """空间信号精度指数

    Args:
        ephemeris (dict): 星历

    Returns:
        str: 二进制串
    """
    sisa = ephemeris["sv_accuracy"]
    # bit 9 to 30
    sisaioc = (sisa >> 2) & 0x3FFFFF
    return data2bincomplement(sisaioc, 22, 1)


def make_bdt_utc_sync_args() -> str:
    """BDT-UTC 时钟同步参数

    Returns:
        str: 二进制串
    """
    # TODO: 找到数据源，完善这一部分
    logging.warning("BDT-UTC Time Sync Args is not implemented!")
    return "0" * 97


def make_subframe3_type1(ephemeris: dict, bdgim_data: list) -> bytes:
    """创建类型1的子帧3

    Args:
        ephemeris (dict): 星历数据
        bdgim_data (dict): 电离层参数

    Returns:
        bytes: bytes形式的子帧
    """
    pageid = data2bincomplement(0b1, 6, 1)
    hs = data2bincomplement(0, 2, 1)
    dif = data2bincomplement(0, 1, 1)
    sif = data2bincomplement(0, 1, 1)
    aif = data2bincomplement(0, 1, 1)
    sismai = data2bincomplement((ephemeris["sv_accuracy"] >> 28) & 0xf, 4, 1)
    sisaioe = data2bincomplement((ephemeris["sv_accuracy"] >> 24) & 0x1f, 5, 1)
    sisaioc = make_sisaioc(ephemeris)
    bdgim = make_iono_corr_args(bdgim_data)
    time_sync = make_bdt_utc_sync_args()
    rev = "0" * 27
    frame = pageid + hs + dif + sif + aif + sismai + sisaioe + sisaioc + bdgim + time_sync + rev
    frame_b = bytes([int(frame[i:i+8], 2) for i in range(len(frame))])
    frame = frame_b + crc24q_gen(frame_b)
    return frame
    