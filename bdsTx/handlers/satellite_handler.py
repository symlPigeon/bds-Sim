"""
Author: symlpigeon
Date: 2022-11-22 11:44:41
LastEditTime: 2022-11-23 10:28:45
LastEditors: symlpigeon
Description: satellite handler
FilePath: /bds-Sim/bdsTx/handlers/satellite_handler.py
"""

import logging
from abc import abstractmethod
from typing import TYPE_CHECKING, List

from base_object import baseProcessorHandler, baseSourceHandler

from bdsTx.frame.b1c import b1c_frame

if TYPE_CHECKING:
    from satellite_queue_handler import satelliteQueueHandler


class satelliteHandler(baseSourceHandler):
    def __init__(
        self,
        prn: int,
        manager: satelliteQueueHandler,
        next_handler: baseProcessorHandler,
    ):
        self._ranging_code = manager.get_ranging_code(prn)
        self._ephemeris = manager.get_ephemeris(prn)
        self._ldpc_mat_1 = manager.get_ldpc_mat_1()
        self._ldpc_mat_2 = manager.get_ldpc_mat_2()
        self._next_handler = next_handler
        self._manager = manager

    @abstractmethod
    def _produce(self):
        pass

    @abstractmethod
    def trigger(self):
        pass


class b1cSatelliteHandler(satelliteHandler):
    def __init__(
        self,
        prn: int,
        manager: satelliteQueueHandler,
        next_handler: baseProcessorHandler,
        frame_order: List[int],
    ):
        super().__init__(prn, manager, next_handler)
        self._iono_corr = manager.get_iono_corr("bdgim")
        self._frame_order = frame_order
        self._frame_creater = b1c_frame.b1cFrame(
            prn,
            self._ephemeris,
            self._iono_corr["alpha"],
            self._frame_order,
            self._ldpc_mat_1,
            self._ldpc_mat_2,
        )

    def _produce(self):
        frame = self._frame_creater.make_frame(self._manager.get_curr_time())
        
    def trigger(self):
        logging.info(f"{self} - b1cSatelliteHandler trigger")
        self._produce()
