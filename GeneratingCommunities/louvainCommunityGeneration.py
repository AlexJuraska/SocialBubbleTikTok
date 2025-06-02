"""
This script generates communities using Louvain community detection algorithm.
"""

from GeneratingCommunities.fileGetter import getData
from GeneratingCommunities.fileGetter import LOUVAIN_DATA_SOURCE as DATA_OUTPUT

from RelationshipExtractor import LouvainExtractor
import json
import time

try:
    data = getData()
except:
    data = {}

extractor = LouvainExtractor()

start = time.time()
usersByCommunity, connections = extractor.extract(data)

print("---------------------------------------------------------------------")
print(f"Louvain separation took {time.time() - start} seconds")

checkpoint = time.time()

communities: dict[str, dict[str, set | dict[str, int]]] = dict()
for user, community in usersByCommunity.items():
    community = str(community)
    if user == "":
        continue
    if community not in communities:
        communities[community] = {"members" : {user, }}
    else:
        if "members" not in communities[community]:
            communities[community] = {"members": {user, }}
        else:
            communities[community]["members"].add(user)


for conFrom, conTo  in connections:
    conFromComm = str(usersByCommunity[conFrom])
    conToComm = str(usersByCommunity[conTo])

    if conFromComm != conToComm:
        if "connections" not in communities[conFromComm]:
            communities[conFromComm]["connections"] = {conToComm : 1}
        else:
            if conToComm not in communities[conFromComm]["connections"]:
                communities[conFromComm]["connections"][conToComm] = 1
            else:
                communities[conFromComm]["connections"][conToComm] += 1

        if "connections" not in communities[conToComm]:
            communities[conToComm]["connections"] = {conFromComm : 1}
        else:
            if conFromComm not in communities[conToComm]["connections"]:
                communities[conToComm]["connections"][conFromComm] = 1
            else:
                communities[conToComm]["connections"][conFromComm] += 1

for user in data:
    hashtags: list[str] = data[user]["hashtags"]
    commentsPosted: list[dict[str]] = data[user]["commentsPosted"]
    userComm = str(usersByCommunity[user])

    if "hashtags" not in communities[userComm]:
        communities[userComm]["hashtags"] = set()
    communities[userComm]["hashtags"] = communities[userComm]["hashtags"].union(set(hashtags))


    if "comments" not in communities[userComm]:
        communities[userComm]["comments"] = set()

    for comment in commentsPosted:
        communities[userComm]["comments"].add(comment["text"])

communities: dict[str, dict[str, list | dict[str, int]]]
for com in communities:
    communities[com]["members"] = list(communities[com]["members"])
    if "connections" not in communities[com]:
        communities[com]["connections"] = dict()
    communities[com]["hashtags"] = list(communities[com]["hashtags"])
    communities[com]["comments"] = list(communities[com]["comments"])

with open(DATA_OUTPUT, "w") as f:
    json.dump(communities, f, indent=3)

# print("---------------------------------------------------------------------")
print(f"Louvain data saved to '{DATA_OUTPUT}'. It took {time.time() - checkpoint} seconds.")