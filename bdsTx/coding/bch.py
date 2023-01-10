"""
Author: symlpigeon
Date: 2022-11-10 21:46:25
LastEditTime: 2022-11-10 21:48:16
LastEditors: symlpigeon
Description: BCH编码
FilePath: /sim_bds/python/coding/bch.py
"""

# 这个讲的还挺清楚 http://staff.ustc.edu.cn/~wyzhou/ct_chapter3.pdf


from bdsTx.coding.lfsr import LFSR


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
    init_phase = int.from_bytes(data, "big")
    lfsr = LFSR(k, g, init_phase)
    outbits = lfsr.run(n)
    if len(outbits) % 8 != 0:
        outbits = "0" * (8 - len(outbits) % 8) + outbits
    return bytearray(int(outbits[i : i + 8], 2) for i in range(0, len(outbits), 8))


def bch_21_6_enc(data: bytes) -> bytes:
    """BCH(21, 6) 编码
    BCH(21,6), n = 21, k = 6, t = 3, d = 7 (查7纠3)
    属于非本源BCH码, 生成多项式g(x) = x^6+x^4+x^2+x+1

    Args:
        data (bytes): 待编码数据

    Returns:
        bytes: 编码数据
    """
    # FIXME: why? wtf? how?
    # g = 0b1010111
    g = 0b111010
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
    # g = 0b110011111
    g = 0b11111001
    return bch_enc(data, g, 51, 8)


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
        assert a == b, f"Error {i}, expected {bin(b)[2:]}, got {bin(a)[2:]}"
    for i in range(0, 2**8):
        a = int.from_bytes(bch_51_8_enc(i.to_bytes(1, "big")), "big")
        b = bch51[i]
        assert a == b, f"Error {i}, expected {b}, got {a}"
