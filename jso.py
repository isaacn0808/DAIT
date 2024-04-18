import json

def uploadData(recJson):
    with open("data.json", "r") as file:
        global data
        data = json.load(file)
    # json data processing
    if (list(recJson.keys())[0] == "uuid"):
        data["users"].append(recJson)
    elif list(recJson.keys())[0] == "maze":
        for i, user in enumerate(data["users"]):
            if user["uuid"] == recJson["uuid"]:
                data["users"][i]["mazes"].append(recJson["maze"])
                data["users"][i]["selections"].append(recJson["selection"]) 
    elif list(recJson.keys())[0] == "time":
        for i, user in enumerate(data["users"]):
            if user["uuid"] == recJson["uuid"]:
                data["users"][i]["time"] = recJson["time"]
    else:
        print("Invalid Data dump")
    
    updated = json.dumps(data)
    with open("data.json", "w") as outfile:
        outfile.write(updated)