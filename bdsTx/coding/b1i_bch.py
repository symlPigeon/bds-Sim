"""
Author: symlpigeon
Date: 2023-01-10 15:11:33
LastEditTime: 2023-01-10 20:43:14
LastEditors: symlpigeon
Description: BCH(15, 11, 1) for B1I.
FilePath: /bds-Sim/bdsTx/coding/b1i_bch.py
"""

# NOTE: 最初预期是所有的返回值均采用bytes进行传递，然而电文中大量的数据均不是8bits对齐的，这导致了这里的实现给后面的实现带来了巨大的麻烦。


def bch_15_11_enc(data: bytes) -> bytes:
    """BCH(15, 11, 1)编码
    NOTE: 这里理论上应该能够使用bch.py中的方法来实现的，但是实际上遇到了各种问题
    g(x) = x^4 + x + 1
                                            +--------+
    +-----------------+-------------------- | gate-1 | <-----------+
    |                 |                     +--------+             |
    |    +----+       v       +----+      +----+      +----+       |       +--------+
    +--> | r0 | ---> xor ---> | r1 | ---> | r2 | ---> | r3 | ---> xor ---> | gate-2 | ---+
         +----+               +----+      +----+      +----+       ^       +--------+    |
                                                                   |                     |
                                                 input data -------+-------------------> or ---> output
    Args:
        data (bytes): 待编码数据, 11-bits

    Returns:
        bytes: 编码结果
    """
    int_data = bytes2long(data)
    # 初始化4个寄存器
    r0, r1, r2, r3 = 0, 0, 0, 0
    out = 0
    # 将数据输入寄存器中
    for i in range(11):
        # 前11个周期，gate2关闭，gage1打开
        outbit = (int_data & (0x1 << (10 - i))) >> (10 - i)
        out <<= 1
        out += outbit
        nxt_bit = r3 ^ outbit
        r3 = r2
        r2 = r1
        r1 = r0 ^ nxt_bit
        r0 = nxt_bit
    out <<= 4
    out |= r0 | (r1 << 1) | (r2 << 2) | (r3 << 3)
    return out.to_bytes(2, "big")


def bytes2long(b: bytes) -> int:
    """bytes to long

    Args:
        b (bytes): input bytes, big-endian

    Returns:
        int: output
    """
    return int.from_bytes(b, "big", signed=False)


def bitwise_parallel_to_serial(data1: bytes, data2: bytes, bitlen: int = 15) -> bytes:
    """1-bit parallel to serial conversion.

    Args:
        data1 (bytes): input data 1
        data2 (bytes): input data 2

    Returns:
        bytes: output data
    """
    out_data = 0
    int_data1 = bytes2long(data1)
    int_data2 = bytes2long(data2)
    for idx in range(bitlen):
        bit1 = ((int_data1 & (0x1 << (bitlen - idx - 1))) >> (bitlen - idx - 1)) & 0b1
        bit2 = ((int_data2 & (0x1 << (bitlen - idx - 1))) >> (bitlen - idx - 1)) & 0b1
        out_data |= (bit1 << 1) + bit2
        out_data <<= 2
    return out_data.to_bytes(4, "big")


def b1i_bch_encode(data: bytes) -> bytes:
    """The BCH(15,11,1) in B1I contains three parts:
    First, we do a 11-bits serial-parallel conversion, divide the 22-bits input into 2 parts.
    To each parts, we perform a BCH(15, 11, 1) encoding, getting two 15-bits output.
    Finally, a 1-bit parallel-serial conversion is performed, resulting to a 30-bits encoded data.

    Args:
        data (bytes): The input data, should be 22-bits.

    Returns:
        bytes: The 30-bits output data.
    """
    data_byte1 = (data[0] << 3) + ((data[1] & 0b11100000) >> 5)
    data_byte2 = ((data[1] & 0b00011111) << 6) + ((data[2] & 0b11111100) >> 2)
    enc_data_byte1 = bch_15_11_enc(data_byte1.to_bytes(2, "big"))
    enc_data_byte2 = bch_15_11_enc(data_byte2.to_bytes(2, "big"))
    return bitwise_parallel_to_serial(enc_data_byte1, enc_data_byte2)


def b1i_bch_encode_word_1(data: bytes) -> bytes:
    """This is a special case of b1i_bch_encode, the word 1 contains 26 info bits,
    which means the first 15 bits does not need to be encoded.

    Args:
        data (bytes): intput data, should be 26-bits

    Returns:
        bytes: the 30-bits output data
    """
    data_1 = ((data[0] << 7) & 0b111111110000000) + (
        ((data[1] & 0b11111110) >> 1) & 0b01111111
    )
    data_2 = (
        ((data[1] & 0b00000001) << 10)
        + ((data[2] & 0b11111111) << 2)
        + ((data[3] & 0b11000000) >> 6)
    )
    enc_data = bch_15_11_enc(data_2.to_bytes(2, "big"))
    return ((data_1 << 17) + (int.from_bytes(enc_data, "big") << 2)).to_bytes(4, "big")


def b1i_bch_encode_bin(data: str) -> str:
    """将二进制字符串形式的帧数据进行BCH编码，以及相关的交织等操作
    这里将数据类型反复转换会带来一定的损失，不过作为弥补最初设计缺陷的措施，只能姑且这样。
    WARNING: 屎山请勿随意改动

    Args:
        data (str): 待编码数据

    Returns:
        str: 二进制字符串形式的编码后的字符串
    """
    if len(data) == 26:
        # word 1
        enc_data = b1i_bch_encode_word_1(int(data + "000000", 2).to_bytes(4, "big"))
    elif len(data) == 22:
        # other words
        enc_data = b1i_bch_encode(int(data + "00", 2).to_bytes(3, "big"))
    else:
        raise Exception("Invalid data length")
    bin_enc_data = bin(int.from_bytes(enc_data, "big"))[2:]
    if len(data) == 26:
        bin_enc_data = bin_enc_data[0 : len(bin_enc_data) - 6]  # remove the right padding bits
    elif len(data) == 22:
        bin_enc_data = bin_enc_data[0 : len(bin_enc_data) - 2] # remove the right padding bits
    bin_enc_data = "0" * (30 - len(bin_enc_data)) + bin_enc_data # left padding zero
    # cut 30 bits
    return bin_enc_data[0:30]


if __name__ == "__main__":
    data = "0100101101100000100000"
    enc = b1i_bch_encode_bin(data)
    print(enc, len(enc))
    data = b"\xE2\x40\xDC\xB0"
    print(b1i_bch_encode_word_1(data).hex())
    data = b"\x03\x72"
    print(bch_15_11_enc(data).hex())

    # 01001011011
    # 00000100000
    # 0010000010011010001010
