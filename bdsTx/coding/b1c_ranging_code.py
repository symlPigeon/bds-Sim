'''
Author: symlpigeon
Date: 2022-11-08 10:06:28
LastEditTime: 2022-11-10 14:35:31
LastEditors: symlpigeon
Description: 生成b1c信号主码
FilePath: /sim_bds/python/coding/b1c_ranging_code.py
'''

import json
from typing import Tuple
from weil_code import get_weil_code, legendre_seq


MASTER_CODE_LENGTH = 10230
MASTER_WEIL_CODE_LENGTH = 10243
SUB_CODE_LENGTH = 1800
SUB_WEIL_CODE_LENGTH = 3607


def get_prn_data_from_json_file(filename: str = "prn_data/b1c_prn_data.json") -> dict:
    """从json文件中获取PRN信息

    Args:
        filename (str, optional): 文件名. Defaults to "prn_data.json".

    Returns:
        dict: PRN信息
    """
    with open(filename, "r") as f:
        data = json.load(f)
    return data


class b1c_prn_loader:
    __prn_data = get_prn_data_from_json_file()

    @classmethod
    def get_prn_data(cls, prn: int, code_type: str) -> dict:
        """获取PRN信息

        Args:
            prn (int): 卫星PRN号
            type (str): 对应的截取信息类型，可选值为"data", "pilot", "sub_pilot"

        Raises:
            ValueError: 如果PRN号或者type不在范围内

        Returns:
            dict: PRN号对应的信息
        """
        try:
            return cls.__prn_data[code_type][prn - 1]
        except:
            raise ValueError("Invalid PRN number!")


def get_b1c_code(prn: int, code_type: str) -> str:
    """获取B1C码字

    Args:
        prn (int): 卫星PRN号
        type (str, optional): 类型. "data" or "pilot" or "sub_pilot"

    Returns:
        bytes: 码字
    """
    w, p = b1c_prn_loader.get_prn_data(
        prn, code_type)["w"], b1c_prn_loader.get_prn_data(prn, code_type)["p"]
    if code_type == "data" or code_type == "pilot":
        seq_length = MASTER_WEIL_CODE_LENGTH
        code_length = MASTER_CODE_LENGTH
    elif code_type == "sub_pilot":
        seq_length = SUB_WEIL_CODE_LENGTH
        code_length = SUB_CODE_LENGTH
    else:
        # this should not happen...
        raise ValueError("Invalid code type!")
    weil_code = get_weil_code(legendre_seq.get(seq_length), w, seq_length)
    code = ""
    for k in range(p - 1, p + code_length - 1):
        code += str(weil_code[k % seq_length])
    # 合并3bit，生成八进制的序列。
    oct_code = "".join([str(int(code[i:i + 3], 2))
                       for i in range(0, len(code), 3)])
    return oct_code


if __name__ == "__main__":
    """
    测试正确性
    """
    from colorama import Fore, Style
    flag = True
    for prn in range(1, 64, 1):
        for code_type in ["data", "pilot", "sub_pilot"]:
            code = get_b1c_code(prn, code_type)
            first_24 = code[:8]
            last_24 = code[-8:]
            target_first_24 = b1c_prn_loader.get_prn_data(prn, code_type)[
                "first_24bit"]
            target_last_24 = b1c_prn_loader.get_prn_data(prn, code_type)[
                "last_24bit"]
            if first_24 != target_first_24:
                print(
                    f"[{Fore.RED}ERROR{Style.RESET_ALL}]  PRN{prn} {code_type} first 24bit error!")
                print(
                    f"Should get {Fore.BLUE}{target_first_24}{Style.RESET_ALL}, but get {Fore.BLUE}{first_24}{Style.RESET_ALL}")
                flag = False
            if last_24 != target_last_24:
                print(
                    f"[{Fore.RED}ERROR{Style.RESET_ALL}]  PRN{prn} {code_type} last 24bit error!")
                print(
                    f"Should get {Fore.BLUE}{target_last_24}{Style.RESET_ALL}, but get {Fore.BLUE}{last_24}{Style.RESET_ALL}")
                flag = False
    if flag:
        print(f"[{Fore.GREEN}SUCCESS{Style.RESET_ALL}] All tests passed!")
    else:
        print(f"[{Fore.RED}ERROR{Style.RESET_ALL}] Some tests failed!")
