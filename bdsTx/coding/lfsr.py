'''
Author: symlpigeon
Date: 2022-12-27 17:30:27
LastEditTime: 2023-01-10 21:30:49
LastEditors: symlpigeon
Description: Linear Feedback Shift Register
FilePath: /bds-Sim/bdsTx/coding/lfsr.py
'''

import numpy as np


def uint32_swar(x: np.uint32) -> np.uint32:
    """ unsigned int32 variable presicion SWAR algorithm

    Args:
        x (int): input number

    Returns:
        int: Hamming weight of input number
    """
    x = np.uint32((x & 0x55555555) + ((x >> 1) & 0x55555555))
    x = np.uint32((x & 0x33333333) + ((x >> 2) & 0x33333333))
    x = np.uint32((x & 0x0F0F0F0F) + ((x >> 4) & 0x0F0F0F0F))
    x = (x * 0x01010101) >> 24; 
    return x


class LFSR:
    def __init__(self, l: int, g: int, initial_phase: int):
        # Notice that g is a polynomial coefficient, MSB first
        self._l = l
        self._g = g
        self._reg = initial_phase
    
    def get(self) -> int:
        # The output bit is the LSB of the register
        out_bit = (self._reg & (1 << (self._l - 1))) >> (self._l - 1)
        fb_status = self._reg & self._g
        fb_val = 0
        while fb_status > 0:
            fb_val ^= uint32_swar(np.uint32(fb_status & 0xffffffff))
            fb_status >>= 32
        self._reg <<= 1
        self._reg |= fb_val & 0x1
        self._reg &= (1 << self._l) - 1
        return out_bit
    
    def get_status(self) -> int:
        return self._reg & ((1 << self._l) - 1)
    
    def run(self, cnt: int) -> str:
        ans = ""
        for _ in range(cnt):
            ans += str(self.get())
        return ans
        
        
if __name__ == "__main__":
    lfsr = LFSR(10, 0b1011100001, 0b1010101010)
    for i in range(30):
        #print(lfsr.get(), end='')
        lfsr.get()
    