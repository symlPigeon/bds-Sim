"""
Author: symlpigeon
Date: 2022-11-12 12:18:41
LastEditTime: 2022-11-12 12:18:45
LastEditors: symlpigeon
Description: 一些进制转换的函数
FilePath: /bdsTx/frame/util.py
"""

from typing import Union
import math


def data2bincomplement(data: Union[int, float], bitsize: int, ratio: float = 1) -> str:
    """将十进制数转换成二进制形式的补码字符串

    Args:
        data (Union[int, float]): 数据
        bitsize (int): 数据位数
        ratio (int, optional): 比例系数. Defaults to 1.

    Returns:
        str: 01, str
    """
    # 将数据按照比例系数换算
    data = int(data / ratio)
    # 转换为补码
    data = int.from_bytes(data.to_bytes(math.ceil(bitsize / 8), "big", signed=True), "big")
    return bin(data)[2:].zfill(bitsize)[-bitsize:]


if __name__ == "__main__":
    print(data2bincomplement(-1231, 13))
