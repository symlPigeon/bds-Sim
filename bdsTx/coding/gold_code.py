'''
Author: symlpigeon
Date: 2023-01-08 14:42:57
LastEditTime: 2023-01-08 20:46:44
LastEditors: symlpigeon
Description: Generate Gold Code
FilePath: /bds-Sim/bdsTx/coding/gold_code.py
'''


# Gold 序列由两个LFSR G1和G2生成，其中
# G1 111110000011(MSB first)
# G2 101100111111(MSB first)
# 初始相位均为01010101010


from typing import List

import numpy as np

from bdsTx.coding.lfsr import LFSR, uint32_swar

GOLD_CODE_G1_COEF = 0b10000011111
GOLD_CODE_G2_COEF = 0b11111001101
GOLD_CODE_INIT_PHASE = 0b01010101010
GOLD_CODE_LENGTH = 2046


def generate_gold_code(phases: List[int]) -> str:
    # init LFSR
    G1 = LFSR(11, GOLD_CODE_G1_COEF, GOLD_CODE_INIT_PHASE)
    G2 = LFSR(11, GOLD_CODE_G2_COEF, GOLD_CODE_INIT_PHASE)
    # the phase selector of G2
    phase_selector = 0
    for phase in phases:
        phase_selector += 1 << (11 - phase)
    phase_selector &= 0x7ff
    code = ""
    for _ in range(GOLD_CODE_LENGTH):
        code += str(G1.get() ^ (uint32_swar(np.uint32((G2.get_status() & phase_selector) & 0x7ff)) & 0x1))
        # shift G2
        _ = G2.get()
    return code