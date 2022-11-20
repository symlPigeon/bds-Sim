"""
Author: symlpigeon
Date: 2022-11-12 11:27:00
LastEditTime: 2022-11-12 11:27:03
LastEditors: symlpigeon
Description: B1C子帧2构造
FilePath: /bdsTx/frame/b1c/b1c_subframe2.py
"""

import numpy as np

from bdsTx.coding import crc24q, ldpc, ldpc_mat, pre_ldpc
from bdsTx.frame.util import data2bincomplement
from bdsTx.satellite_info import time_system


def make_ephemeris1(ephemeris: dict) -> str:
    """创建星历I

    Args:
        ephemeris (dict): 星历数据

    Returns:
        str: 二进制字符串形式的星历I
    """
    ans = ""
    ans += data2bincomplement(ephemeris["Toe"], 11, 300)
    ans += data2bincomplement(ephemeris["sat_type"], 2, 1)
    ans += data2bincomplement(ephemeris["deltaA/sqrtA"], 26, pow(2, -9))
    ans += data2bincomplement(ephemeris["A_DOT/EMPTY"], 25, pow(2, -21))
    ans += data2bincomplement(ephemeris["delta_n0"], 17, pow(2, -44))
    ans += data2bincomplement(ephemeris["delta_n0_dot"], 23, pow(2, -57))
    ans += data2bincomplement(ephemeris["M0"], 33, pow(2, -32))
    ans += data2bincomplement(ephemeris["e"], 33, pow(2, -34))
    ans += data2bincomplement(ephemeris["omega"], 33, pow(2, -32))
    return ans


def make_ephemeris2(ephemeris:dict) -> str:
    """创建星历II

    Args:
        ephemeris (dict): 星历数据

    Returns:
        str: 二进制字符串形式的星历II
    """
    ans = ""
    ans += data2bincomplement(ephemeris["Omega0"], 33, pow(2, -32))
    ans += data2bincomplement(ephemeris["i0"], 33, pow(2, -32))
    ans += data2bincomplement(ephemeris["Omega_dot"], 19, pow(2, -44))
    ans += data2bincomplement(ephemeris["IDOT"], 15, pow(2, -44))
    ans += data2bincomplement(ephemeris["Cis"], 16, pow(2, -30))
    ans += data2bincomplement(ephemeris["Cic"], 16, pow(2, -30))
    ans += data2bincomplement(ephemeris["Crs"], 24, pow(2, -8))
    ans += data2bincomplement(ephemeris["Crc"], 24, pow(2, -8))
    ans += data2bincomplement(ephemeris["Cus"], 21, pow(2, -30))
    ans += data2bincomplement(ephemeris["Cuc"], 21, pow(2, -30))
    return ans


def make_clockbias(ephemeris: dict) -> str:
    """创建钟差参数

    Args:
        ephemeris (dict): 星历

    Returns:
        str: 二进制字符串形式的钟差参数
    """
    ans = ""
    ans += data2bincomplement(ephemeris["toc"], 11, 300)
    ans += data2bincomplement(ephemeris["a0"], 25, pow(2, -34))
    ans += data2bincomplement(ephemeris["a1"], 22, pow(2, -50))
    ans += data2bincomplement(ephemeris["a2"], 11, pow(2, -66))
    return ans


def make_subframe2(curr_time: float, ephemeris: dict) -> bytes:
    bds_week, bds_second = time_system.utc2bds(curr_time)
    WN = data2bincomplement(bds_week & 0x1FFF, 13)
    how = data2bincomplement(int(bds_second / 3600) & 0xFF, 8)
    iode = data2bincomplement(ephemeris["iode/aode"] & 0x3FF, 10)
    iodc = data2bincomplement(ephemeris["iodc/aodc"] & 0xFF, 8)
    eph1 = make_ephemeris1(ephemeris)
    eph2 = make_ephemeris2(ephemeris)
    clock_bias = make_clockbias(ephemeris)
    TGDB2ap = data2bincomplement(ephemeris["tgd"], 12, pow(2, -34))
    ISCB1Cd = data2bincomplement(ephemeris["isc"], 12, pow(2, -34))
    TGDB1Cp = data2bincomplement(ephemeris["tgd"], 12, pow(2, -34))
    Rev = data2bincomplement(0, 7)
    frame = WN + how + iode + iodc + eph1 + eph2 + clock_bias + TGDB2ap + ISCB1Cd + TGDB1Cp + Rev
    frame = bytes([int(frame[i:i+8], 2) for i in range(0, len(frame), 8)])
    frame += crc24q.crc24q_gen(frame)
    return frame


def encoding_subframe2(subframe2: bytes, ldpc_mat: np.ndarray) -> np.ndarray:
    """对子帧2进行LDPC编码

    Args:
        subframe2 (bytes): 子帧2数据

    Returns:
        bytes: LDPC编码后的子帧2
    """
    data = pre_ldpc.pre_ldpc_enc(subframe2, 600)
    return ldpc.ldpc64(ldpc_mat, data)


if __name__ == "__main__":
    import json
    import time
    eph = json.load(open("../../../bdsTx/satellite_info/ephemeris/tarc3130.22b.json", "r", encoding="utf-8"))
    frame = make_subframe2(time.time(), eph["19"]["2022-11-09_00:00:00"])
    matpath = "../../../bdsTx/coding/ldpc_mat_gen/ldpc_matG_100_200.json"
    mat = json.load(open(matpath, "r", encoding="utf-8"))
    print(encoding_subframe2(frame, np.array(mat)))
    