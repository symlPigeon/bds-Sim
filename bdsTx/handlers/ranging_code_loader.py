"""
Author: symlPigeon 2163953074@qq.com
Date: 2023-02-13 15:12:06
LastEditTime: 2023-02-14 16:18:53
LastEditors: symlpigeon
Description: 读取测距码
FilePath: /bds-Sim/bdsTx/handlers/ranging_code_loader.py
"""

import json
import logging

from bdsTx.satellite_info.broadcast_type import SIGNAL_TYPE


class rangingCodeReader:
    def __init__(self, filepath: str):
        self._filepath = filepath

    def read(self, prn: int, signal_type: int) -> dict:
        try:
            match signal_type:
                case SIGNAL_TYPE.B1C_SIGNAL:
                    path = self._filepath + f"/b1c/prn-{prn}.json"
                case SIGNAL_TYPE.B1I_SIGNAL:
                    path = self._filepath + f"/b1i/prn-{prn}.json"
                case SIGNAL_TYPE.B3I_SIGNAL:
                    path = self._filepath + f"/b3i/prn-{prn}.json"
                case SIGNAL_TYPE.B2A_SIGNAL:
                    logging.warning("B2A signal is not supported yet")
                    raise FileNotFoundError()
                case _:
                    logging.error("Unsupported broadcast type: %d" % signal_type)
                    logging.error("Only these types are supported:")
                    logging.error("  SIGNAL_TYPE.B1I -- 1")
                    logging.error("  SIGNAL_TYPE.B3I -- 2")
                    logging.error("  SIGNAL_TYPE.B1C -- 3")
                    logging.error("  SIGNAL_TYPE.B2A -- 4 (NOT IMPLEMENTED YET)")
                    raise FileNotFoundError()
            with open(path, "r") as f:
                data = json.load(f)
            match signal_type:
                case SIGNAL_TYPE.B1C_SIGNAL:
                    data["prn"] = data["data"]
                    data["qprn"] = data["pilot"]
                    data["qprn_sub"] = data["sub_pilot"]
                case SIGNAL_TYPE.B1I_SIGNAL | SIGNAL_TYPE.B3I_SIGNAL:
                    pass # the data is already in the right format
            return data
        except FileNotFoundError:
            logging.error("File Not Found!")
            return {}
        except json.JSONDecodeError:
            logging.error("JSON Decode Error!")
            return {}
