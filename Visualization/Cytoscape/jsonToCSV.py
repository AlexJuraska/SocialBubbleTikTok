#######################################
# Basic edges and nodes for Cytoscape #
#######################################

import json
import csv

DATA_FILE:str = ".json"
COMM_FILE:str = ".json"
OUTPUT_FILE_INTERACTIONS:str = ".csv"

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

with open(COMM_FILE, "r", encoding="utf-8") as f:
    commData = json.load(f)

csvDataEdges = [
    ["user1", "user2", "interaction", "directed"],
]

for userFrom in commData["0"]["members"]:
    if userFrom not in data:
        continue
    info = data[userFrom]

    for userTo in info["following"]:
        if userFrom == userTo:
            continue

        newEntry = []
        if userFrom in data[userTo]["following"]:
            if [userTo, userFrom, "FALSE"] not in csvDataEdges:
                newEntry = [userFrom, userTo, "follows", "FALSE"]
        else:
            newEntry = [userFrom, userTo, "follows", "TRUE"]

        if len(newEntry) > 0:
            csvDataEdges.append(newEntry)

    for commenter in info["commenters"]:
        newEntry = [commenter, userFrom, "commentedOn", "TRUE"]
        csvDataEdges.append(newEntry)


with open(OUTPUT_FILE_INTERACTIONS, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(csvDataEdges)