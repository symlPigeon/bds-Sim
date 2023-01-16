'''
Author: symlpigeon
Date: 2023-01-16 17:42:09
LastEditTime: 2023-01-16 18:52:38
LastEditors: symlpigeon
Description: D1 导航电文子帧3
FilePath: /bds-Sim/bdsTx/frame/b1i/d1/subframe3.py
'''

from bdsTx.coding.b1i_bch import b1i_bch_encode_bin
from bdsTx.frame.b1i.d1.pre import Pre
from bdsTx.frame.util import data2bin, data2bincomplement
from bdsTx.satellite_info.time_system import utc2bds


def create_subframe3(curr_time: float, eph: dict) -> str:
    """生成B1I D1子帧3格式
    为了方便性，这里一并进行了BCH编码，而不是B1C的先成帧再编码

    Args:
        curr_time (float):
        eph (dict): 星历文件

    Returns:
        str: 子帧3, hex str
    """
    frame = ""
    
    # ----- Word  1 -----
    WN, SOW = utc2bds(curr_time)
    SOW = bin(int(SOW))[2:].zfill(20)
    SOW_h, SOW_l = SOW[0:8], SOW[8:20]
    frame += b1i_bch_encode_bin(Pre + "0000" + "011" + SOW_h)  # Pre 11 bits + Rev 4 bits + FraID 3 bits + SOW first 8 bits
    
    # ----- Word  2 -----
    toe = data2bin(eph["Toe"], 17, pow(2, 3))
    toe_m, toe_l = toe[2:12], toe[12:17]
    frame += b1i_bch_encode_bin(SOW_l + toe_m)  # toe middle 10 bits + SOW last 12 bits
    
    # ----- Word  3 -----
    i_0 = data2bincomplement(eph["i0"], 32, pow(2, -31))
    i_0_h, i_0_l = i_0[0:17], i_0[17:32]
    frame += b1i_bch_encode_bin(toe_l + i_0_h)  # toe last 5 bits + i_0 high 17 bits
    
    # ----- Word  4 -----
    cic = data2bincomplement(eph["Cic"], 18, pow(2, -31))
    cic_h, cic_l = cic[0:7], cic[7:18]
    frame += b1i_bch_encode_bin(i_0_l + cic_h)  # i_0 low 15 bits + Cic high 7 bits
    
    # ----- Word  5 -----
    omega_dot = data2bincomplement(eph["Omega_dot"], 24, pow(2, -43))
    omega_dot_h, omega_dot_l = omega_dot[0:11], omega_dot[11:24]
    frame += b1i_bch_encode_bin(cic_l + omega_dot_h)  # Cic low 11 bits + omega_dot high 11 bits
    
    # ----- Word  6 -----
    cis = data2bincomplement(eph["Cis"], 18, pow(2, -31))
    cis_h, cis_l = cis[0:9], cis[9:18]
    frame += b1i_bch_encode_bin(omega_dot_l + cis_h)  # omega_dot low 13 bits + Cis high 9 bits
    
    # ----- Word  7 -----
    idot = data2bincomplement(eph["IDOT"], 14, pow(2, -43))
    idot_h, idot_l = idot[0:13], idot[13:14]
    frame += b1i_bch_encode_bin(cis_l + idot_h)  # Cis low 9 bits + IDOT high 13 bits
    
    # ----- Word  8 -----
    omega_0 = data2bincomplement(eph["Omega0"], 32, pow(2, -31))
    omega_0_h, omega_0_l = omega_0[0:21], omega_0[21:32]
    frame += b1i_bch_encode_bin(idot_l + omega_0_h)  # IDOT low 1 bit + Omega_0 high 21 bits
    
    # ----- Word  9 -----
    omega = data2bincomplement(eph["omega"], 32, pow(2, -31))
    omega_h, omega_l = omega[0:11], omega[11:32]
    frame += b1i_bch_encode_bin(omega_0_l + omega_h)  # Omega_0 low 11 bits + omega high 11 bits
    
    # ----- Word 10 -----
    frame += b1i_bch_encode_bin(omega_l + "0") # omega low 21 bits + Rev 1 bit
    
    # convert bin str to hex str
    return "".join([hex(int(frame[i : i + 4], 2))[2:] for i in range(0, len(frame), 4)])


if __name__ == "__main__":
    import time

    curr_time = time.time()
    eph = {
            "toc": 518400,
            "a0": 0.000919836340472,
            "a1": -3.43369777056e-12,
            "a2": 0.0,
            "Crs": -425.078125,
            "delta_n0": -6.4181244835e-10,
            "M0": 0.660436096054,
            "Cuc": -1.38343311846e-05,
            "e": 0.000552382436581,
            "Cus": -3.85334715247e-06,
            "Toe": 518400.0,
            "Cic": -2.23517417908e-08,
            "Omega0": -0.8442337586,
            "Cis": 1.42026692629e-07,
            "i0": 0.0681732025675,
            "Crc": 113.546875,
            "omega": -0.47219019011,
            "Omega_dot": 1.66756946096e-09,
            "IDOT": -1.83936233111e-10,
            "BDT Week": 888.0,
            "sv_accuracy": 2,
            "hs": 0,
            "tgd": -4.7e-09,
            "isc": -1e-08,
            "signal_time": 518400.0,
            "aode": 1,
            "sqrtA": 6493.4376049,
            "aodc": 0,
            "support_type": 1,
            "sat_type": 1
        }
    print(create_subframe3(curr_time, eph))
