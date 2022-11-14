'''
Author: symlpigeon
Date: 2022-11-08 19:22:21
LastEditTime: 2022-11-14 17:15:57
LastEditors: symlpigeon
Description: 将星历文件转换为json格式
FilePath: /bds-Sim/bdsTx/satellite_info/convert_ephemeris_to_json.py
'''

import json
import calendar
from time_system import utc2bds


def get_data(x): return list(filter(None, x.split(' ')))[-1]


def render_ephemeris(ephemeris_file_path: str, ephemeris_output_path: str, iono_corr_path: str) -> None:
    '''
    将星历文件转换为json格式
    '''
    with open(ephemeris_file_path, 'r') as f:
        ephemeris = f.read()
    ephemeris = ephemeris.split("\n")
    while "" in ephemeris:
        ephemeris.remove("")
    # 分割文件
    idx = 0
    while get_data(ephemeris[idx]) != "HEADER":
        idx += 1

    # -------------
    #   电离层参数
    # -------------

    iono_corr_lines_type1 = []
    iono_corr_lines_type2 = []
    for i in range(0, idx):
        if get_data(ephemeris[i]) == "CORR":
            if ephemeris[i][0:4] == "BDSA" or ephemeris[i][0:4] == "BDSB":
                iono_corr_lines_type1.append(ephemeris[i])
            elif ephemeris[i][0:4] == "BDS1" or ephemeris[i][0:4] == "BDS2" or ephemeris[i][0:4] == "BDS3":
                iono_corr_lines_type2.append(ephemeris[i])
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
        with open(iono_corr_path, 'w') as f:
            json.dump({"klobuchar": klobuchar_iono_corr,
                      "bdgim": bdgim_iono_corr}, f, indent=4)
    else:
        print("Maybe Invalid Iono Correction Data, skipping...")

    # -------------
    #   卫星星历
    # -------------

    json_data = {}
    idx += 1  # 切到下一行
    for line in range(idx, len(ephemeris), 8):  # 一次8行
        try:
            current_id = ephemeris[line][1:3]
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
            json_data[current_id][time_idx] = {}
            _, toc = utc2bds(calendar.timegm((bdt_year, bdt_month, bdt_day, bdt_hour, bdt_minute, bdt_second, 0, 0, 0)))
            # 卫星钟偏系数a0, second
            a0 = float(ephemeris[line][23:42].strip())
            # 卫星钟漂系数a1, sec/sec
            a1 = float(ephemeris[line][42:61].strip())
            # 卫星钟漂移率系数a2, sec/sec^2
            a2 = float(ephemeris[line][61:].strip())
            # IODE/AODE 星历参数版本号/星历数据龄期
            iode_aode = int(float(ephemeris[line+1][4:23].strip()))
            # Crs 轨道半径正弦调和改正项振幅, meter
            Crs = float(ephemeris[line+1][23:42].strip())
            # 参考时刻卫星平均角速度和计算值之差Delta_n0, rad/sec
            delta_n0 = float(ephemeris[line+1][42:61].strip())
            # 参考时刻平近点角M0, rad
            M0 = float(ephemeris[line+1][61:].strip())
            # Cuc 纬度幅角的余弦调和改正项的振幅, rad
            Cuc = float(ephemeris[line+2][4:23].strip())
            # e 偏心率
            e = float(ephemeris[line+2][23:42].strip())
            # Cus 纬度幅角的正弦调和改正项的振幅, rad
            Cus = float(ephemeris[line+2][42:61].strip())
            # DeltaA_sqrtA 卫星轨道长半轴平方根, meter or meter^(1/2)
            deltaA_sqrtA = float(ephemeris[line+2][61:].strip())
            # Toe 参考时刻, sec
            Toe = float(ephemeris[line+3][4:23].strip())
            # Cic 轨道倾角余弦调和改正项的振幅, rad
            Cic = float(ephemeris[line+3][23:42].strip())
            # Omega0 升交点赤经, rad
            Omega0 = float(ephemeris[line+3][42:61].strip())
            # Cis 轨道倾角正弦调和改正项的振幅, rad
            Cis = float(ephemeris[line+3][61:].strip())
            # i0 参考时刻轨道倾角, rad
            i0 = float(ephemeris[line+4][4:23].strip())
            # Crc 轨道半径余弦调和改正项振幅, meter
            Crc = float(ephemeris[line+4][23:42].strip())
            # omega 近地点幅角， rad
            omega = float(ephemeris[line+4][42:61].strip())
            # Omega_dot 升交点赤经变化率, rad/sec
            Omega_dot = float(ephemeris[line+4][61:].strip())
            # IDOT 轨道倾角变化率, rad/sec
            IDOT = float(ephemeris[line+5][4:23].strip())
            # Data 电文来源，integer
            data = int(float(ephemeris[line+5][23:42].strip()))
            # BDT Week, 注意这个是平滑过渡的
            bdt_week = float(ephemeris[line+5][42:61].strip())
            # A_DOT / EMPTY, A_DOT对应长半轴变化率
            a_dot = float(ephemeris[line+5][61:].strip())
            # 空间信号精度指数及空间信号检测精度指数 或 SV accuracy
            sv_accuracy = int(float(ephemeris[line+6][4:23].strip()))
            # HS 卫星健康状态
            hs = int(float(ephemeris[line+6][23:42].strip()))
            # TGD / TGD1
            tgd = float(ephemeris[line+6][42:61].strip())
            # ISC / TGD2
            isc = float(ephemeris[line+6][61:].strip())
            # 信号发射时间，BDT周内秒
            signal_time = float(ephemeris[line+7][4:23].strip())
            # IODC / AODC 钟差参数版本号/时钟数据龄期
            iodc_aodc = int(float(ephemeris[line+7][23:42].strip()))
            # Delta n0 dot 参考时刻卫星平均角速度与计算值之差的变化率, rad/sec^2
            delta_n0_dot = float(ephemeris[line+7][42:61].strip())
            # SatType/Empty,卫星轨道类型或者留空
            sat_type = int(float(ephemeris[line+7][61:].strip()))

            json_data[current_id][time_idx]["toc"] = toc
            json_data[current_id][time_idx]["a0"] = a0
            json_data[current_id][time_idx]["a1"] = a1
            json_data[current_id][time_idx]["a2"] = a2
            json_data[current_id][time_idx]["iode/aode"] = iode_aode
            json_data[current_id][time_idx]["Crs"] = Crs
            json_data[current_id][time_idx]["delta_n0"] = delta_n0
            json_data[current_id][time_idx]["M0"] = M0
            json_data[current_id][time_idx]["Cuc"] = Cuc
            json_data[current_id][time_idx]["e"] = e
            json_data[current_id][time_idx]["Cus"] = Cus
            json_data[current_id][time_idx]["deltaA/sqrtA"] = deltaA_sqrtA
            json_data[current_id][time_idx]["Toe"] = Toe
            json_data[current_id][time_idx]["Cic"] = Cic
            json_data[current_id][time_idx]["Omega0"] = Omega0
            json_data[current_id][time_idx]["Cis"] = Cis
            json_data[current_id][time_idx]["i0"] = i0
            json_data[current_id][time_idx]["Crc"] = Crc
            json_data[current_id][time_idx]["omega"] = omega
            json_data[current_id][time_idx]["Omega_dot"] = Omega_dot
            json_data[current_id][time_idx]["IDOT"] = IDOT
            json_data[current_id][time_idx]["Data"] = data
            json_data[current_id][time_idx]["BDT Week"] = bdt_week
            json_data[current_id][time_idx]["A_DOT/EMPTY"] = a_dot
            json_data[current_id][time_idx]["sv_accuracy"] = sv_accuracy
            json_data[current_id][time_idx]["hs"] = hs
            json_data[current_id][time_idx]["tgd"] = tgd
            json_data[current_id][time_idx]["isc"] = isc
            json_data[current_id][time_idx]["signal_time"] = signal_time
            json_data[current_id][time_idx]["iodc/aodc"] = iodc_aodc
            json_data[current_id][time_idx]["delta_n0_dot"] = delta_n0_dot
            json_data[current_id][time_idx]["sat_type"] = sat_type

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
            python convert_ephemeris_to_json.py [input_file] [ephemeris_file] [ionosphere_file]")
        exit(0)
    if ifile == ofile:
        c = input(
            "input file is the same as output file, are you sure to overwrite it? (y/[n])")
        if c != "y":
            exit(0)
    render_ephemeris(ifile, ofile, ofile2)
