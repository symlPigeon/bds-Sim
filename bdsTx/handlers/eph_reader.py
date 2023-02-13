'''
Author: symlPigeon 2163953074@qq.com
Date: 2023-02-13 11:56:42
LastEditTime: 2023-02-13 12:33:51
LastEditors: symlPigeon 2163953074@qq.com
Description: 读取星历
FilePath: /bds-Sim/bdsTx/handlers/eph_reader.py
'''

import json
import logging
import traceback


class ephemeris_reader:
    def __init__(self, filepath: str) -> None:
        """初始化星历读取器

        Args:
            filepath (str): 读取星历文件的路径
        """
        self._filepath = filepath
        self._eph = {}
        
    def _reader(self) -> None:
        """read eph
        """
        try:
            f = open(self._filepath, "r")
            self._eph = json.load(f)
        except FileNotFoundError as e:
            logging.error("Ephemeris file not found: %s" % self._filepath)
            traceback.print_exception(e)
            self._eph = {}
        except json.JSONDecodeError as e:
            logging.error("Ephemeris file format error: %s" % self._filepath)
            traceback.print_exception(e)
            self._eph = {}
        except Exception as e:
            logging.error("Unexcepted error: %s" % self._filepath)
            traceback.print_exception(e)
            self._eph = {}