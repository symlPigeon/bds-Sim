import json

with open("./b3i_data.txt", "r") as f:
    data = f.read()
    
data = data.split("\n")
while "" in data:
    data.remove("")
    
output_data = {
    "data" : []
}

for line in data:
    e = line.split(" ")
    prn = int(e[0])
    init_phase_num = int(e[4])
    init_phase = e[5]
    
    output_data["data"].append({
        "prn": prn,
        "init_phase_num": init_phase_num,
        "init_phase": init_phase
    })
    
with open("./b3i_phase_data.json", "w") as f:
    json.dump(output_data, f, indent=4)