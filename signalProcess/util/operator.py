'''
Author: symlPigeon 2163953074@qq.com
Date: 2023-02-06 15:46:11
LastEditTime: 2023-02-06 17:27:49
LastEditors: symlPigeon 2163953074@qq.com
Description: Operator for signal processing
FilePath: /bds-Sim/signalProcess/util/operator.py
'''

from abc import ABC
from typing import Any, Callable, List, Sequence, Type

import numpy as np

from signalProcess.common.base_types import sizedIterableSource


class multiPortOperator(sizedIterableSource):
    # in this module, we perform some operations on multiple input ports
    # this class perform the operations, output as an Iterable object
    def __init__(self, in_ports: List[sizedIterableSource], operation: Callable[[List[Any]], Any] , dtype: Type) -> None:
        """对多输入的信号源进行处理

        Args:
            in_ports (List[Iterable]): 输入的各个信号源, should be repeatable.
        """
        self._num_ports = len(in_ports)
        self._in_ports = in_ports
        self._len = np.max([len(port) for port in in_ports])
        self._dtype = dtype
        #   NOTE: in this section, we just assume that all inputs are repeatable
        #   Enable the code below if you want to check the repeatable of inputs
        # assert all([port.is_repeatable() for port in in_ports]), "All inputs should be repeatable"
        self._func = operation
        self._idx = 0
    
    def __iter__(self):
        return self
    
    def __len__(self) -> int:
        return self._len
    
    def __getitem__(self, idx: int) -> Any:
        params = [port[idx] for port in self._in_ports]
        return self._func(params)
    
    def __next__(self):
        # WARNING: be careful! this may cause infinite loop!
        if self._idx >= self._len:
            self._idx = 0
        ret = self[self._idx]
        self._idx += 1
        return ret
    
    def is_repeatable(self) -> bool:
        # Maybe we should check the repeatable of inputs, just in case
        # but not now :)
        return True
    
    
class multiPortAdd(multiPortOperator):
    def __init__(self, in_ports: List[sizedIterableSource], dtype: Type = np.uint8) -> None:
        super().__init__(in_ports, lambda x: np.sum(x), dtype)
        

class multiPortMultiply(multiPortOperator):
    def __init__(self, in_ports: List[sizedIterableSource], dtype: Type = np.uint8) -> None:
        super().__init__(in_ports, lambda x: np.prod(x), dtype)
        

class multiPortXor(multiPortOperator):
    def __init__(self, in_ports: List[sizedIterableSource], dtype: Type = np.uint8) -> None:
        super().__init__(in_ports, lambda x: np.bitwise_xor.reduce(x), dtype)
        
        
if __name__ == "__main__":
    from signalProcess.util.data_util import vectorSource
    data1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=np.uint8)
    data2 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=np.uint8)
    s1 = vectorSource(data1, True)
    s2 = vectorSource(data2, True)
    add = multiPortAdd([s1, s2])
    for i in range(20):
        print(next(add), end=" ")
        
    print()
        
    mul = multiPortMultiply([s1, s2])
    for i in range(20):
        print(next(mul), end=" ")
        
        