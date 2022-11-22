"""
Author: symlpigeon
Date: 2022-11-22 11:46:55
LastEditTime: 2022-11-22 11:48:52
LastEditors: symlpigeon
Description: 卫星队列处理
FilePath: /bds-Sim/bdsTx/handlers/satellite_queue_handler.py
"""

import datetime
import json
import logging
import time
from typing import TYPE_CHECKING

import numpy as np
from base_object import baseSourceHandler

if TYPE_CHECKING:
    from satellite_handler import satelliteHandler


class satelliteQueueHandler(baseSourceHandler):
    def __init__(
        self,
        ranging_code_path: str,
        ephemeris_path: str,
        iono_corr_path: str,
        ldpc_mat_path: str,
        queue_size: int = 4,
        curr_time: float = time.time(),
    ):
        # ranging code太多了，还是让satellite handler自己去读取吧
        self._ranging_code_path = ranging_code_path
        self._load_ephemeris_path(ephemeris_path)
        self._load_ldpc_mat(ldpc_mat_path)
        self._load_iono_corr(iono_corr_path)
        self._queue = []
        self._queue_size = queue_size
        self._curr_time = curr_time
        self._refer_time = time.time()
        logging.debug(f"{self} - Satellite queue handler init done")

    def _load_ephemeris_path(self, ephemeris_path: str) -> None:
        with open(ephemeris_path, "r", encoding="utf-8") as f:
            self._ephemeris = json.load(f)

    def _load_ldpc_mat(self, ldpc_path: str) -> None:
        with open(ldpc_path + "/ldpc_matG_100_200.json", "r", encoding="utf-8") as f:
            self._ldpc_mat_1 = json.load(f)
        with open(ldpc_path + "/ldpc_matG_44_88.json", "r", encoding="utf-8") as f:
            self._ldpc_mat_2 = json.load(f)

    def _load_iono_corr(self, iono_corr_path: str) -> None:
        with open(iono_corr_path, "r", encoding="utf-8") as f:
            self.iono_corr = json.load(f)

    def _produce(self) -> None:
        for obj in self._queue:
            obj.trigger()

    def _add_satellite(self, satellite: satelliteHandler) -> None:
        if self._queue_size >= len(self._queue):
            logging.error(f"{self} - Satellite queue is full")
            return
        self._queue.append(satellite)

    def trigger(self) -> None:
        self._produce()

    def get_ldpc_mat_1(self) -> np.ndarray:
        return self._ldpc_mat_1

    def get_ldpc_mat_2(self) -> np.ndarray:
        return self._ldpc_mat_2

    def get_curr_time(self) -> float:
        return self._curr_time + time.time() - self._refer_time

    def get_ranging_code(self, prn: int) -> dict:
        filepath = self._ranging_code_path + f"/prn-{prn}.json"
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    def get_iono_corr(self, model: str) -> dict:
        # FIXME: Figure out which is the best data to use!
        return self.iono_corr[model]["a"]

    def get_ephemeris(self, prn: int) -> dict:
        eph = self._ephemeris[f"{prn:02d}"]
        # Get the closest ephemeris
        curr_time = self.get_curr_time()
        min_diff = 1e9
        # 2022-11-09_00:00:00 YYYY-MM_DD_HH:MM:SS
        target_time = ""
        for t in eph.keys():
            diff = abs(
                time.mktime(
                    datetime.datetime.strptime(t, "%Y-%m-%d_%H:%M:%S").timetuple()
                )
                - curr_time
            )
            if diff < min_diff:
                min_diff = diff
                target_time = t
        return eph[target_time]
