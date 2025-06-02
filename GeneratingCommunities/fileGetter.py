import json

# DATA_SOURCE = "../Data/Information/data.json"
DATA_SOURCE = "../CustomData/dataTestComplexTopics1.json"
def getData():
    try:
        with open(DATA_SOURCE, "r", encoding='utf-8') as file:
            return json.load(file)
    except:
        raise RuntimeError("Data source is wrong")

# LOUVAIN_DATA_SOURCE = "../Data/Information/louvainCommunities.json"
LOUVAIN_DATA_SOURCE = "../CustomData/customLouvainCommunities.json"
def getLouvainData():
    try:
        with open(LOUVAIN_DATA_SOURCE, "r", encoding='utf-8') as file:
            return json.load(file)
    except:
        raise RuntimeError("Louvain data source is wrong")

# LEIDEN_DATA_SOURCE = "../Data/Information/leidenCommunities.json"
LEIDEN_DATA_SOURCE = "../CustomData/customLeidenCommunities.json"
def getLeidenData():
    try:
        with open(LEIDEN_DATA_SOURCE, "r", encoding='utf-8') as file:
            return json.load(file)
    except:
        raise RuntimeError("Leiden data source is wrong")