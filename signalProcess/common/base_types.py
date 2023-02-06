'''
Author: symlPigeon 2163953074@qq.com
Date: 2023-02-06 16:57:30
LastEditTime: 2023-02-06 17:01:33
LastEditors: symlPigeon 2163953074@qq.com
Description: 基本的一些类型定义，主要用来完善补全提示和水代码行数，意义不大 :(
FilePath: /bds-Sim/signalProcess/common/base_types.py
'''

from typing import Any, Protocol


class sizedIterableSource(Protocol):
    def __len__(self) -> int:
        ...
        
    def __next__(self) -> Any:
        ...
        
    def __iter__(self):
        return self
        
    def __getitem__(self, idx: int) -> Any:
        ...
        
    def is_repeatable(self) -> bool:
        ...