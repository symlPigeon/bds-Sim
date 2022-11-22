'''
Author: symlpigeon
Date: 2022-11-22 10:40:07
LastEditTime: 2022-11-22 19:26:16
LastEditors: symlpigeon
Description: 基类
FilePath: /bds-Sim/bdsTx/handlers/base_object.py
'''

from abc import ABC


class baseSourceHandler(ABC):
    def __init__(self):
        pass
    def _produce(self):
        pass
    def trigger(self):
        pass
        
        
class baseProcessorHandler(ABC):
    def __init__(self):
        pass
    def _process(self, *args):
        pass
    def add(self, *args):
        pass
    def trigger(self):
        pass
        