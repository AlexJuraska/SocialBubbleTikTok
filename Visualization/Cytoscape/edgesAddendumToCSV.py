############################################################
# Adding the users themselves as additional info for edges #
############################################################

import json
import csv

DATA_FILE:str = ".json"
OUTPUT_FILE_FOLLOWING:str = ".csv"

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

csvDataEdges = [
    ["shared name", "user1", "user2"],
]

for userFrom, info in data.items():

    for userTo in info["following"]:
        if userFrom == userTo:
            continue

        newEntry = []
        if userFrom in data[userTo]["following"]:
            if [f"{userTo} (follows) {userFrom}", userTo, userFrom] not in csvDataEdges:
                newEntry = [f"{userFrom} (follows) {userTo}", userFrom, userTo]
        else:
            newEntry = [f"{userFrom} (follows) {userTo}", userFrom, userTo]

        if len(newEntry) > 0:
            csvDataEdges.append(newEntry)

    for commenter in info["commenters"]:
        newEntry = [f"{commenter} (commentedOn) {userFrom}", commenter, userFrom]

        csvDataEdges.append(newEntry)

with open(OUTPUT_FILE_FOLLOWING, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(csvDataEdges)