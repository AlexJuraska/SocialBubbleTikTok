###########################################################################
# Adding political spectrum information to the graph (specific community) #
###########################################################################

import json
import csv

DATA_FILE:str = ".json"
COMM_FILE:str = ".json"
OUTPUT_FILE:str = ".csv"

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

with open(COMM_FILE, "r", encoding="utf-8") as f:
    commData = json.load(f)

csvDataNodesIdeology = [
    ["name", "ideology", "ideologyColor", "communityIDColor"],
]

representatives = {
        "con" : ["@smer_sd_tiktok", "@hlas_socialna_demokracia", "@peter_pellegrini"],
        "lib" : ["@michalsimecka", "@richardsulik_", "@progresivne_slovensko", "@ivan.korcok"],
        "new" : ["@dennikntiktok"]
    }
specs = {
        "con": ("conservative","#eb4034"),
        "lib": ("liberal","#348feb"),
        "new": ("news","#eff224"),
        "cen": ("centrist", "#b300b3")
    }

communityColor = "#ecd0db"

selectedCommunityMembers = commData["0"]["members"]
for user in selectedCommunityMembers:
    if user not in data:  # Just in case
        continue
    info = data[user]

    most = {
        "con" : 0,
        "lib" : 0,
        "new" : 0
    }

    for key, group in representatives.items():
        if user in group:
            name, color = specs[key]
            csvDataNodesIdeology.append([user, name, color, communityColor])
            skipToNext = True
            break
    else:
        skipToNext = False

    if skipToNext:
        skipToNext = False
        continue

    if len(info["following"]) != 0:
        fol = info["following"]
    else:
        fol = info["followers"]

    for follow in fol:
        if user == follow or follow not in selectedCommunityMembers:
            continue

        for key, group in representatives.items():
            if follow in group:
                most[key] += 1

    for commenter in info["commentedOn"] :
        if user == commenter or commenter not in selectedCommunityMembers:
            continue

        for key, group in representatives.items():
            if commenter in group:
                most[key] += 1


    if most["new"] > max(most["lib"], most["con"]):
        key = "new"
    elif most["lib"] == most["con"]:
        key = "cen"
    elif most["lib"] > most["con"]:
        key = "lib"
    else:
        key = "con"

    name, color = specs[key]
    csvDataNodesIdeology.append([user, name, color, communityColor])

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(csvDataNodesIdeology)