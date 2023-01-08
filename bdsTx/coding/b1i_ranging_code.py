'''
Author: symlpigeon
Date: 2023-01-08 16:05:00
LastEditTime: 2023-01-08 20:47:53
LastEditors: symlpigeon
Description: 生成B1I信号测距码
FilePath: /bds-Sim/bdsTx/coding/b1i_ranging_code.py
'''

import json

from bdsTx.coding.gold_code import generate_gold_code


def get_phase_data_from_file(filename: str = "prn_data/b1i_phase_info.json") -> dict:
    with open(filename, "r") as f:
        data = json.load(f)
    return data


def export_b1i_ranging_code(filepath: str = "prn_data/b1i_phase_info.json", outpath: str = "ranging_code/b1i/") -> None:
    phase_data = get_phase_data_from_file(filepath)
    for entry in phase_data["data"]:
        json_data = {}
        json_data["prn"] = entry["prn"]
        phase = entry["phase"]
        code = generate_gold_code(phase)
        json_data["prn"] = "".join([str(int(code[i:i + 3], 2))
                       for i in range(0, len(code), 3)])
        with open(outpath + f"prn-{entry['prn']}.json", "w") as f:
            f.write(json.dumps(json_data, indent=4))
            
            
if __name__ == "__main__":
    # Generating B1I ranging code
    export_b1i_ranging_code()
    print("Generated!")
    # verify
    with open("prn_data/b1icode.csv", "r") as f:
        code_data = f.read()
    code_data = code_data.split("\n")
    while "" in code_data:
        code_data.remove("")
    for prn in range(1, 64):
        v_code = "".join(i for i in code_data[prn - 1].split(","))
        v_code = "".join([str(int(v_code[i:i + 3], 2))
                       for i in range(0, len(v_code), 3)])
        with open("ranging_code/b1i/prn-" + str(prn) + ".json", "r") as f:
            t_code = json.load(f)["prn"]
        if v_code != t_code:
            # print(v_code)
            # print(t_code)
            print(f"prn-{prn} is wrong!")