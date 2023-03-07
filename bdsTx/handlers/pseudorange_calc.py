"""
Author: symlPigeon 2163953074@qq.com
Date: 2023-02-16 15:42:12
LastEditTime: 2023-02-16 16:21:01
LastEditors: symlPigeon 2163953074@qq.com
Description: 生成伪距计算结果
FilePath: /bds-Sim/bdsTx/handlers/pseudorange_calc.py
"""

from typing import Tuple

from bdsTx.satellite_info.coordinate_system import lla2ecef
from bdsTx.satellite_info.pseudorange import get_pseudo_range


class pseudoRangeGenerator:
    def __init__(
        self,
        ephemeris: dict,
        iono_data: dict | list,
        carrier_freq: float,
        pos: Tuple[float, float, float],
        curr_time: float,
        model: str = "bdgim",
    ):
        """初始化伪距计算器

        Args:
            ephemeris (dict): 星历数据，针对当前卫星
            iono_data (dict): 电离层模型
            carrier_freq (float): 载波频率
            pos (Tuple[float, float, float]): 接收机位置，should be llh
            curr_time (float): 当前时间
            model (str, optional): 电离层校正模型选择. Defaults to "bdgim".
        """
        self._eph = ephemeris
        self._iono_data = iono_data
        self._carrier_freq = carrier_freq
        self._pos = lla2ecef(*pos)
        self._curr_time = curr_time
        self._model = model

    def get_pseudo_range(self) -> float:
        """计算伪距

        Returns:
            float: 伪距
        """
        return get_pseudo_range(
            self._eph,
            self._iono_data,
            self._carrier_freq,
            self._pos,
            self._curr_time,
            self._model,
        )

    def get_ref_pseudo_range(self) -> float:
        """计算参考伪距

        Returns:
            float: 伪距
        """
        return get_pseudo_range(
            self._eph,
            self._iono_data,
            self._carrier_freq,
            (0, 0, 0,),
            self._curr_time,
            self._model
        )