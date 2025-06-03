##################################################
# Classes for the community detection extraction #
##################################################

import igraph as ig
import leidenalg
from collections import defaultdict

class RelationshipExtractor:
    def extract(self, data: dict) -> ( dict[str, int] | set[str], set[tuple[str, str]] ):
        raise NotImplementedError("Abstract method")

class LeidenExtractor(RelationshipExtractor):

    def __init__(self,
                 followingWeight: float = 1.0,
                 commentedWeight: float = 2.0,
                 hashtagWeight: float = 0.5,
                 ):
        if not all((isinstance(followingWeight, float),
                    isinstance(commentedWeight, float),
                    isinstance(hashtagWeight, float))):
            raise TypeError('All weights must be floats')

        self.__followingWeight = followingWeight
        self.__commentedWeight = commentedWeight
        self.__hashtagWeight = hashtagWeight

        self.__providedData = None
        self.__hashtagUsers = None

    def extract(self, data: dict) -> tuple[ dict[str, int], set[tuple[str, str]] ]:

        self.__providedData = data
        self.__hashtagUsers = self.__preprocessHashtags()

        weightedData = self.__weighData()

        graph = self.__createGraph(weightedData)

        partition = leidenalg.find_partition(
            graph,
            leidenalg.ModularityVertexPartition,
            weights=graph.es["weight"]
        )

        usersByCommunity: dict[str, int]
        usersByCommunity = {
            graph.vs[i]['name']: communityId
            for i, communityId in enumerate(partition.membership)
        }

        connections: set[tuple[str, str]] = set(weightedData.keys())

        return usersByCommunity, connections

    def __preprocessHashtags(self) -> dict[str, set[str]]:
        hashtagDict = defaultdict(set)
        for user, info in self.__providedData.items():
            for tag in info.get('hashtags', []):
                hashtagDict[tag].add(user)

        return dict(hashtagDict)

    def __weighData(self) -> dict[tuple[str, str], float]:
        edgeWeights = defaultdict(float)

        for user, info in self.__providedData.items():

            for followed in info.get('following', []):

                edgeWeights[(user, followed)] += self.__followingWeight

            for commentedOn in info.get('commentedOn', []):
                edgeWeights[(user, commentedOn)] += self.__commentedWeight

            userHashtags = set(info.get('hashtags', []))

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

class LouvainExtractor(RelationshipExtractor):
    def __init__(self,
                 followingWeight: float = 1.0,
                 commentedWeight: float = 2.0,
                 hashtagWeight: float = 0.5,
                 ):
        if not all((isinstance(followingWeight, float),
                    isinstance(commentedWeight, float),
                    isinstance(hashtagWeight, float))):
            raise TypeError('All weights must be floats')

        self.__followingWeight = followingWeight
        self.__commentedWeight = commentedWeight
        self.__hashtagWeight = hashtagWeight

        self.__providedData = None
        self.__hashtagUsers = None

    def extract(self, data: dict) -> ( dict[str, int] | set[str], set[tuple[str, str]] ):

        self.__providedData = data
        self.__hashtagUsers = self.__hashtagUsers = self.__preprocessHashtags()

        weightedData = self.__weighData()

        undirGraph = self.__createGraph(weightedData)

        partition = undirGraph.community_multilevel(weights="weight")

        usersByCommunity: dict[str, int]
        usersByCommunity = {
            undirGraph.vs[i]['name']: communityId
            for i, communityId in enumerate(partition.membership)
        }

        connections: set[tuple[str, str]] = set(weightedData.keys())

        return usersByCommunity, connections

    def __preprocessHashtags(self) -> dict[str, set[str]]:
        hashtagDict = defaultdict(set)
        for user, info in self.__providedData.items():
            for tag in info.get('hashtags', []):
                hashtagDict[tag].add(user)

        return dict(hashtagDict)

    def __weighData(self) -> dict[tuple[str, str], float]:
        edgeWeights = defaultdict(float)

        for user, info in self.__providedData.items():

            for followed in info.get('following', []):

                edgeWeights[(user, followed)] += self.__followingWeight

            for commentedOn in info.get('commentedOn', []):
                edgeWeights[(user, commentedOn)] += self.__commentedWeight

            userHashtags = set(info.get('hashtags', []))

            for hashtag in userHashtags:
                for otherUser in self.__hashtagUsers[hashtag]:
                    if user == otherUser:
                        continue
                    edgeWeights[(user, otherUser)] += self.__hashtagWeight

        return edgeWeights

    def __createGraph(self, weightedEdges: dict[tuple[str, str], float]) -> ig.Graph:
        """
        :returns: an undirected graph where the weight of edges is the sum of their directions weights
        """

        graph = ig.Graph(directed=True)

        nodes = set(self.__providedData.keys())
        for u1, u2 in weightedEdges.keys():
            nodes.update([u1, u2])
        graph.add_vertices(list(nodes))

        edges = list(weightedEdges.keys())
        weights = list(weightedEdges.values())
        graph.add_edges(edges)
        graph.es["weight"] = weights

        graph = graph.as_undirected(combine_edges="sum")

        return graph