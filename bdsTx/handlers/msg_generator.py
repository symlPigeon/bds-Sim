'''
Author: symlPigeon 2163953074@qq.com
Date: 2023-02-13 13:57:17
LastEditTime: 2023-03-08 20:24:50
LastEditors: symlPigeon 2163953074@qq.com
Description: 生成导航信息
FilePath: /bds-Sim/bdsTx/handlers/msg_generator.py
'''

import logging
from typing import List, Tuple

from bdsTx.frame.b1c.b1c_frame import b1cFrame
from bdsTx.frame.b1i.b1i_frame import b1iFrame
from bdsTx.handlers.ldpc_loader import ldpcLoader
from bdsTx.handlers.pseudorange_calc import pseudoRangeGenerator  # 在MSG生成部分实现伪距计算
from bdsTx.satellite_info.broadcast_type import *
from bdsTx.satellite_info.constants import *
from bdsTx.satellite_info.detect_sat_type import *
from bdsTx.satellite_info.position_calculate_by_ephemeris import (
    get_satellite_position_by_ephemeris,
)
from bdsTx.satellite_info.visible_satellite_searcher import calc_elevation_angle


class messageGenerator:
    def __init__(self, satellites: List[Tuple[int, dict]], broadcast_type: int):
        """初始化消息生成器

        Args:
            satellites (List[Tuple[int, dict]]): selector选择的部分
        """
        if len(satellites) == 0:
            logging.error("No satellite is selected. Check if the parameters are correct.")
            assert False
        if len(satellites) <= 3:
            logging.error("Too few satellites are selected. The simulation will not be able to work.")
            assert False
        if broadcast_type not in SIGNAL_TYPE.SUPPORT_SIGNAL_TYPE:
            logging.error("Unsupported broadcast type: %d" % broadcast_type)
            logging.error("Only these types are supported:")
            logging.error("  SIGNAL_TYPE.B1I -- 1")
            logging.error("  SIGNAL_TYPE.B3I -- 2")
            logging.error("  SIGNAL_TYPE.B1C -- 3")
            logging.error("  SIGNAL_TYPE.B2A -- 4 (NOT IMPLEMENTED YET)")
            assert False
        self._sats = satellites
        self._broadcast_type = broadcast_type
        
    def _gen_b1c_frame(self, curr_time: float, total_time: float, pos: Tuple[float, float, float], ldpc_mat_1: ldpcLoader, ldpc_mat_2: ldpcLoader, iono_corr: list, frame_order: List[int]) -> dict:
        ans = {}
        for i in range(4):
            prn, eph = self._sats[i]
            generator = b1cFrame(prn, eph, iono_corr, frame_order, ldpc_mat_1.get(), ldpc_mat_2.get())
            ans[prn] = {
                "data": "",
                "delay": [],
                "elevation": [],
            }
            for j in range(int(total_time / 18)):
                # 18s一个帧
                ans[prn]["data"] += generator.make_hexframe(curr_time + 18 * j)
            for j in range(int(total_time * 10)): # Sample per 0.1 seconds
                prange = pseudoRangeGenerator(eph, iono_corr, B1I_CARRIER_FREQ, pos, curr_time + 0.1 * j, model="bdgim")
                ans[prn]["delay"].append(prange.get_pseudo_range())
                satellite_pos = get_satellite_position_by_ephemeris(eph, curr_time + 0.1 * j)
                ans[prn]["elevation"].append(calc_elevation_angle(rx_pos=pos, sat_pos=satellite_pos))
            prange = pseudoRangeGenerator(eph, iono_corr, B1I_CARRIER_FREQ, pos, curr_time, model="bdgim")
            ans[prn]["refDelay"] = (prange.get_ref_pseudo_range())
        return ans
    
    def _gen_b1i_frame(self, curr_time: float, total_time: float, pos: Tuple[float, float, float], iono_corr: dict, almanac: dict) -> dict:
        ans = {}
        cnt = 0
        try:
            while cnt < len(self._sats):
                prn, eph = self._sats[cnt]
                if detect_sat_type(prn) == SAT_TYPE.SAT_TYPE_GEO:
                    logging.warning("Satellite %d is a GEO satellite" % prn)
                    logging.warning("  which broadcasts D2 message, is not implemented yet!")
                    cnt += 1 # Update the counter
                    continue
                ans[prn] = {
                    "data": "",
                    "delay": [],
                    "elevation": [],
                }
                generator = b1iFrame(prn, eph, iono_corr, almanac)
                for j in range(int(total_time / 30)):
                    # 30s一个帧
                    ans[prn]["data"] += generator.make_hexframe(curr_time + 30 * j)
                for j in range(int(total_time * 10)): # Sample pesudo range every 0.1s
                    # FIXME: B3I carrier frequency is different, which will cause a different pseudorange
                    # Creating a new method for B3I!
                    prange = pseudoRangeGenerator(eph, iono_corr, B1I_CARRIER_FREQ, pos, curr_time + 0.1 * j, model="klobuchar")
                    ans[prn]["delay"].append(prange.get_pseudo_range())
                    satellite_pos = get_satellite_position_by_ephemeris(eph, curr_time + 0.1 * j)
                    ans[prn]["elevation"].append(calc_elevation_angle(rx_pos=pos, sat_pos=satellite_pos))
                    
                prange = pseudoRangeGenerator(eph, iono_corr, B1I_CARRIER_FREQ, pos, curr_time, model="klobuchar")
                ans[prn]["refDelay"] = prange.get_ref_pseudo_range()
                cnt += 1
        except IndexError as e:
            logging.error("Ooops! It seems that there're not enough MEO and IGSO satellites.")
            return {}
        return ans
    
    def gen_message(self, curr_time: float, total_time: float, args: dict) -> dict:
        """生成导航电文

        Args:
            curr_time (float): 当前的UTC时间
            total_time (float): 需要播发的总时间，秒为单位
            args (dict): 附加信息
            对于B1C来说，需要提供以下信息：
            {
                ldpc_mat_1: ldpc_loader, // LDPC(100, 200)矩阵
                ldpc_mat_2: ldpc_loader, // LDPC(44,88)矩阵
                iono_corr: list, // BDGIM模型参数
                frame_order: List[int] // 不同帧的顺序
                pos: Tuple[float, float, float] // 接收机位置
            }
            对于B1I/B3I，你需要提供这些信息：
            {
                iono_corr: dict, // Klobuchar模型参数
                almanac: dict, // 历书数据
                pos: Tuple[float, float, float] // 接收机位置
            }

        Returns:
            dict: _description_
        """
        try:
            match self._broadcast_type:
                case SIGNAL_TYPE.B1C_SIGNAL:
                    ldpc_mat_1 = args["ldpc_mat_1"]
                    ldpc_mat_2 = args["ldpc_mat_2"]
                    iono_corr = args["iono_corr"]
                    frame_order = args["frame_order"]
                    pos = args["pos"]
                    return self._gen_b1c_frame( curr_time, total_time, pos, ldpc_mat_1, ldpc_mat_2, iono_corr, frame_order)
                case SIGNAL_TYPE.B1I_SIGNAL:
                    iono_corr = args["iono_corr"]
                    almanac = args["almanac"]
                    pos = args["pos"]
                    return self._gen_b1i_frame(curr_time, total_time, pos, iono_corr, almanac)
                case SIGNAL_TYPE.B3I_SIGNAL:
                    iono_corr = args["iono_corr"]
                    almanac = args["almanac"]
                    pos = args["pos"]
                    return self._gen_b1i_frame(curr_time, total_time, pos, iono_corr, almanac)
                case SIGNAL_TYPE.B2A_SIGNAL:
                    logging.error("Not Implemented yet :(")
                    return {}
                case _:
                    # this should never happen
                    return {}
        except KeyError as e:
            logging.error("Missing argument: %s" % e)
            logging.error("You should pass the arguments like below:")
            logging.error("""For B1C
            {
                'ldpc_mat_1': ldpc_loader, // LDPC(100, 200)矩阵
                'ldpc_mat_2': ldpc_loader, // LDPC(44,88)矩阵
                'iono_corr': list, // BDGIM模型参数
                'frame_order': List[int], // 不同帧的顺序
                'pos': Tuple[float, float, float] // 接收机位置
            }
            For B1I/B3I
            {
                'iono_corr': dict, // Klobuchar模型参数
                'almanac': dict, // 历书数据
                'pos': Tuple[float, float, float] // 接收机位置
            }""")
            raise e
            return {}