"""
Author: symlpigeon
Date: 2023-01-15 13:48:07
LastEditTime: 2023-01-20 11:02:43
LastEditors: symlpigeon
Description: B1I 电文构造
FilePath: /bds-Sim/bdsTx/frame/b1i/b1i_frame.py
"""

from bdsTx.frame.b1i.d1.subframe1 import create_subframe1
from bdsTx.frame.b1i.d1.subframe2 import create_subframe2
from bdsTx.frame.b1i.d1.subframe3 import create_subframe3
from bdsTx.frame.b1i.d1.subframe4 import create_subframe4
from bdsTx.frame.b1i.d1.subframe5 import create_subframe5


class b1iFrame:
    """B1I Frame"""

    def __init__(self, prn: int, eph: dict, klobuchar: dict, alc: dict) -> None:
        """Initiate the B1I Frame obj
        
        !!! Note that the ephemeris only contains the the data of the current satellite.
        But the almanac contains all the data of the satellites.
          Be careful!

        Args:
            prn (int): satellite PRN
            eph (dict): ephemeris
            klobuchar (dict): klobuchar model parameters
            alc (dict): almanac
        """
        self._prn = prn
        self._eph = eph
        self._klobuchar = klobuchar
        self._alc = alc

    def get_prn(self) -> int:
        """get satellite PRN number

        Returns:
            int: PRN number
        """
        return self._prn

    def get_eph(self) -> dict:
        """get ephemeris

        Returns:
            dict: ephemeris
        """
        return self._eph

    def get_klobuchar(self) -> dict:
        """get Klobuchar model parameters

        Returns:
            dict: Model Parameters
        """
        return self._klobuchar

    def get_alc(self) -> dict:
        """get almanac data

        Returns:
            dict: almanac
        """
        return self._alc

    def make_hexframe(self, curr_time: float) -> str:
        """Generate B1I frame

        Args:
            curr_time (float): current timestamp, UTC

        Returns:
            str: Frame data in hex string
        """
        subframe1 = create_subframe1(curr_time, self._eph, self._klobuchar)
        subframe2 = create_subframe2(curr_time, self._eph)
        subframe3 = create_subframe3(curr_time, self._eph)
        # NOTE: Currently, we just ignore the pageID parameter...
        subframe4 = create_subframe4(curr_time, self._alc)
        subframe5 = create_subframe5(curr_time, self._alc)
        frame = subframe1 + subframe2 + subframe3 + subframe4 + subframe5
        return frame

    def make_frame(self, curr_time: float) -> bytes:
        """Generate B1I frame
        !!! BE CAUTIOUS: B1I frame length is 1500 bits,
        which means it is not a multiple of 8 bits.
        To solve this problem, we pad 4 bits of 0 at the end of the frame.

        Args:
            curr_time (float): current timestamp, in UTC

        Returns:
            bytes: Frame data in bytes
        """
        frame = self.make_hexframe(curr_time)
        frame += "0" * 4
        return bytes.fromhex(frame)


if __name__ == "__main__":
    import json
    import time
    eph = json.load(open("../../satellite_info/ephemeris/tarc0140.json"))["12"]["2023-01-14_00:00:00"]
    klo = json.load(open("../../satellite_info/ionosphere/iono_corr.json"))["klobuchar"]["a"]
    alc = json.load(open("../../satellite_info/almanac/tarc0190.23alc.json"))
    frame_maker = b1iFrame(30, eph, klo, alc)
    print(frame_maker.make_hexframe(time.time()))