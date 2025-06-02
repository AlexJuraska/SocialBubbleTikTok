###################################################################
# Additional leiden community information for nodes for Cytoscape #
###################################################################

import json
import csv
import random

DATA_FILE:str = "../../CustomData/customLeidenCommunities.json"
OUTPUT_FILE_LEIDEN:str = "customLeidenData.csv"

def getColor() -> str:
    R = random.randint(180, 255)
    G = random.randint(180, 255)
    B = random.randint(180, 255)
    return f"#{R:02x}{G:02x}{B:02x}"

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

csvDataEdges = [
    ["user", "leidenCommunityID", "communityIDColor"],
]

for comm, info in data.items():
    commColor = getColor()
    for member in info["members"]:
        csvDataEdges.append([member, comm, commColor])

with open(OUTPUT_FILE_LEIDEN, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(csvDataEdges)