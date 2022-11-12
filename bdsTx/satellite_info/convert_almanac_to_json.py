'''
Author: symlpigeon
Date: 2022-11-08 15:13:17
LastEditTime: 2022-11-09 11:57:12
LastEditors: symlpigeon
Description: 解析历书数据，把历书数据转换为适合电脑读取的格式（也更加适合人类阅读）
FilePath: /sim_bds/python/satellite_info/convert_almanac_to_json.py
'''

import json

# why don't you use csv or json???
# 还是尽可能的希望做到只解析一次，后面采用存储的json读取


def get_data(x): return list(filter(None, x.split(' ')))[-1]


def render_almanac(input_filename: str, output_filename: str) -> None:
    with open(input_filename, "r") as f:
        almanac = f.read()
    # 先按照行分割
    almanac = almanac.split("\n")
    json_data = {}
    current_id = 0
    for line in almanac:
        if line.startswith("********"):
            # 取出PRN-ID，写的不够优雅
            current_id = int(line[34:36])
            json_data[current_id] = {}
            continue
        if line == "":
            # 空行
            continue
        match line[0:3]:  # 赞美Python 3.10！
            case "ID:":
                # Stellaris ID
                pass
            case "Hea":  # Health
                json_data[current_id]["Health"] = int(get_data(line))
            case "Ecc":  # Eccentricity
                json_data[current_id]["Eccentricity"] = float(get_data(line))
            case "Tim":  # Time of Applicability
                json_data[current_id]["TimeOfApplicability"] = float(
                    get_data(line))
            case "Orb":  # Orbital Inclination
                json_data[current_id]["OrbitalInclination"] = float(
                    get_data(line))
            case "Rat":  # Rate of Right Ascension
                json_data[current_id]["RateOfRightAscension"] = float(
                    get_data(line))
            case "SQR":  # Square Root of Semi-Major Axis
                json_data[current_id]["SquareRootOfSemiMajorAxis"] = float(get_data(
                    line))
            case "Rig":  # Right Ascen at Week
                json_data[current_id]["RightAscenAtWeek"] = float(
                    get_data(line))
            case "Arg":  # Argument of Perigee
                json_data[current_id]["ArgumentOfPerigee"] = float(
                    get_data(line))
            case "Mea":  # Mean Anomaly
                json_data[current_id]["MeanAnomaly"] = float(get_data(line))
            case "Af0":  # Clock Correction Coefficient
                json_data[current_id]["ClockTimeBiasCoefficient"] = float(get_data(
                    line))
            case "Af1":  # Clock Correction Coefficient
                json_data[current_id]["ClockTimeDriftCoefficient"] = float(get_data(
                    line))
            case "wee":  # Week Number
                json_data[current_id]["WeekNumber"] = int(get_data(line))
    with open(output_filename, "w") as f:
        json.dump(json_data, f, indent=4)


if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    output_filename = sys.argv[2]
    if filename == "" or output_filename == "":
        print("Usage: python convert_almanac_to_json.py input_filename output_filename")
        exit(1)
    if filename == output_filename:
        c = input("Are you sure you want to overwrite the original file? (y/n)")
        if c != "y":
            exit(0)
    render_almanac(filename, output_filename)
