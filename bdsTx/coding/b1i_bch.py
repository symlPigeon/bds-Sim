"""
Author: symlpigeon
Date: 2023-01-10 15:11:33
LastEditTime: 2023-01-10 20:43:14
LastEditors: symlpigeon
Description: BCH(15, 11, 1) for B1I.
FilePath: /bds-Sim/bdsTx/coding/b1i_bch.py
"""


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
        r3 = r2; r2 = r1
        r1 = r0 ^ nxt_bit
        r0 = nxt_bit
    out <<= 4
    out |= r0 | (r1 << 1) |(r2 << 2)| (r3<< 3)
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
        bit1 = (int_data1 & (0x1 << (bitlen - idx - 1))) >> (bitlen - idx - 1)
        bit2 = (int_data2 & (0x1 << (bitlen - idx - 1))) >> (bitlen - idx - 1)
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


if __name__ == "__main__":
    data = 0b010010110110000010000000.to_bytes(3, "big")
    print(bin(int.from_bytes(b1i_bch_encode(data), "big"))[2:])
    data = b"\xE2\x40\xDC\xB0"
    print(b1i_bch_encode_word_1(data).hex())
    
    # 01001011011
    # 00000100000
    # 0010000010011010001010
