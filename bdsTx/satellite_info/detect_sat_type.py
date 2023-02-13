'''
Author: symlpigeon
Date: 2023-01-16 15:11:29
LastEditTime: 2023-02-13 11:49:02
LastEditors: symlPigeon 2163953074@qq.com
Description: 判断卫星类型
FilePath: /bds-Sim/bdsTx/satellite_info/detect_sat_type.py
'''

class SAT_TYPE:
    SAT_TYPE_GEO = 1
    SAT_TYPE_IGSO = 2
    SAT_TYPE_MEO = 3

def detect_sat_type(current_id: str) -> int:
    """从卫星的PRN号转换为卫星轨道类型
    1:GEO 2:IGSO 3:MEO

    Args:
        current_id (str): 卫星PRN

    Returns:
        int: 轨道类型
    """
    prn = int(current_id)
    # http://www.csno-tarc.cn/system/constellation
    sat_type = [
        0, # prn 0 is invalid
        1, 1, 1, 1, 1, # 1-5
        2, 2, 2, 2, 2, # 6-10
        3, 3, 2, 3, 0, # 11-15, prn 15 is empty
        2, 0, 0, 3, 3, # 16-20, prn 17, 18 is empty
        3, 3, 3, 3, 3, # 21-25
        3, 3, 3, 3, 3, # 26-30
        2, 3, 3, 3, 3, # 31-35
        3, 3, 2, 2, 2, # 36-40
        3, 3, 3, 3, 3, # 41-45
        3, 0, 0, 0, 0, # 46-50, prn 47, 48, 49, 50 is empty
        0, 0, 0, 0, 0, # 51-55, prn 51, 52, 53, 54, 55 is empty
        2, 3, 3, 1, 1, # 56-60
        1
    ]
    return sat_type[prn]

