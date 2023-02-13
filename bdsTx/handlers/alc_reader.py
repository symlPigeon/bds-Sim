'''
Author: symlPigeon 2163953074@qq.com
Date: 2023-02-13 14:50:23
LastEditTime: 2023-02-13 14:52:06
LastEditors: symlPigeon 2163953074@qq.com
Description: 读取历书数据
FilePath: /bds-Sim/bdsTx/handlers/alc_reader.py
'''

import json
import logging


class almanacReader:
    def __init__(self, filepath: str) -> None:  
        self._filepath = filepath
        self._almanac = {}
        self._read()
        
    def _read(self):
        try:
            with open(self._filepath, "r") as f:
                self._almanac = json.load(f)
        except FileNotFoundError as e:
            logging.error("Almanac file not found: %s" % self._filepath)
        except json.JSONDecodeError as e:
            logging.error("Almanac file format error: %s" % self._filepath)
            
    def getAlmanac(self) -> dict:
        return self._almanac
         