'''
Author: symlpigeon
Date: 2023-01-19 10:14:09
LastEditTime: 2023-01-20 14:50:42
LastEditors: symlpigeon
Description: D1 导航电文子帧4
FilePath: /bds-Sim/bdsTx/frame/b1i/d1/subframe4.py
'''

import numpy as np

from bdsTx.coding.b1i_bch import b1i_bch_encode_bin
from bdsTx.frame.b1i.d1.pre import Pre
from bdsTx.frame.util import data2bin, data2bincomplement
from bdsTx.satellite_info.time_system import utc2bds


def create_subframe4(curr_time: float, alc: dict, page_id: int = 1) -> str:
    """生成B1I D1子帧4格式

    Args:
        curr_time (float): 参考时间
        alc (dict): 历书数据
        page_id (int): 页面ID

    Returns:
        str: 十六进制数据串
    """
    frame = ""
    
    # Parameters
    WN, SOW = utc2bds(curr_time)
    alc = alc[str(page_id)]
    sow = data2bin(SOW, 20, 1)
    sqrtA = data2bin(alc["SquareRootOfSemiMajorAxis"], 24, pow(2, -11))
        # NOTE: I'm not sure if multiply pi is a correct idea...
        # The range of omega0 is [-1, 1], but the value in almanac file exceeds the range.
        # So I wonder if i should multiply pi to the value...
        # Yes, the omega and m0 are also in the same situation.
    omega0 = data2bincomplement(alc["RightAscenAtWeek"], 24, pow(2, -23) * np.pi)
    delta_i = data2bincomplement(alc["OrbitalInclination"], 16, pow(2, -19) * np.pi)
    toa = data2bin(alc["TimeOfApplicability"], 8, pow(2, 12))
    omega_dot = data2bincomplement(alc["RateOfRightAscension"], 17, pow(2, -38) * np.pi)
    omega = data2bincomplement(alc["ArgumentOfPerigee"], 24, pow(2, -23) * np.pi)
    e = data2bin(alc["Eccentricity"], 17, pow(2, -21))
    m0 = data2bincomplement(alc["MeanAnomaly"], 24, pow(2, -23) * np.pi)
    a0 = data2bincomplement(alc["ClockTimeBiasCoefficient"], 11, pow(2, -20))
    a1 = data2bincomplement(alc["ClockTimeDriftCoefficient"], 11, pow(2, -38))
    pnum = data2bin(page_id, 7, 1)
    # Split into 2 words
    SOW_h, SOW_l = sow[0:8], sow[8:20]
    sqrtA_h, sqrtA_l = sqrtA[0:2], sqrtA[2:24]
    omega0_h, omega0_l = omega0[0:22], omega0[22:24]
    delta_i_h, delta_i_l = delta_i[0:3], delta_i[3:16]
    omega_dot_h, omega_dot_l = omega_dot[0], omega_dot[1:17]
    omega_h, omega_l = omega[0:6], omega[6:24]
    m0_h, m0_l = m0[0:4], m0[4:24]
    
    # 子帧5不进行分时播发
    amepid = "00"
    
    frame += b1i_bch_encode_bin(Pre + "0000" + "100" + SOW_h)
    # 7 bits Pnum 
    frame += b1i_bch_encode_bin(SOW_l + "0" + pnum + sqrtA_h)
    frame += b1i_bch_encode_bin(sqrtA_l)
    frame += b1i_bch_encode_bin(a1 + a0)
    frame += b1i_bch_encode_bin(omega0_h)
    frame += b1i_bch_encode_bin(omega0_l + e + delta_i_h)
    frame += b1i_bch_encode_bin(delta_i_l + toa + omega_dot_h)
    frame += b1i_bch_encode_bin(omega_dot_l + omega_h)
    frame += b1i_bch_encode_bin(omega_l + m0_h)
    frame += b1i_bch_encode_bin(m0_l + amepid)
    
    return "".join([hex(int(frame[i : i + 4], 2))[2:] for i in range(0, len(frame), 4)])


if __name__ == "__main__":
    alc = {
        "Health": 1,
        "Eccentricity": 0.00049495697021,
        "TimeOfApplicability": 430080.0,
        "OrbitalInclination": 0.019821908,
        "RateOfRightAscension": -7.08600945e-09,
        "SquareRootOfSemiMajorAxis": 5282.568359,
        "RightAscenAtWeek": -2.164172378,
        "ArgumentOfPerigee": 0.226022856,
        "MeanAnomaly": 2.04332308,
        "ClockTimeBiasCoefficient": 9.536743e-07,
        "ClockTimeDriftCoefficient": 0.0,
        "WeekNumber": 888
    }
    import time
    print(create_subframe4(time.time(), alc, 1))