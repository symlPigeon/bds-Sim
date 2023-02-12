"""
Author: symlpigeon
Date: 2023-01-08 14:42:57
LastEditTime: 2023-01-10 20:18:26
LastEditors: symlpigeon
Description: Generate Gold Code
FilePath: /bds-Sim/bdsTx/coding/gold_code.py
"""


# Gold 序列由两个LFSR G1和G2生成，其中
# G1 111110000011(MSB first)
# G2 101100111111(MSB first)
# 初始相位均为01010101010


from typing import List

import numpy as np

from bdsTx.coding.lfsr import LFSR, uint32_swar

B1I_GOLD_CODE_G1_COEF = 0b11111000001
B1I_GOLD_CODE_G2_COEF = 0b10110011111
B1I_GOLD_CODE_INIT_PHASE = 0b01010101010
B1I_GOLD_CODE_LENGTH = 2046

B3I_GOLD_CODE_G1_COEF = 0b1000000001101
B3I_GOLD_CODE_G2_COEF = 0b1101101110001
B3I_GOLD_CODE_G1_INIT_PHASE = 0b1111111111111
B3I_GOLD_CODE_G1_INIT_COND_PHASE = 0b0011111111111
B3I_GOLD_CODE_LENGTH = 10230


def b1i_generate_gold_code(phases: List[int]) -> str:
    # init LFSR
    G1 = LFSR(11, B1I_GOLD_CODE_G1_COEF, B1I_GOLD_CODE_INIT_PHASE)
    G2 = LFSR(11, B1I_GOLD_CODE_G2_COEF, B1I_GOLD_CODE_INIT_PHASE)
    # the phase selector of G2
    phase_selector = 0
    for phase in phases:
        phase_selector += 1 << (phase - 1)
    phase_selector &= 0x7FF
    code = ""
    for _ in range(B1I_GOLD_CODE_LENGTH):
        code += str(
            G1.get()
            ^ (uint32_swar(np.uint32((G2.get_status() & phase_selector))) & 0x1)
        )
        # shift G2
        _ = G2.get()
    return code


def b3i_generate_gold_code(phase: int) -> str:
    # init LFSR
    G1 = LFSR(13, B3I_GOLD_CODE_G1_COEF, B3I_GOLD_CODE_G1_INIT_PHASE)
    G2 = LFSR(13, B3I_GOLD_CODE_G2_COEF, phase)
    G1_cnt = 0
    code = ""
    for _ in range(B3I_GOLD_CODE_LENGTH):
        # # Why it worked?
        # # if g1 is in init condition, init it
        
        # if G1.get_status() == B3I_GOLD_CODE_G1_INIT_COND_PHASE:
        #     #print("reset")
        #     G1.reset(B3I_GOLD_CODE_G1_INIT_PHASE)
        if G1_cnt == 8190:
            G1.reset(B3I_GOLD_CODE_G1_INIT_PHASE)
            G1_cnt = 0
        code += str(G1.get() ^ G2.get())
        G1_cnt += 1
    return code
        