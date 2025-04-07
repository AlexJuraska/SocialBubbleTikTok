import json
from typing import Optional
import igraph as ig
import leidenalg
from collections import defaultdict

class LeidenSeparation:
    def __init__(self, data: dict,
                       followingWeight: Optional[float] = 1.0,
                       commentedWeight: Optional[float] = 2.0,
                       hashtagWeight: Optional[float] = 0.5,
                 ):
        if data is None or len(data) == 0:
            raise ValueError("Data is empty")

        if not all((isinstance(followingWeight, float),
                    isinstance(commentedWeight, float),
                    isinstance(hashtagWeight, float))):
            raise TypeError('All weights must be floats')

        self.__providedData = data
        self.__followingWeight = followingWeight
        self.__commentedWeight = commentedWeight
        self.__hashtagWeight = hashtagWeight

        self.__hashtagUsers:defaultdict[str, set[str]] = defaultdict(set)
        self.__data: list[list[str]]

        self.__runAlgorithm()

    def __preprocessHashtags(self):
        for user, info in self.__providedData.items():
            for tag in info.get('hashtags', []):
                self.__hashtagUsers[tag].add(user)

    def __weighData(self) -> dict[tuple[str, str], float]:
        edgeWeights = defaultdict(float)

        for user, info in self.__providedData.items():
            for followed in info.get('following', []):
                edgeWeights[(user, followed)] += self.__followingWeight

            for commentedOn in info.get('commentedOn', []):
                edgeWeights[(user, commentedOn)] += self.__commentedWeight

            userHashtags = set(info.get('hashtags', []))
            if len(userHashtags) == 0:
                continue

            for hashtag in userHashtags:
                for otherUser in self.__hashtagUsers[hashtag]:
                    if user == otherUser:
                        continue
                    edgeWeights[(user, otherUser)] += self.__hashtagWeight

        return edgeWeights

    def __createGraph(self, weightedEdges: dict[tuple[str, str], float]) -> ig.Graph:
        graph = ig.Graph(directed=True)

        nodes = set(self.__providedData.keys())
        for u1, u2 in weightedEdges.keys():
            nodes.update([u1, u2])
        graph.add_vertices(list(nodes))

        edges = list(weightedEdges.keys())
        weights = list(weightedEdges.values())
        graph.add_edges(edges)
        graph.es["weight"] = weights

        return graph

    def __runAlgorithm(self):

        weightedData = self.__weighData()

        graph = self.__createGraph(weightedData)

        partition = leidenalg.find_partition(
            graph,
            leidenalg.ModularityVertexPartition,
            weights=graph.es["weight"]
        )

        self.__data = [
            [graph.vs[idx]['name'] for idx in community]
            for community in partition
        ]

    def __getitem__(self, key):
        return self.__data[key]

    def __iter__(self) -> iter:
        return iter(self.__data)

    def __len__(self) -> int:
        return len(self.__data)

    def __reversed__(self) -> reversed:
        return reversed(self.__data)

    def __str__(self):
        returnStr = f"Found {len(self)} communities."
        for i, community in enumerate(self.__data):  # Show first 5 communities
            returnStr += f"Community {i+1}: {', '.join(community)}\n\n"

        return returnStr

if __name__ == "__main__":
    with open("../Data/Information/data.json", "r") as file:
        data = json.load(file)

    lS = LeidenSeparation(data)

    print(lS)