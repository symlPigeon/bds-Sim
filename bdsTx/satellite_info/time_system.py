"""
Author: symlpigeon
Date: 2022-11-08 16:13:30
LastEditTime: 2022-11-10 16:13:05
LastEditors: symlpigeon
Description: UTC - GPS - BDS 时间转换
FilePath: /sim_bds/python/satellite_info/time_system.py
"""

import calendar
import datetime
import math
import time
from typing import List, Tuple


def utc2bds(utc_time: float) -> Tuple[int, float]:
    """UTC时间转换为北斗时间

    Args:
        utc_time (float): UTC时间戳

    Returns:
        Tuple[int, float]: 二元组，(北斗周，北斗秒)
    """
    bds_time_begin = calendar.timegm((2006, 1, 1, 0, 0, 0))
    interval = utc_time - bds_time_begin
    bds_week = int(interval / 604800)
    bds_second = interval % 604800
    return bds_week, bds_second


def bds2utc(bds_week: int, bds_second: float) -> float:
    """北斗时间转换为UTC时间

    Args:
        bds_week (int): 北斗周
        bds_second (float): 北斗秒

    Returns:
        float: UTC时间戳
    """
    bds_time_begin = calendar.timegm((2006, 1, 1, 0, 0, 0))
    return bds_time_begin + bds_week * 604800 + bds_second


def utc2mjd(utc_time: float) -> float:
    """UTC转约化儒略日时间

    Args:
        utc_time (float): UTC时间

    Returns:
        float: 约化儒略日, 天为单位
    """
    # 这玩意不准......
    # date = datetime.datetime.fromtimestamp(utc_time)
    # julian_day = (
    #     367 * date.year
    #     - int((7 * (date.year + int((date.month + 9) / 12.0))) / 4.0)
    #     + int((275 * date.month) / 9.0)
    #     + date.day
    #     + 1721013.5
    #     + (date.hour + date.minute / 60.0 + date.second / pow(60, 2)) / 24.0
    #     - 0.5 * math.copysign(1, 100 * date.year + date.month - 190002.5)
    #     + 0.5
    # )
    # return julian_day - 2400000.5

    BDS_JDT_START = 57389
    return (utc_time - calendar.timegm((2016, 1, 1, 12, 0, 0))) / 86400 + BDS_JDT_START


def mjd2mdj_odd_hour(mjd: float) -> float:
    """约化儒略日转换为MJD（奇小时）

    Args:
        mjd (float): 约化儒略日

    Returns:
        float: MJD（奇小时）
    """
    non_int_time = mjd - int(mjd)
    hour = int(non_int_time * 24)
    if int(hour) % 2 == 0:
        hour += 1
    return int(hour)


def get_closest_timestamp(timestamps: List[str], target_time: float) -> str:
    """从一坨时间戳里面挑一个最近的时间戳

    Args:
        timestamps (List[str]): 时间戳列表
        target_time (float): 目标时间

    Returns:
        str: 最近的一个时间戳
    """
    # convert YYYY-MM-DD HH:MM:SS to timestamp
    float_timestamps = [(calendar.timegm(time.strptime(x, "%Y-%m-%d_%H:%M:%S")), x) for x in timestamps]
    float_timestamps = sorted(float_timestamps, key=lambda x: abs(x[0] - target_time))
    return float_timestamps[0][1]


if __name__ == "__main__":
    import time

    # 一致性
    utc_time = time.time()
    print(utc_time)
    bds_week, bds_second = utc2bds(utc_time)
    print(bds_week, bds_second)
    utc_time = bds2utc(bds_week, bds_second)
    print(utc_time)
    bds_week, bds_second = utc2bds(utc_time)
    print(bds_week, bds_second)

    # MJD
    # 2013年1月1日00:30:00（UT）是儒略日期2,456,293.520833
    utc_time = calendar.timegm((2013, 1, 1, 0, 30, 0))
    print(utc2mjd(utc_time))

    for hour in range(0, 24):
        ts = calendar.timegm((2013, 1, 1, hour, 0, 1))
        print(hour, mjd2mdj_odd_hour(utc2mjd(ts)))
