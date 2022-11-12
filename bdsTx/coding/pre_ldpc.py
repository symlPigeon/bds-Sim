"""
Author: symlpigeon
Date: 2022-11-11 19:17:07
LastEditTime: 2022-11-11 19:17:09
LastEditors: symlpigeon
Description: 子帧进行LDPC编码时是以6bit为单位的,而在内存里显然以8bit为单位更方便,所以需要进行转换
FilePath: /bdsTx/coding/pre_ldpc.py
"""

import numpy as np


def pre_ldpc_enc(data: bytes, in_bit_len: int) -> np.ndarray:
    """将8字节一组的数据转换为6bit一组的数据

    Args:
        data (bytes): 子帧的原始数据
        in_bit_len (int): 子帧的原始长度

    Returns:
        np.ndarray: 编码后的数据
    """
    assert in_bit_len % 6 == 0, "Invalid in_bit_len!"
    out_bin_len = in_bit_len // 6
    out = np.zeros((out_bin_len,), dtype=np.uint8)
    # 3 * 8 = 4 * 6
    for idx in range(in_bit_len // (8 * 3)):
        # +--------+--------+--------+
        # |######## ######## ########|
        # +--------+--------+--------+
        #  ******&& &&&&^^^^ ^^%%%%%%

        out[idx * 4] = (data[idx * 3] >> 2) & 0x3F
        out[idx * 4 + 1] = (
            ((data[idx * 3] & 0x3) << 4) | ((data[idx * 3 + 1] >> 4) & 0xF)
        ) & 0x3F
        out[idx * 4 + 2] = (
            ((data[idx * 3 + 1] & 0x1F) << 2) | ((data[idx * 3 + 2] >> 6) & 0x3)
        ) & 0x3F
        out[idx * 4 + 3] = data[idx * 3 + 2] & 0x3F
    return out


if __name__ == "__main__":
    import random

    for _ in range(100):
        length = random.randint(10, 12) * 6
        data = bytes([random.randint(0, 255) for _ in range(length)])
        data_str = "".join([f"{x:08b}" for x in data])
        convert_data = pre_ldpc_enc(data, length * 8)
        convert_data_str = "".join([f"{x:06b}" for x in convert_data])
        assert data_str == convert_data_str, "Error!\n {} \n {}".format(
            data_str, convert_data_str
        )
