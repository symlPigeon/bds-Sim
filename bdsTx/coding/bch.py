"""
Author: symlpigeon
Date: 2022-11-10 21:46:25
LastEditTime: 2022-11-10 21:48:16
LastEditors: symlpigeon
Description: BCH编码
FilePath: /sim_bds/python/coding/bch.py
"""

# 这个讲的还挺清楚 http://staff.ustc.edu.cn/~wyzhou/ct_chapter3.pdf

from typing import Tuple

import numpy as np


def uint8_swar(x: np.uint8) -> np.uint8:
    """统计一个uint8的1的个数
    Variable-Precision SWAR Algorithm, 好厉害

    Args:
        x (np.uint8): 待统计的数

    Returns:
        int: 1的个数
    """
    x = np.uint8((x & 0x55) + ((x >> 1) & 0x55))
    x = np.uint8((x & 0x33) + ((x >> 2) & 0x33))
    x = np.uint8((x & 0x0F) + ((x >> 4) & 0x0F))
    return x


def reg_shl(reg: np.ndarray, k: int) -> Tuple[np.ndarray, int]:
    """寄存器左移位

    Args:
        reg (np.ndarray): 寄存器数组, dtype=np.uint8
        k (int): 长度 bit

    Returns:
        np.ndarray: 位移之后的寄存器
    """
    byte_length = k // 8 + (0 if k % 8 == 0 else 1)
    out_bit = (reg[0] >> 7) & 0x1
    for idx in range(byte_length - 1):
        reg[idx] <<= 1
        reg[idx] |= (reg[idx + 1] >> 7) & 0x1
    reg[byte_length - 1] <<= 1
    return reg, int(out_bit)


def reg_feedback(reg: np.ndarray, g: np.ndarray, k: int) -> int:
    """寄存器反馈

    Args:
        reg (np.ndarray): 寄存器, dtype=np.uint8
        g (np.ndarray): 本原多项式, dtype=np.uint8
        k (int): 寄存器宽度 bit

    Returns:
        int: 反馈值
    """
    feedback_cnt = 0
    byte_length = k // 8 + (0 if k % 8 == 0 else 1)
    for idx in range(byte_length):
        feedback_cnt += uint8_swar(reg[idx] & g[idx])
    return feedback_cnt & 0x1


def bch_enc(data: bytes, g: int, n: int, k: int) -> bytes:
    """BCH 编码

    Args:
        data (bytes): 待编码数据
        g (int): 本原多项式的系数们组成的二进制序列, MSB在前
        n (int): BCH码的长度 bit
        k (int): BCH码的数据长 bit

    Returns:
        bytes: 编码结果
    """
    # Reg stores the state of the shift register, MSB
    reg = np.array(list(data), dtype=np.uint8)
    if k % 8 != 0:
        reg[k // 8] <<= 8 - k % 8
    # reverse the order of bits in each byte
    bin_g = bin(g)[2:][::-1]
    if len(bin_g) % 8 != 0:
        bin_g += "0" * (8 - len(bin_g) % 8)
    poly = np.array(
        [int(bin_g[i : i + 8], 2) for i in range(0, len(bin_g), 8)], dtype=np.uint8
    )

    ans = 0
    for _ in range(n):
        feedback = reg_feedback(reg, poly, k)
        reg, out_bit = reg_shl(reg, k)
        reg[k // 8 + (0 if k % 8 == 0 else 1) - 1] |= feedback << ((8 - k % 8) % 8)
        ans = (ans << 1) | out_bit
    return ans.to_bytes(n // 8 + 1, "big")


def bch_21_6_enc(data: bytes) -> bytes:
    """BCH(21, 6) 编码
    BCH(21,6), n = 21, k = 6, t = 3, d = 7 (查7纠3)
    属于非本源BCH码, 生成多项式g(x) = x^6+x^4+x^2+x+1

    Args:
        data (bytes): 待编码数据

    Returns:
        bytes: 编码数据
    """
    g = 0b1010111
    return bch_enc(data, g, 21, 6)


def bch_51_8_enc(data: bytes) -> bytes:
    """BCH(51, 8)编码
    BCH(51, 8), n = 51, k = 8
    生成多项式 g(x) = x^8 + x^7 + x^4 + x^3 + x^2 + x + 1

    Args:
        data (bytes): 待编码数据

    Returns:
        bytes: 编码数据
    """
    g = 0b110011111
    return bch_enc(data, g, 51, 8)


def bch_15_11_enc(data:bytes) -> bytes:
    """BCH(15,11,1)编码
    BCH(15,11,1) n=15, k=11, t=1
    生成多项式 g(x) = x^4 + x + 1

    Args:
        data (bytes): 待编码数据

    Returns:
        bytes: 编码数据
    """
    g = 0b10011
    return bch_enc(data, g, 15, 11)


if __name__ == "__main__":
    with open("bch_test/bch_enc.csv", "r") as f:
        data = f.read()
    data = data.split("\n")
    while "" in data:
        data.remove("")
    raw_bch21 = data[0:4]
    raw_bch51 = data[4:]

    bch21 = []
    for lines in raw_bch21:
        bchdata = lines.split(",")
        for item in bchdata:
            bch21.append(int(item[2:], 16))
    bch51 = []
    for lines in raw_bch51:
        bchdata = lines.split(",")
        for item in bchdata:
            bch51.append(int(item[2:], 16))

    for i in range(0, 2**6):
        a = int.from_bytes(bch_21_6_enc(i.to_bytes(1, "big")), "big")
        b = bch21[i]
        assert a == b, f"Error {i}, expected {b}, got {a}"
    for i in range(0, 2**8):
        a = int.from_bytes(bch_51_8_enc(i.to_bytes(1, "big")), "big")
        b = bch51[i]
        assert a == b, f"Error {i}, expected {b}, got {a}"
