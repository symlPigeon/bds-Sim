"""
Author: symlpigeon
Date: 2022-11-11 19:15:19
LastEditTime: 2022-11-11 19:15:21
LastEditors: symlpigeon
Description: 块交织
FilePath: /bdsTx/coding/interleaving.py
"""

import numpy as np


def interleaving(subframe2: np.ndarray, subframe3: np.ndarray) -> bytes:
    mat = np.zeros((36, 48 // 8), dtype=np.uint8)
    # 写入22行子帧2和11行子帧3
    for ridx in range(11):
        # 一共六列, 分两组
        for cidx in range(2):
            mat[ridx * 3, cidx * 3] = ((subframe2[ridx * 16 + cidx] << 2) & 0xFC) | (
                (subframe2[ridx * 16 + cidx + 1] >> 4) & 0x3
            )
            mat[ridx * 3, cidx * 3 + 1] = (
                (subframe2[ridx * 16 + cidx + 1] << 4) & 0xF0
            ) | ((subframe2[ridx * 16 + cidx + 2] >> 2) & 0xF)
            mat[ridx * 3, cidx * 3 + 2] = (
                (subframe2[ridx * 16 + cidx + 2] << 6) & 0xC0
            ) | (subframe2[ridx * 16 + cidx + 3] & 0x3F)

            mat[ridx * 3 + 1, cidx * 3] = (
                (subframe2[ridx * 16 + cidx + 4] << 2) & 0xFC
            ) | ((subframe2[ridx * 16 + cidx + 5] >> 4) & 0x3)
            mat[ridx * 3 + 1, cidx * 3 + 1] = (
                (subframe2[ridx * 16 + cidx + 5] << 4) & 0xF0
            ) | ((subframe2[ridx * 16 + cidx + 6] >> 2) & 0xF)
            mat[ridx * 3 + 1, cidx * 3 + 2] = (
                (subframe2[ridx * 16 + cidx + 6] << 6) & 0xC0
            ) | (subframe2[ridx * 16 + cidx + 7] & 0x3F)

            mat[ridx * 3 + 2, cidx * 3] = ((subframe3[ridx * 2 + cidx] << 2) & 0xFC) | (
                (subframe3[ridx * 2 + cidx + 1] >> 4) & 0x3
            )
            mat[ridx * 3 + 2, cidx * 3 + 1] = (
                (subframe3[ridx * 2 + cidx + 1] << 4) & 0xF0
            ) | ((subframe3[ridx * 2 + cidx + 2] >> 2) & 0xF)
            mat[ridx * 3 + 2, cidx * 3 + 2] = (
                (subframe3[ridx * 2 + cidx + 2] << 6) & 0xC0
            ) | (subframe3[ridx * 2 + cidx + 3] & 0x3F)

    for ridx in range(33, 36):
        for cidx in range(2):
            mat[ridx, cidx * 3] = (
                (subframe2[ridx * 8 - 11 * 8 + cidx * 2] << 2) & 0xFC
            ) | ((subframe2[ridx * 8 - 11 * 8 + cidx * 2 + 1] >> 4) & 0x3)
            mat[ridx, cidx * 3 + 1] = (
                (subframe2[ridx * 8 - 11 * 8 + cidx * 2 + 1] << 4) & 0xF0
            ) | ((subframe2[ridx * 8 - 11 * 8 + cidx * 2 + 2] >> 2) & 0xF)
            mat[ridx, cidx * 3 + 2] = (
                (subframe2[ridx * 8 - 11 * 8 + cidx * 2 + 2] << 6) & 0xC0
            ) | (subframe2[ridx * 8 - 11 * 8 + cidx * 2 + 3] & 0x3F)
    print(mat)

    out = np.zeros(36 * 6, dtype=np.uint8)
    for col in range(48):
        for row in range(36):
            out_idx = 36 * col + row
            out_byte_idx = out_idx // 8
            out_bit_idx = out_idx % 8
            out[out_byte_idx] |= ((mat[row, col // 8] >> (7 - col % 8)) & 1) << (
                7 - out_bit_idx
            )
    return out.tobytes()


if __name__ == "__main__":
    # from pre_ldpc import pre_ldpc_enc
    # from ldpc import ldpc64
    # from ldpc_mat import ldpcMat_100_200, ldpcMat_44_88
    # import random

    # ldpc_subframe2 = ldpcMat_100_200()
    # ldpc_subframe3 = ldpcMat_44_88()
    # subframe2 = bytearray([random.randint(0, 255) for _ in range(600 // 8)])
    # subframe3 = bytearray([random.randint(0, 255) for _ in range(264 // 8)])
    # enc_subframe2 = ldpc64(ldpc_subframe2.mat(), pre_ldpc_enc(subframe2, 600))
    # enc_subframe3 = ldpc64(ldpc_subframe3.mat(), pre_ldpc_enc(subframe3, 264))
    # ans = interleaving(enc_subframe2, enc_subframe3)
    # print(ans)
    subframe1 = np.array([0b101010 for _ in range(200)], dtype=np.uint8)
    subframe2 = np.array([0b101010 for _ in range(88)], dtype=np.uint8)
    print(interleaving(subframe1, subframe2))
