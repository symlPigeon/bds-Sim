"""
Author: symlpigeon
Date: 2023-01-16 17:01:11
LastEditTime: 2023-01-16 17:39:03
LastEditors: symlpigeon
Description: D1 导航电文子帧2
FilePath: /bds-Sim/bdsTx/frame/b1i/d1/subframe2.py
"""


import numpy as np

from bdsTx.coding.b1i_bch import b1i_bch_encode_bin
from bdsTx.frame.b1i.d1.pre import Pre
from bdsTx.frame.util import data2bin, data2bincomplement
from bdsTx.satellite_info.time_system import utc2bds


def create_subframe2(curr_time: float, eph: dict) -> str:
    """生成B1I D1子帧2格式
    为了方便性，这里一并进行了BCH编码，而不是B1C的先成帧再编码

    Args:
        curr_time (float):
        eph (dict): 星历文件

    Returns:
        str: 子帧2, hex str
    """
    frame = ""

    # ----- Word  1 -----
    word1 = ""
    word1 += Pre + "0000"  # Pre 11 bits + Rev 4 bits
    word1 += "010"  # FraID 3 bits
    WN, SOW = utc2bds(curr_time)
    SOW = bin(int(SOW))[2:].zfill(20)
    word1 += SOW[0:8]  # SOW first 8 bits
    frame += b1i_bch_encode_bin(word1)

    # ----- Word  2 -----
    word2 = ""
    word2 += SOW[8:20]  # SOW last 12 bits
        # NOTE: In BDS frame, the unit of delta_n is pi/s, however in ephemeris file, the unit is rad/s
        # SO we need to convert the unit. Some other parameters also need to be converted.
    delta_n = data2bincomplement(eph["delta_n0"], 16, pow(2, -43) * np.pi)
    delta_n_h = delta_n[0:10]  # delta_n first 10 bits
    delta_n_l = delta_n[10:16]  # delta_n last 6 bits
    word2 += delta_n_h  # delta_n high 10 bits
    frame += b1i_bch_encode_bin(word2)

    # ----- Word  3 -----
    word3 = ""
    word3 += delta_n_l  # delta_n low 6 bits
    cuc = data2bincomplement(eph["Cuc"], 18, pow(2, -31))
    cuc_h = cuc[0:16]
    cuc_l = cuc[16:18]
    word3 += cuc_h  # Cuc high 16 bits
    frame += b1i_bch_encode_bin(word3)

    # ----- Word  4 -----
    word4 = ""
    word4 += cuc_l  # Cuc low 2 bits
    M0 = data2bincomplement(eph["M0"], 32, pow(2, -31) * np.pi)
    M0_h = M0[0:20]
    M0_l = M0[20:32]
    word4 += M0_h  # M0 high 20 bits
    frame += b1i_bch_encode_bin(word4)

    # ----- Word  5 -----
    word5 = ""
    word5 += M0_l  # M0 low 12 bits
    e = data2bin(eph["e"], 32, pow(2, -33))
    e_h = e[0:10]
    e_l = e[10:32]
    word5 += e_h  # e high 10 bits
    frame += b1i_bch_encode_bin(word5)

    # ----- Word  6 -----
    word6 = ""
    word6 += e_l  # e low 22 bits
    frame += b1i_bch_encode_bin(word6)

    # ----- Word  7 -----
    word7 = ""
    word7 += data2bincomplement(eph["Cus"], 18, pow(2, -31))  # Cus 18 bits
    crc = data2bincomplement(eph["Crc"], 18, pow(2, -6))
    crc_h = crc[0:4]
    crc_l = crc[4:18]
    word7 += crc_h  # Crc high 4 bits
    frame += b1i_bch_encode_bin(word7)

    # ----- Word  8 -----
    word8 = ""
    word8 += crc_l  # Crc low 14 bits
    crs = data2bincomplement(eph["Crs"], 18, pow(2, -6))
    crs_h = crs[0:8]
    crs_l = crs[8:18]
    word8 += crs_h  # Crs high 8 bits
    frame += b1i_bch_encode_bin(word8)

    # ----- Word  9 -----
    word9 = ""
    word9 += crs_l  # Crs low 10 bits
    sqrtA = data2bin(eph["sqrtA"], 32, pow(2, -19))
    sqrtA_h = sqrtA[0:12]
    sqrtA_l = sqrtA[12:32]
    word9 += sqrtA_h
    frame += b1i_bch_encode_bin(word9)

    # ------ Word 10 -----
    word10 = ""
    word10 += sqrtA_l  # sqrtA low 20 bits
    toe_h = data2bin(eph["Toe"], 17, pow(2, 3))[0:2]
    word10 += toe_h
    frame += b1i_bch_encode_bin(word10)

    # convert bin str to hex str
    return "".join([hex(int(frame[i : i + 4], 2))[2:] for i in range(0, len(frame), 4)])


if __name__ == "__main__":
    import time

    curr_time = time.time()
    eph = {
        "support_type": 1,
        "toc": 522000,
        "a0": 0.000919824116863,
        "a1": -3.41060513165e-12,
        "a2": 0.0,
        "Crs": -347.953125,
        "delta_n0": -1.34398455378e-09,
        "M0": 0.931910033702,
        "Cuc": -1.15092843771e-05,
        "e": 0.000549515360035,
        "Cus": 5.21447509527e-06,
        "Toe": 522000.0,
        "Cic": -1.210719347e-08,
        "Omega0": -2.52764175673,
        "Cis": 9.31322574616e-08,
        "i0": 0.073241217465,
        "Crc": -164.34375,
        "omega": -1.79753130082,
        "Omega_dot": 2.46510268142e-09,
        "IDOT": -1.10004582132e-10,
        "BDT Week": 888.0,
        "sv_accuracy": 2,
        "hs": 0,
        "tgd": -4.7e-09,
        "isc": -1e-08,
        "signal_time": 522000.0,
        "aode": 1,
        "sqrtA": 6493.42383957,
        "aodc": 0,
        "sat_type": 1,
    }
    print(create_subframe2(curr_time, eph))
