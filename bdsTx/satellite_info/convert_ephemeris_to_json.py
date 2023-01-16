'''
Author: symlpigeon
Date: 2022-11-08 19:22:21
LastEditTime: 2023-01-16 15:13:19
LastEditors: symlpigeon
Description: 将星历文件转换为json格式
FilePath: /bds-Sim/bdsTx/satellite_info/convert_ephemeris_to_json.py
'''

import calendar
import json
from typing import List, Tuple

from detect_sat_type import detect_sat_type
from time_system import utc2bds


def get_data(x): return list(filter(None, x.split(' ')))[-1]


def render_iono_corr_data(raw_eph_data: List[str]) -> Tuple[dict, dict]:
    """从星历文件中解析电离层参数

    Args:
        raw_eph_data (List[str]): 原始的星历文件数据，应该是截取了其中电离层参数的部分

    Returns:
        Tuple[dict, dict]: klobuchar模型以及BDGIM模型参数
    """
    iono_corr_lines_type1 = []
    iono_corr_lines_type2 = []
    for i in range(0, len(raw_eph_data)):
        if get_data(raw_eph_data[i]) == "CORR":
            if raw_eph_data[i][0:4] == "BDSA" or raw_eph_data[i][0:4] == "BDSB":
                iono_corr_lines_type1.append(raw_eph_data[i])
            elif raw_eph_data[i][0:4] == "BDS1" or raw_eph_data[i][0:4] == "BDS2" or raw_eph_data[i][0:4] == "BDS3":
                iono_corr_lines_type2.append(raw_eph_data[i])
    if len(iono_corr_lines_type1) % 2 == 0 and len(iono_corr_lines_type2) % 3 == 0:
        klobuchar_iono_corr = {}
        for line_idx in range(0, len(iono_corr_lines_type1), 2):
            sate_id = iono_corr_lines_type1[line_idx][57:59]
            entry_idx = iono_corr_lines_type1[line_idx][54]
            alpha1 = float(iono_corr_lines_type1[line_idx][6:17].strip())
            alpha2 = float(iono_corr_lines_type1[line_idx][18:29].strip())
            alpha3 = float(iono_corr_lines_type1[line_idx][30:41].strip())
            alpha4 = float(iono_corr_lines_type1[line_idx][42:53].strip())
            beta1 = float(iono_corr_lines_type1[line_idx + 1][6:17].strip())
            beta2 = float(iono_corr_lines_type1[line_idx + 1][18:29].strip())
            beta3 = float(iono_corr_lines_type1[line_idx + 1][30:41].strip())
            beta4 = float(iono_corr_lines_type1[line_idx + 1][42:53].strip())
            klobuchar_iono_corr[entry_idx] = {
                "sate_id": sate_id,
                "alpha": [alpha1, alpha2, alpha3, alpha4],
                "beta": [beta1, beta2, beta3, beta4]
            }
        bdgim_iono_corr = {}
        for line_idx in range(0, len(iono_corr_lines_type2), 3):
            sate_id = iono_corr_lines_type2[line_idx][57:59]
            entry_idx = iono_corr_lines_type2[line_idx][54]
            alpha1 = float(iono_corr_lines_type2[line_idx][6:17].strip())
            alpha2 = float(iono_corr_lines_type2[line_idx][18:29].strip())
            alpha3 = float(iono_corr_lines_type2[line_idx][30:41].strip())
            alpha4 = float(iono_corr_lines_type2[line_idx + 1][6:17].strip())
            alpha5 = float(iono_corr_lines_type2[line_idx + 1][18:29].strip())
            alpha6 = float(iono_corr_lines_type2[line_idx + 1][30:41].strip())
            alpha7 = float(iono_corr_lines_type2[line_idx + 2][6:17].strip())
            alpha8 = float(iono_corr_lines_type2[line_idx + 2][18:29].strip())
            alpha9 = float(iono_corr_lines_type2[line_idx + 2][30:41].strip())
            bdgim_iono_corr[entry_idx] = {
                "sate_id": sate_id,
                "alpha": [alpha1, alpha2, alpha3, alpha4, alpha5, alpha6, alpha7, alpha8, alpha9]
            }
        return klobuchar_iono_corr, bdgim_iono_corr 
    return {}, {}


