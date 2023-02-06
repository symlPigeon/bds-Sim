'''
Author: symlPigeon 2163953074@qq.com
Date: 2023-02-06 14:12:29
LastEditTime: 2023-02-06 15:17:26
LastEditors: symlPigeon 2163953074@qq.com
Description: 
FilePath: /bds-Sim/signalProcess/util/constellation.py
'''

import numpy as np


def bpsk_constellation() -> np.ndarray:
    """BPSK constellation

    Returns:
        np.ndarray: BPSK constellation
    """
    # 0 -> 1, 1 -> -1
    return np.array([1, -1], dtype=np.float32)