'''
Author: symlPigeon 2163953074@qq.com
Date: 2023-02-13 11:56:42
LastEditTime: 2023-02-13 14:51:05
LastEditors: symlPigeon 2163953074@qq.com
Description: 读取星历
FilePath: /bds-Sim/bdsTx/handlers/eph_reader.py
'''

import json
import logging
import traceback

from bdsTx.satellite_info.time_system import get_closest_timestamp


class ephemerisReader:
    def __init__(self, filepath: str) -> None:
        """初始化星历读取器

        Args:
            filepath (str): 读取星历文件的路径
        """
        self._filepath = filepath
        self._eph = {}
        logging.info("Reading ephemeris file: %s" % self._filepath)
        self._reader()
        logging.info("Ephemeris file read complete!")
        
    def _reader(self) -> None:
        """read eph
        """
        try:
            with open(self._filepath, "r") as f:
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
            
    def get_ephemeris(self) -> dict:
        """获取星历

        Returns:
            dict: 星历
        """
        return self._eph
    
    def get_ephemeris_by_prn(self, prn: int) -> dict:
        """根据卫星号获取星历

        Args:
            prn (int): 卫星号

        Returns:
            dict: 星历
        """
        try:
            return self.get_ephemeris()["%02d" % prn]
        except KeyError:
            logging.error("Ephemeris of PRN %02d not found" % prn)
            return {}
        
    def get_ephemeris_by_prn_and_time(self, prn: int, timestamp: float) -> dict:
        """根据卫星PRN号和时间获取星历

        Args:
            prn (int): PRN号
            timestamp (float): 当前UTC时间戳

        Returns:
            dict: 星历
        """
        ts = list(self.get_ephemeris_by_prn(prn).keys())
        if ts == {}:
            logging.error("Ephemeris of PRN %02d not found" % prn)
        cts = get_closest_timestamp(ts, timestamp)
        return self.get_ephemeris_by_prn(prn)[cts]