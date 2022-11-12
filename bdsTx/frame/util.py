"""
Author: symlpigeon
Date: 2022-11-12 12:18:41
LastEditTime: 2022-11-12 12:18:45
LastEditors: symlpigeon
Description: 一些进制转换的函数
FilePath: /bdsTx/frame/util.py
"""

from typing import Union


def twos_comp(val: int, bits: int) -> int:

    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val


def count_bits(data: int) -> int:
    """计算二进制的位数

    Args:
        data (int): 数据

    Returns:
        int: 二进制位数
    """
    cnt = 0
    while data:
        data &= data - 1
        cnt += 1
    return cnt


def data2bincomplement(data: Union[int, float], bitsize: int, ratio: int = 1) -> bytes:
    """将十进制数转换为二进制补码形式的bytes, 长度不满8位LSB补零

    Args:
        data (Union[int, float]): 数据
        bitsize (int): 数据位数
        ratio (int, optional): 比例系数. Defaults to 1.

    Returns:
        bytes: 返回的bytes
    """
    data = int(data / ratio)
    bitlen = count_bits(data)
    if bitlen > bitsize:
        data = data >> (bitlen - bitsize)
    signbit = 1 << (bitsize - 1)
    sign = data & signbit
    mask = signbit - 1
    if sign:
        data = -(data & mask)
    # LSB 补上满到8位的0
    data <<= (8 - bitsize % 8) % 8
    ans = b""
    while data:
        lsb = data & 0xFF
        ans = lsb.to_bytes(1, "big") + ans
        data >>= 4
    return ans


if __name__ == "__main__":
    print(count_bits(-3))
