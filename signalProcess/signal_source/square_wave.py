'''
Author: symlPigeon 2163953074@qq.com
Date: 2023-02-05 16:58:26
LastEditTime: 2023-02-05 17:30:25
LastEditors: symlPigeon 2163953074@qq.com
Description: 方波信号源
FilePath: /bds-Sim/signalProcess/signal_source/square_wave.py
'''

import numpy as np


def square_wave(A: np.float32, f: np.float32, phi_0: np.float32, fs: np.float32, T: np.float32) -> np.ndarray:
    """方波信号源

    Args:
        A (float): 振幅
        f (float): 频率
        phi_0 (float): 初相
        fs (float): 采样率
        T (float): 采样时间

    Returns:
        np.ndarray: 采样数据
    """
    t = np.arange(0, T, 1 / fs, dtype=np.float32)
    return A * np.sign(np.sin(2 * np.pi * f * t + phi_0))


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    fs = np.float32(2e3)
    A = np.float32(1)
    f = np.float32(100)
    phi_0 = np.float32(np.pi / 4)
    T = np.float32(0.1)
    data = square_wave(A, f, phi_0, fs, T)
    plt.plot(data)
    plt.show()