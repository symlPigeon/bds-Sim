'''
Author: symlPigeon 2163953074@qq.com
Date: 2023-02-12 11:37:25
LastEditTime: 2023-02-12 12:17:59
LastEditors: symlPigeon 2163953074@qq.com
Description: ranging code generator for B3I
FilePath: /bds-Sim/bdsTx/coding/b3i_ranging_code.py
'''

import json

from bdsTx.coding.gold_code import b3i_generate_gold_code


def load_phase(filename: str = "prn_data/b3i_phase_data.json") -> dict:
    with open(filename, "r") as f:
        data = json.load(f)
    return data

def export_b3i_ranging_code(
    filepath: str = "prn_data/b3i_phase_data.json", outpath: str = "ranging_code/b3i/"
) -> None:
    phase_data = load_phase(filepath)
    for entry in phase_data["data"]:
        json_data = {}
        json_data["prn"] = entry["prn"]
        phase = entry["init_phase"]
        code = b3i_generate_gold_code(int(phase[::-1], 2))
        json_data["prn"] = "".join(
            [str(int(code[i : i + 3], 2)) for i in range(0, len(code), 3)]
        )
        with open(outpath + f"prn-{entry['prn']}.json", "w") as f:
            f.write(json.dumps(json_data, indent=4))
            
            
if __name__ == "__main__":
    # Generating B3I ranging code
    export_b3i_ranging_code()
    print("Generated!")
    # verify
    with open("prn_data/b3icode.csv", "r") as f:
        code_data = f.read()
    code_data = code_data.split("\n")
    while "" in code_data:
        code_data.remove("")
    for prn in range(1, 64):
        v_code = "".join(i for i in code_data[prn - 1].split(","))
        v_code = "".join(
            [str(int(v_code[i : i + 3], 2)) for i in range(0, len(v_code), 3)]
        )
        with open("ranging_code/b3i/prn-" + str(prn) + ".json", "r") as f:
            t_code = json.load(f)["prn"]
        if v_code != t_code:
            print(v_code)
            print(t_code)
            print(f"prn-{prn} is wrong!")
            exit(1)
