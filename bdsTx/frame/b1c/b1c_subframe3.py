"""
Author: symlpigeon
Date: 2022-11-16 13:23:35
LastEditTime: 2022-11-16 13:23:37
LastEditors: symlpigeon
Description: B1C subframe3
FilePath: /bds-Sim/bdsTx/frame/b1c/b1c_subframe3.py
"""

import json

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


