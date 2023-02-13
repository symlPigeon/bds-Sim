'''
Author: symlPigeon 2163953074@qq.com
Date: 2023-02-13 11:24:42
LastEditTime: 2023-02-13 11:50:16
LastEditors: symlPigeon 2163953074@qq.com
Description: 卫星的广播类型
FilePath: /bds-Sim/bdsTx/satellite_info/broadcast_type.py
'''

class SIGNAL_TYPE:
    B1I_SIGNAL = 1
    B3I_SIGNAL = 2
    B1C_SIGNAL = 3
    B2A_SIGNAL = 4
    SUPPORT_SIGNAL_TYPE = [B1I_SIGNAL, B3I_SIGNAL, B1C_SIGNAL, B2A_SIGNAL]

_BxI_list = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
    11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
    21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 
    32, 33, 34, 35, 36, 37, 38, 39, 40, 41,
    42, 43, 44, 45, 46, 59, 60
]

_B1C_B2a_list = [
    19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
    29, 30, 32, 33, 34, 35, 36, 37, 38, 39,
    40, 41, 42, 43, 44, 45, 46
]


def is_b1i_valid(prn: int) -> bool:
    """判断卫星是否能够发送B1I信号

    Args:
        prn (int): 卫星的PRN号

    Returns:
        bool: 是否能够发送B1I信号
    """
    return prn in _BxI_list


def is_b3i_valid(prn: int) -> bool:
    """判断卫星是否能够发送B3I信号

    Args:
        prn (int): 卫星的PRN号

    Returns:
        bool: 是否能够发送B3I信号
    """
    return prn in _BxI_list


def is_b1c_valid(prn: int) -> bool:
    """判断卫星是否能够发送B1C信号

    Args:
        prn (int): 卫星的PRN号

    Returns:
        bool: 是否能够发送B1C信号
    """
    return prn in _B1C_B2a_list


def is_b2a_valid(prn: int) -> bool:
    """判断卫星是否能够发送B2a信号

    Args:
        prn (int): 卫星的PRN号

    Returns:
        bool: 是否能够发送B2a信号
    """
    return prn in _B1C_B2a_list


def is_signal_able_to_tx(prn: int, signal: int) -> bool:
    """判断卫星是否能够发射某种信号

    Args:
        prn (int): 卫星PRN号
        signal (int): 信号类型

    Returns:
        bool: 是否能够发送
    """
    match signal:
        case SIGNAL_TYPE.B1I_SIGNAL:
            return is_b1i_valid(prn)
        case SIGNAL_TYPE.B3I_SIGNAL:
            return is_b3i_valid(prn)
        case SIGNAL_TYPE.B1C_SIGNAL:
            return is_b1c_valid(prn)
        case SIGNAL_TYPE.B2A_SIGNAL:
            return is_b2a_valid(prn)
        case _:
            return False