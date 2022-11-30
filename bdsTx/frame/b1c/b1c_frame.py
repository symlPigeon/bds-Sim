"""
Author: symlpigeon
Date: 2022-11-10 21:46:02
LastEditTime: 2022-11-10 21:46:06
LastEditors: symlpigeon
Description: B1C帧构造
FilePath: /sim_bds/python/satellite_info/b1c_frame.py
"""

import json
from typing import List

import numpy as np
from b1c_subframe1 import encoding_subframe1, make_subframe1
from b1c_subframe2 import encoding_subframe2, make_subframe2
from b1c_subframe3 import encoding_subframe3, make_subframe3

from bdsTx.coding.interleaving import interleaving


def _mix_subframe(
    subframe1: bytes, subframe2: np.ndarray, subframe3: np.ndarray
) -> bytes:
    """把三个子帧合并成一个数据帧

    Args:
        subframe1 (bytes): 子帧1
        subframe2 (np.ndarray): 子帧2，注意子帧2和3都是ndarray，这个可以改但是没啥必要
        subframe3 (np.ndarray): 子帧3

    Returns:
        bytes: 数据帧
    """
    return subframe1 + interleaving(subframe2, subframe3)


class b1cFrame:
    """B1C Frame"""

    def __init__(
        self,
        prn: int,
        eph: dict,
        bdgim: list,
        frame_order: List[int],
        ldpc_mat_1: np.ndarray,
        ldpc_mat_2: np.ndarray
    ):
        self._prn = prn
        self._eph = eph
        self._bdgim = bdgim
        self._frame_order = frame_order
        self._subframe3idx = 0
        self._ldpc_mat_1 = ldpc_mat_1
        self._ldpc_mat_2 = ldpc_mat_2

    def get_prn(self):
        """get Prn"""
        return self._prn

    def get_eph(self):
        """get Ephemeris"""
        return self._eph

    def get_bdgim(self):
        """get BDGIM"""
        return self._bdgim

    def get_frame_order(self):
        """get frame order for subframe3"""
        return self._frame_order

    def make_frame(self, curr_time: float) -> bytes:
        """生成B1C帧"""
        subframe1 = make_subframe1(self._prn, curr_time)
        subframe2 = make_subframe2(curr_time, self._eph)
        subframe3 = make_subframe3(
            self._eph, self._bdgim, self._frame_order[self._subframe3idx]
        )
        self._subframe3idx = (self._subframe3idx + 1) % len(self._frame_order)
        subframe1 = encoding_subframe1(subframe1)
        subframe2 = encoding_subframe2(subframe2, self._ldpc_mat_1)
        subframe3 = encoding_subframe3(subframe3, self._ldpc_mat_2)
        return _mix_subframe(subframe1, subframe2, subframe3)


if __name__ == "__main__":
    import json
    import time

    from bdsTx.coding.ldpc_mat import ldpcMat_44_88, ldpcMat_100_200
    eph = json.load(open("../../satellite_info/ephemeris/tarc3130.22b.json", "r"))["22"]["2022-11-09_12:00:00"]
    bdgim = json.load(open("../../../bdsTx/satellite_info/ionosphere/iono_corr.json", "r", encoding="utf-8"))
    bdgim = bdgim["bdgim"]["a"]["alpha"]
    mat1 = json.load(open("../../coding/ldpc_mat_gen/ldpc_matG_100_200.json", "r"))
    mat2 = json.load(open("../../coding/ldpc_mat_gen/ldpc_matG_44_88.json", "r"))
    frame_maker = b1cFrame(22, eph, bdgim, [1], mat1, mat2)
    frame = frame_maker.make_frame(time.time())
    hex_frame = ""
    for i in frame:
        hex_frame += f"{i:02x}"
    print(hex_frame)
    print(len(hex_frame))