def detect_file_type(raw_eph_data: List[str]) -> int:
    """判断星历文件类型，B1I/B3I or B1C/B2A

    Args:
        raw_eph_data (List[str]): 原始数据

    Returns:
        str: 文件类型，1 for B1I/B3I，2 for B1C/B2A
    """    
    raw_string = "".join(raw_eph_data)
    raw_splited = raw_string.split(" ")
    if "B1I" in raw_splited or "B3I" in raw_splited:
        print("+ B1I/B3I ephemeris detected")
        return 1
    elif "B1C" in raw_splited or "B2A" in raw_splited:
        print("+ B1C/B2A ephemeris detected")
        return 2
    # 不知道啥类型，就当作B1I/B3I
    return 1


def render_ephemeris(ephemeris_file_path: List[str], ephemeris_output_path: str, iono_corr_path: str) -> None:
    """解析星历文件

    Args:
        ephemeris_file_path (str): 星历文件路径，支持多个文件
        ephemeris_output_path (str): 导出的解析数据路径
        iono_corr_path (str): 导出的电离层校正数据路径
    """
    json_data = {}
    
    for eph_file in ephemeris_file_path:
        # -------------
        #     读取
        # -------------
        with open(eph_file, 'r') as f:
            ephemeris = f.read()
        ephemeris = ephemeris.split("\n")
        while "" in ephemeris:
            ephemeris.remove("")
        # 分割文件，找到星历数据头部结束的位置
        head_end_idx = 0
        while get_data(ephemeris[head_end_idx]) != "HEADER":
            head_end_idx += 1
            
        # -------------
        #    判断类型
        # -------------
        
        # 截取注释数据
        comment_start = 0
        while get_data(ephemeris[comment_start]) != "COMMENT":
            comment_start += 1
        comment_end = comment_start
        while get_data(ephemeris[comment_end]) == "COMMENT":
            comment_end += 1
        eph_type = detect_file_type(ephemeris[comment_start:comment_end])

        # -------------
        #   电离层参数
        # -------------
        
        # 几个文件里面的参数应该是一样的，保留最后一个有用的应该就行
        # 截取电离层校正参数开始位置
        iono_corr_start_idx = 0
        while get_data(ephemeris[iono_corr_start_idx]) != "CORR":
            iono_corr_start_idx += 1
        # 解析从开始位置到文件结尾这一段内的参数，应该都是电离层参数吧……
        klobuchar_iono_corr, bdgim_iono_corr = render_iono_corr_data(ephemeris[iono_corr_start_idx:head_end_idx])
        # 保存解析的数据
        if klobuchar_iono_corr != {} or bdgim_iono_corr != {}:
            with open(iono_corr_path, 'w') as f:
                json.dump({"klobuchar": klobuchar_iono_corr,
                            "bdgim": bdgim_iono_corr}, f, indent=4)
        else:
            # Something must be wrong
            print("Maybe Invalid Iono Correction Data, skipping...")

        # -------------
        #   卫星星历
        # -------------
        head_end_idx += 1  # 切到下一行
        for line in range(head_end_idx, len(ephemeris), 8):  # 一次8行
            try:
                # LINE 1        SV/EPOCH/SV CLK
                # ---------------------------------
                # 当前卫星ID
                current_id = ephemeris[line][1:3]
                # 如果已有该条目
                if current_id not in json_data:
                    json_data[current_id] = {}
                # Time (BDT)
                bdt_year = int(ephemeris[line][4:8])
                bdt_month = int(ephemeris[line][9:11])
                bdt_day = int(ephemeris[line][12:14])
                bdt_hour = int(ephemeris[line][15:17])
                bdt_minute = int(ephemeris[line][18:20])
                bdt_second = int(ephemeris[line][21:23])
                time_idx = f"{bdt_year}-{bdt_month:02d}-{bdt_day:02d}_{bdt_hour:02d}:{bdt_minute:02d}:{bdt_second:02d}"
                # 如果已有该条目
                if time_idx not in json_data[current_id]:
                    json_data[current_id][time_idx] = {}
                    json_data[current_id][time_idx]["support_type"] = 0
                _, toc = utc2bds(calendar.timegm((bdt_year, bdt_month, bdt_day, bdt_hour, bdt_minute, bdt_second, 0, 0, 0)))
                # 卫星钟偏系数a0, second
                a0 = float(ephemeris[line][23:42].strip())
                # 卫星钟漂系数a1, sec/sec
                a1 = float(ephemeris[line][42:61].strip())
                # 卫星钟漂移率系数a2, sec/sec^2
                a2 = float(ephemeris[line][61:].strip())
                
                # LINE 2     BROADCAST ORBIT-1
                # ---------------------------------
                # IODE/AODE 星历参数版本号/星历数据龄期
                iode_aode = int(float(ephemeris[line+1][4:23].strip()))
                # Crs 轨道半径正弦调和改正项振幅, meter
                Crs = float(ephemeris[line+1][23:42].strip())
                # 参考时刻卫星平均角速度和计算值之差Delta_n0, rad/sec
                delta_n0 = float(ephemeris[line+1][42:61].strip())
                # 参考时刻平近点角M0, rad
                M0 = float(ephemeris[line+1][61:].strip())
                
                # LINE 3     BROADCAST ORBIT-2
                # ---------------------------------
                # Cuc 纬度幅角的余弦调和改正项的振幅, rad
                Cuc = float(ephemeris[line+2][4:23].strip())
                # e 偏心率
                e = float(ephemeris[line+2][23:42].strip())
                # Cus 纬度幅角的正弦调和改正项的振幅, rad
                Cus = float(ephemeris[line+2][42:61].strip())
                # DeltaA_sqrtA 卫星轨道长半轴平方根, meter or meter^(1/2)
                deltaA_sqrtA = float(ephemeris[line+2][61:].strip())
                
                # LINE 4    BROADCAST ORBIT-3
                # ---------------------------------
                # Toe 参考时刻, sec
                Toe = float(ephemeris[line+3][4:23].strip())
                # Cic 轨道倾角余弦调和改正项的振幅, rad
                Cic = float(ephemeris[line+3][23:42].strip())
                # Omega0 升交点赤经, rad
                Omega0 = float(ephemeris[line+3][42:61].strip())
                # Cis 轨道倾角正弦调和改正项的振幅, rad
                Cis = float(ephemeris[line+3][61:].strip())
                
                # LINE 5    BROADCAST ORBIT-4
                # ---------------------------------
                
                # i0 参考时刻轨道倾角, rad
                i0 = float(ephemeris[line+4][4:23].strip())
                # Crc 轨道半径余弦调和改正项振幅, meter
                Crc = float(ephemeris[line+4][23:42].strip())
                # omega 近地点幅角， rad
                omega = float(ephemeris[line+4][42:61].strip())
                # Omega_dot 升交点赤经变化率, rad/sec
                Omega_dot = float(ephemeris[line+4][61:].strip())
                
                # LINE 6    BROADCAST ORBIT-5
                # ---------------------------------
                # IDOT 轨道倾角变化率, rad/sec
                IDOT = float(ephemeris[line+5][4:23].strip())
                # Data 电文来源，integer / in B1I, B3I, is spare
                data = int(float(ephemeris[line+5][23:42].strip()))
                # BDT Week, 注意这个是平滑过渡的
                bdt_week = float(ephemeris[line+5][42:61].strip())
                # A_DOT / EMPTY, A_DOT对应长半轴变化率
                a_dot = float(ephemeris[line+5][61:].strip())
                
                # LINE 7   BROADCAST ORBIT-6
                # ---------------------------------
                # 空间信号精度指数及空间信号检测精度指数 或 SV accuracy
                sv_accuracy = int(float(ephemeris[line+6][4:23].strip()))
                # HS 卫星健康状态
                hs = int(float(ephemeris[line+6][23:42].strip()))
                # TGD / TGD1
                tgd = float(ephemeris[line+6][42:61].strip())
                # ISC / TGD2
                isc = float(ephemeris[line+6][61:].strip())
                
                # LINE 8   BROADCAST ORBIT-7
                # ---------------------------------
                # 信号发射时间，BDT周内秒
                signal_time = float(ephemeris[line+7][4:23].strip())
                # IODC / AODC 钟差参数版本号/时钟数据龄期
                iodc_aodc = int(float(ephemeris[line+7][23:42].strip()))
                if eph_type == 2:
                    # Delta n0 dot 参考时刻卫星平均角速度与计算值之差的变化率, rad/sec^2
                    delta_n0_dot = float(ephemeris[line+7][42:61].strip())
                    # SatType/Empty,卫星轨道类型或者留空
                    sat_type = int(float(ephemeris[line+7][61:].strip()))
                else:
                    delta_n0_dot = 0
                    sat_type = 0
                    
                # ---------------------------------
                # 保存数据
                # ---------------------------------
                json_data[current_id][time_idx]["toc"] = toc
                json_data[current_id][time_idx]["a0"] = a0
                json_data[current_id][time_idx]["a1"] = a1
                json_data[current_id][time_idx]["a2"] = a2
                json_data[current_id][time_idx]["Crs"] = Crs
                json_data[current_id][time_idx]["delta_n0"] = delta_n0
                json_data[current_id][time_idx]["M0"] = M0
                json_data[current_id][time_idx]["Cuc"] = Cuc
                json_data[current_id][time_idx]["e"] = e
                json_data[current_id][time_idx]["Cus"] = Cus
                json_data[current_id][time_idx]["Toe"] = Toe
                json_data[current_id][time_idx]["Cic"] = Cic
                json_data[current_id][time_idx]["Omega0"] = Omega0
                json_data[current_id][time_idx]["Cis"] = Cis
                json_data[current_id][time_idx]["i0"] = i0
                json_data[current_id][time_idx]["Crc"] = Crc
                json_data[current_id][time_idx]["omega"] = omega
                json_data[current_id][time_idx]["Omega_dot"] = Omega_dot
                json_data[current_id][time_idx]["IDOT"] = IDOT
                json_data[current_id][time_idx]["BDT Week"] = bdt_week
                json_data[current_id][time_idx]["sv_accuracy"] = sv_accuracy
                json_data[current_id][time_idx]["hs"] = hs
                json_data[current_id][time_idx]["tgd"] = tgd
                json_data[current_id][time_idx]["isc"] = isc
                json_data[current_id][time_idx]["signal_time"] = signal_time
                # 区分两种类型的电文
                if eph_type == 1: # B1I/B3I
                    json_data[current_id][time_idx]["aode"] = iode_aode
                    json_data[current_id][time_idx]["sqrtA"] = deltaA_sqrtA
                    json_data[current_id][time_idx]["aodc"] = iodc_aodc
                    json_data[current_id][time_idx]["support_type"] |= 0b01
                    json_data[current_id][time_idx]["sat_type"] = detect_sat_type(current_id)
                else: # B1C/B2A
                    json_data[current_id][time_idx]["iode"] = iode_aode
                    json_data[current_id][time_idx]["deltaA"] = deltaA_sqrtA
                    json_data[current_id][time_idx]["iodc"] = iodc_aodc
                    json_data[current_id][time_idx]["delta_n0_dot"] = delta_n0_dot
                    json_data[current_id][time_idx]["sat_type"] = sat_type
                    json_data[current_id][time_idx]["A_DOT"] = a_dot
                    json_data[current_id][time_idx]["Data"] = data 
                    json_data[current_id][time_idx]["support_type"] |= 0b10

            except Exception as e:
                print(f"AN ERROR OCCURRED WHEN PROCESSING LINE: {line}")
                print(f"Line: {ephemeris[line]}")
                print(f"Error: {str(e)}")
                exit(0)


    with open(ephemeris_output_path, "w") as f:
        json.dump(json_data, f, indent=4)


if __name__ == "__main__":
    import sys
    ifile = sys.argv[1]
    ofile = sys.argv[2]
    ofile2 = sys.argv[3]
    if ifile == "" or ofile == "":
        print("*** Convert BDS CNAV ephemeris to JSON ***")
        print(
            "Usage: \
            python convert_ephemeris_to_json.py [input_files] [ephemeris_file] [ionosphere_file]\
            input_files is sperated by comma, like 'file1,file2'")
        exit(0)
    if ifile == ofile:
        c = input(
            "input file is the same as output file, are you sure to overwrite it? (y/[n])")
        if c != "y":
            exit(0)
    render_ephemeris(ifile.split(","), ofile, ofile2)
