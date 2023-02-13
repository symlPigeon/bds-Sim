'''
Author: symlPigeon 2163953074@qq.com
Date: 2023-02-13 11:17:51
LastEditTime: 2023-02-13 12:33:11
LastEditors: symlPigeon 2163953074@qq.com
Description: Select satellite for PVT calculation
FilePath: /bds-Sim/bdsTx/handlers/sat_selector.py
'''

import logging
from typing import List, Tuple

from bdsTx.satellite_info.broadcast_type import *
from bdsTx.satellite_info.detect_sat_type import *
from bdsTx.satellite_info.visible_satellite_searcher import get_visible_satellite


class satelliteSelector:
    def __init__(self, ephemeris: dict):
        """可见星选择器

        Args:
            ephemeris (dict): 星历文件
        """
        self._eph = ephemeris
        self._valid_sats = []
        
    def select(self, time: float, pos: Tuple[float, float, float], broadcast_type: int) -> None:
        """选择播发的卫星

        Args:
            time (float): 当前时间
            pos (Tuple[float, float, float]): 需要定位的位置
            broadcast_type (int): 广播类型

        Returns:
            None
        """
        if broadcast_type not in SIGNAL_TYPE.SUPPORT_SIGNAL_TYPE:
            # 要是广播类型不支持的话就返回空
            logging.error("Unsupported broadcast type: %d" % broadcast_type)
            self._valid_sats = []
            return
        self._valid_sats = []
        # 暂时我们还是用默认的可视角吧
        visible_sats = get_visible_satellite(self._eph, pos, time)
        for eph in visible_sats:
            if is_signal_able_to_tx(eph, broadcast_type):
                self._valid_sats.append(eph)
        
        
    def get_satellites(self) -> List[dict]:
        """获取可用的卫星

        Returns:
            List[dict]: 包含可用卫星信息的列表
        """
        return self._valid_sats