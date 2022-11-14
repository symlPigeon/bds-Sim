"""
Author: symlpigeon
Date: 2022-11-11 22:53:13
LastEditTime: 2022-11-11 22:53:15
LastEditors: symlpigeon
Description: B1C子帧1
FilePath: /bdsTx/frame/b1c/b1c_subframe1.py
"""

from typing import Tuple

from bdsTx.coding import bch
from bdsTx.satellite_info import time_system


def make_subframe1(prn: int, curr_time: float) -> Tuple[bytes, bytes]:
    curr_second = time_system.utc2bds(curr_time)[1] % 3600
    curr_second //= 18  # 量化单位18s
    return prn.to_bytes(1, "big"), int(curr_second).to_bytes(1, "big")


def encoding_subframe1(subframe1: Tuple[bytes, bytes]) -> bytes:
    frag1 = bch.bch_21_6_enc(subframe1[0])
    frag2 = bch.bch_51_8_enc(subframe1[1])
    ans = b""
    for idx in range(0, len(frag1) - 1):
        ans += ((frag1[idx] << 3) & 0xF8 | (frag1[idx + 1] >> 5) & 0x07).to_bytes(
            1, "big"
        )
    ans += ((frag1[-1] << 3) & 0xF8 | frag2[0] & 0x07).to_bytes(1, "big")
    ans += frag2[1:]
    return ans


if __name__ == "__main__":
    import time

    subframe1 = make_subframe1(60, time.time())
    # print(subframe1)
    # print(encoding_subframe1(subframe1))
    for b in encoding_subframe1(subframe1):
        print(f"{b:08b}", end=" ")
