"""
Author: symlpigeon
Date: 2023-01-16 14:47:54
LastEditTime: 2023-01-16 17:03:20
LastEditors: symlpigeon
Description: 生成D1子帧1格式
FilePath: /bds-Sim/bdsTx/frame/b1i/d1/subframe1.py
"""

from bdsTx.coding.b1i_bch import b1i_bch_encode_bin
from bdsTx.frame.b1i.d1.pre import Pre
from bdsTx.frame.util import data2bin, data2bincomplement
from bdsTx.satellite_info.time_system import utc2bds


def create_subframe1(curr_time: float, eph: dict, iono_corr: dict) -> str:
    """生成B1I D1子帧1格式
    为了方便性，这里一并进行了BCH编码，而不是B1C的先成帧再编码

    Args:
        curr_time (float):
        eph (dict): 星历文件
        iono_corr (dict): 电离层模型参数

    Returns:
        str: 子帧1, hex str
    """
    frame = ""

    # ----- Word 1 -----
    word1 = ""
    word1 += Pre + "0000"  # Pre 11 bits + Rev 4 bits
    word1 += "001"  # FraID 3 bits
    WN, SOW = utc2bds(curr_time)
    SOW = bin(int(SOW))[2:].zfill(20)
    word1 += SOW[0:8]  # SOW first 8 bits
    frame += b1i_bch_encode_bin(word1)

    # ----- Word 2 -----
    word2 = ""
    word2 += SOW[8:20]  # SOW last 12 bits
    word2 += bin(eph["hs"])[2:][0]  # SatH1 1 bit
    word2 += bin(eph["aodc"])[2:].zfill(5)  # AODC 5 bits
    # TODO: Implement URAI parameter
    word2 += "0000"  # URAI 4 bits
    frame += b1i_bch_encode_bin(word2)

    # ----- Word 3 -----
    word3 = ""
    word3 += bin(WN)[2:].zfill(13)  # WN 13 bits
    toe = data2bin(eph["Toe"], 17, pow(2, 3))
    toe_h = toe[0:9]  # TOE first 9 bits
    toe_l = toe[9:17]  # TOE last 8 bits
    word3 += toe_h  # Toe high 9 bits
    frame += b1i_bch_encode_bin(word3)

    # ----- Word 4 -----
    word4 = ""
    word4 += toe_l  # Toe low 8 bits
    # TODO: Implement T_GD parameter，即*星上设备时延差*
    word4 += "0" * 10  # T_GD1 10 bits
    word4 += "0" * 4  # T_GD2 high 4 bits
    frame += b1i_bch_encode_bin(word4)

    # ------ Word 5 -----
    word5 = ""
    word5 += "0" * 6  # T_GD2 low 6 bits
    word5 += data2bincomplement(iono_corr["alpha"][0], 8, pow(2, -30))  # alpha0 8 bits
    word5 += data2bincomplement(iono_corr["alpha"][1], 8, pow(2, -27))  # alpha1 8 bits
    frame += b1i_bch_encode_bin(word5)

    # ----- Word 6 -----
    word6 = ""
    word6 += data2bincomplement(iono_corr["alpha"][2], 8, pow(2, -24))  # alpha2 8 bits
    word6 += data2bincomplement(iono_corr["alpha"][3], 8, pow(2, -24))  # alpha3 8 bits
    beta0 = data2bincomplement(iono_corr["beta"][0], 8, pow(2, 11))
    beta0_h = beta0[0:6]
    beta0_l = beta0[6:8]
    word6 += beta0_h  # beta0 high 6 bits
    frame += b1i_bch_encode_bin(word6)

    # ----- Word 7 -----
    word7 = ""
    word7 += beta0_l  # beta0 low 2 bits
    word7 += data2bincomplement(iono_corr["beta"][1], 8, pow(2, 14))  # beta1 8 bits
    word7 += data2bincomplement(iono_corr["beta"][2], 8, pow(2, 16))  # beta2 8 bits
    beta3 = data2bincomplement(iono_corr["beta"][3], 8, pow(2, 16))
    beta3_h = beta3[0:4]
    beta3_l = beta3[4:8]
    word7 += beta3_h  # beta3 high 4 bits
    frame += b1i_bch_encode_bin(word7)

    # ------ Word 8 -----
    word8 = ""
    word8 += beta3_l  # beta3 low 4 bits
    word8 += data2bincomplement(eph["a2"], 11, pow(2, -66))  # 11 bits a2 clk corr coef
    a0 = data2bincomplement(eph["a0"], 24, pow(2, -33))
    a0_h = a0[0:7]
    a0_l = a0[7:24]
    word8 += a0_h  # first 7 bits a0 clk corr coef
    frame += b1i_bch_encode_bin(word8)

    # ----- Word 9 -----
    word9 = ""
    word9 += a0_l  # last 17 bits a0 clk corr coef
    a1 = data2bincomplement(eph["a1"], 22, pow(2, -50))
    a1_h = a1[0:5]
    a1_l = a1[5:22]
    word9 += a1_h  # first 5 bits a1 clk corr coef
    frame += b1i_bch_encode_bin(word9)

    # ----- Word 10 -----
    word10 = ""
    word10 += a1_l  # last 17 bits a1 clk corr coef
    word10 += data2bincomplement(eph["aode"], 5, 1)  # AODE 5 bits
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
    iono_corr = {
        "sate_id": "14",
        "alpha": [3.353e-08, 8.196e-08, -1.133e-06, 1.729e-06],
        "beta": [122900.0, -65540.0, -589800.0, 1114000.0],
    }
    print(create_subframe1(curr_time, eph, iono_corr))
