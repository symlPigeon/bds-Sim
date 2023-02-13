'''
Author: symlPigeon 2163953074@qq.com
Date: 2023-02-13 14:30:40
LastEditTime: 2023-02-13 14:35:53
LastEditors: symlPigeon 2163953074@qq.com
Description: LDPC Encoder for B1C
FilePath: /bds-Sim/bdsTx/handlers/ldpc_loader.py
'''

import json
import logging

import numpy as np


class ldpcLoader:
    def __init__(self, filepath: str):
        """加载LDPC矩阵

        Args:
            filepath (str): 路径
        """
        try:
            with open(filepath, "r") as f:
                self._ldpc = np.ndarray(json.load(f))
        except FileNotFoundError as e:
            logging.error("LDPC file not found: %s" % filepath)
            print(e)
            self._ldpc = np.ndarray((0, 0)) 
        except json.JSONDecodeError as e:
            logging.error("LDPC file format error: %s" % filepath)
            print(e)
            self._ldpc = np.ndarray((0, 0))
            
    def get(self) -> np.ndarray:
        return self._ldpc

