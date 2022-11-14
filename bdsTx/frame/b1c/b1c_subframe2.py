"""
Author: symlpigeon
Date: 2022-11-12 11:27:00
LastEditTime: 2022-11-12 11:27:03
LastEditors: symlpigeon
Description: B1C子帧2构造
FilePath: /bdsTx/frame/b1c/b1c_subframe2.py
"""

from coding import pre_ldpc, ldpc, ldpc_mat
from coding import crc24q
from satellite_info import time_system


def make_subframe2(curr_time: float, ephemeris: dict) -> bytes:
    bds_week, bds_second = time_system.utc2bds(curr_time)
    WN = bds_week & 0x1FFF
    how = int(bds_second / 3600) & 0xFF
    iode = ephemeris["iode/aode"] & 0x3FF
    iodc = ephemeris["iodc/aodc"] & 0xFF
    