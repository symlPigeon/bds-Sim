'''
Author: symlPigeon 2163953074@qq.com
Date: 2023-02-13 14:36:47
LastEditTime: 2023-03-06 10:24:54
LastEditors: symlPigeon 2163953074@qq.com
Description: 读取电离层修正数据
FilePath: /bds-Sim/bdsTx/handlers/iono_corr_loader.py
'''

import json
import logging


class ionoCorrReader:
    def __init__(self, filepath: str) -> None:
        """初始化电离层修正数据读取器

        Args:
            filepath (str): 读取电离层修正数据文件的路径
        """
        self._filepath = filepath
        self._iono_corr = {}
        self._reader()
        
    def _reader(self) -> None:
        """_summary_
        """
        try:
            with open(self._filepath, "r") as f:
                self._iono_corr = json.load(f)
        except FileNotFoundError as e:
            logging.error("Iono corr file not found: %s" % self._filepath)
        except json.JSONDecodeError as e:   
            logging.error("Iono corr file format error: %s" % self._filepath)
            
    def get_klobuchar(self) -> dict:
        return self._iono_corr["klobuchar"]["a"]
    
    def get_bdgim(self) -> dict:
        return self._iono_corr["bdgim"]["a"]