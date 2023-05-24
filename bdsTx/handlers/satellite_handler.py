"""
Author: symlPigeon 2163953074@qq.com
Date: 2023-02-16 14:36:05
LastEditTime: 2023-03-28 13:48:55
LastEditors: symlPigeon 2163953074@qq.com
Description: 输出卫星信息和数据帧
FilePath: /bds-Sim/bdsTx/handlers/satellite_handler.py
"""

from __future__ import annotations

import logging
from typing import List, Tuple

from bdsTx.handlers.alc_reader import almanacReader
from bdsTx.handlers.eph_reader import ephemerisReader
from bdsTx.handlers.iono_corr_loader import ionoCorrReader
from bdsTx.handlers.ldpc_loader import ldpcLoader
from bdsTx.handlers.msg_generator import messageGenerator
from bdsTx.handlers.ranging_code_loader import rangingCodeReader
from bdsTx.handlers.sat_selector import satelliteSelector
from bdsTx.satellite_info.broadcast_type import SIGNAL_TYPE
from bdsTx.satellite_info.constants import *
from bdsTx.satellite_info.coordinate_system import lla2ecef
from bdsTx.satellite_info.detect_sat_type import detect_sat_type


class satelliteHandler:
    def __init__(self):
        """construction of satelliteHandler"""
        self._pos = (0.0, 0.0, 0.0)
        self._time = 0.0
        self._signal_type = 0
        self._broadcast_time = 0.0
        self._eph_path = ""
        self._alc_path = ""
        self._iono_path = ""
        self._prn_path = ""
        self._ldpc_paths = ""
        self._eph = {}
        self._alc = {}
        self._available_sats = []
        self._ldpc_mats = []

    def set_position(self, pos: Tuple[float, float, float]) -> satelliteHandler:
        """设置接收机位置

        Args:
            pos (Tuple[float, float, float]): 经纬度、高度

        Returns:
            satelliteHandler: _description_
        """
        self._pos = pos
        return self

    def set_time(self, time: float) -> satelliteHandler:
        """设置时间

        Args:
            time (float): 时间，UTC时间戳

        Returns:
            satelliteHandler: _description_
        """
        self._time = time
        return self

    def set_signal_type(self, signal_type: int) -> satelliteHandler:
        """设置信号类型

        Args:
            signal_type (int): 应该是SIGNAL_TYPE中的某一个

        Returns:
            satelliteHandler: _description_
        """
        self._signal_type = signal_type
        return self

    def set_broadcast_time(self, broadcast_time: float) -> satelliteHandler:
        """设置播发的时间，用于生成数据的长度

        Args:
            broadcast_time (float): 播发时间，单位是秒

        Returns:
            satelliteHandler: _description_
        """
        self._broadcast_time = broadcast_time
        return self

    def set_eph_path(self, eph_path: str) -> satelliteHandler:
        """设置星历文件的路径

        Args:
            eph_path (str): 星历文件的路径

        Returns:
            satelliteHandler: _description_
        """
        self._eph_path = eph_path
        return self

    def set_alc_path(self, alc_path: str) -> satelliteHandler:
        """设置历书文件的路径

        Args:
            alc_path (str): 历书文件的路径，注意这是B1I/B3I需要的

        Returns:
            satelliteHandler: _description_
        """
        self._alc_path = alc_path
        return self

    def set_iono_path(self, iono_path: str) -> satelliteHandler:
        """设置电离层矫正数据的路径

        Args:
            iono_path (str): 电离层矫正数据json文件的路径

        Returns:
            satelliteHandler: _description_
        """
        self._iono_path = iono_path
        return self

    def set_prn_path(self, prn_path: str) -> satelliteHandler:
        """设置PRN号的路径，应该是包含了b1c/b1i/b3i/b2a四个子文件夹的路径

        Args:
            prn_path (str): PRN的路径

        Returns:
            satelliteHandler: _description_
        """
        self._prn_path = prn_path
        return self

    def set_ldpc_path(self, ldpc_path: List[str]) -> satelliteHandler:
        """设置ldpc码的路径，这是B1C/B2a需要的

        Args:
            ldpc_path (List[str]): LDPC矩阵的路径

        Returns:
            satelliteHandler: _description_
        """
        self._ldpc_paths = ldpc_path
        return self

    def load_prn(self) -> satelliteHandler:
        """初始化测距码读取类

        Returns:
            satelliteHandler: _description_
        """
        if self._prn_path == "":
            raise ValueError("PRN file path not set")
        self._prn_reader = rangingCodeReader(self._prn_path)
        return self

    def load_ldpc_mats(self) -> satelliteHandler:
        """加载LDPC矩阵，B1C/B2a需要

        Raises:
            ValueError: 需要先设置好LDPC矩阵的路径

        Returns:
            satelliteHandler: _description_
        """
        if self._ldpc_paths == []:
            raise ValueError("LDPC file path not set")
        for ldpc_path in self._ldpc_paths:
            ldpc_loader = ldpcLoader(ldpc_path)
            self._ldpc_mats.append(ldpc_loader.get())
        return self

    def load_eph(self) -> satelliteHandler:
        """加载星历数据

        Raises:
            ValueError: 需要先设置好星历文件路径

        Returns:
            satelliteHandler: _description_
        """
        if self._eph_path == "":
            raise ValueError("ephemeris file path not set")
        eph_reader = ephemerisReader(self._eph_path)
        self._eph = eph_reader.get_ephemeris()
        return self

    def load_alc(self) -> satelliteHandler:
        """加载历书数据

        Raises:
            ValueError: 需要提前设置好历书文件的路径

        Returns:
            satelliteHandler: _description_
        """
        if self._alc_path == "":
            raise ValueError("almanac file path not set")
        alc_reader = almanacReader(self._alc_path)
        self._alc = alc_reader.getAlmanac()
        return self

    def load_iono_corr(self) -> satelliteHandler:
        """加载电离层数据

        Raises:
            ValueError: 需要提前设置好电离层校正文件的路径

        Returns:
            satelliteHandler: _description_
        """
        if self._iono_path == "":
            raise ValueError("ionosphere correction file path not set")
        self._iono_corr = ionoCorrReader(self._iono_path)
        return self

    def find_satellite(self) -> satelliteHandler:
        """寻找可见星

        Raises:
            ValueError: _description_

        Returns:
            satelliteHandler: _description_
        """
        if self._eph == {}:
            raise ValueError("ephemeris not loaded!")
        sat_finder = satelliteSelector(self._eph)
        self._available_sats = sat_finder.select(
            self._time, self._pos, self._signal_type
        ).get_satellites()
        return self

    def init_msg_gen(self) -> satelliteHandler:
        """初始化消息生成器

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            satelliteHandler: _description_
        """
        self._sat_msg_generator = messageGenerator(
            self._available_sats, self._signal_type
        )
        match self._signal_type:
            case SIGNAL_TYPE.B1C_SIGNAL:
                if len(self._ldpc_mats) < 2:
                    raise ValueError("LDPC matrix not set properly!")
                args = {
                    "ldpc_mat_1": self._ldpc_mats[0],
                    "ldpc_mat_2": self._ldpc_mats[1],
                    "iono_corr": self._iono_corr.get_bdgim(),
                    "frame_order": [
                        1
                    ],  # FIXME: Set this value according to the real-world situtation
                    "pos": lla2ecef(*self._pos),
                }
            case SIGNAL_TYPE.B2A_SIGNAL:
                # NOT IMPLEMENTED YET
                args = {}
            case SIGNAL_TYPE.B1I_SIGNAL | SIGNAL_TYPE.B3I_SIGNAL:
                args = {
                    "iono_corr": self._iono_corr.get_klobuchar(),
                    "almanac": self._alc,
                    "pos": lla2ecef(*self._pos),
                }
            case _:
                raise ValueError("Invalid signal type!")
        self._sat_msg_gen_args = args
        return self

    def generate(self) -> list:
        datas = []
        msgs = self._sat_msg_generator.gen_message(
            self._time, self._broadcast_time, self._sat_msg_gen_args
        )
        
        for prn in msgs:
            prn_info = rangingCodeReader(self._prn_path).read(prn, self._signal_type)
            data = {
                "data": msgs[prn]["data"],
                "type": detect_sat_type(prn),
                "delay": msgs[prn]["delay"],
                "refDelay": msgs[prn]["refDelay"],
                "elevation": msgs[prn]["elevation"],
            }
            data.update(prn_info)
            datas.append(data)
        return datas


if __name__ == "__main__":
    import json
    import time

    logging.basicConfig(level=logging.DEBUG)
    handler = satelliteHandler()
    handler.set_alc_path(
        "bdsTx/satellite_info/almanac/tarc0190.23alc.json"
    ).set_eph_path("bdsTx/satellite_info/ephemeris/tarc0140.json")
    handler.set_time(time.time()).set_position((120, 30, 0)).set_broadcast_time(300)
    handler.set_iono_path("bdsTx/satellite_info/ionosphere/iono_corr.json")
    handler.set_prn_path("bdsTx/coding/ranging_code/")
    handler.set_signal_type(SIGNAL_TYPE.B1I_SIGNAL)
    handler.load_alc().load_eph().load_iono_corr().load_prn().find_satellite().init_msg_gen()
    msg = handler.generate()
    with open("msg.json", "w") as f:
        f.write(json.dumps(msg, indent=4))
