import json

with open("ipc.json", "r", encoding='utf-8') as f:
    data = json.load(f)

    new_json = json.dumps(data, indent=1, sort_keys=True)
# print(new_json[2])
print(new_json[:200])
# with open("ipc_dataset.json", "w") as f:  
#     json.dump(data, f)

