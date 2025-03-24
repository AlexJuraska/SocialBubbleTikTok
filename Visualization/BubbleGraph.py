import json
from pyvis.network import Network
import networkx as nx

class BubbleGraph:
    def __init__(self, dataFile: str, hashtagFile:str):
        self.dataFile: str = dataFile
        self.hashtagFile: str = hashtagFile

        self.graph: nx.DiGraph = nx.DiGraph()

        # Graph style preset
        self.graphStyle = {
            # "fillColor" : "blue",
            # "highlightFillColor": "darkorange",
            "borderWidth": 1
        }

    def resetGraph(self) -> None:
        """
        Function clears the graph of all nodes and edges
        :return: None
        """
        self.graph.clear()

    def __addEdges(self, newEdges: set[tuple[str, str]]) -> None:
        """
        Function adds edges to the graph
        :return: None
        """

        if not isinstance(newEdges, set):
            raise TypeError('newEdges must be a set[tuple[str,str]]')

        if len(newEdges) < 1:
            raise Exception('newEdges must contain at least one edge')

        self.graph.add_edges_from(newEdges)

    def __addSizedNodes(self, nodes: dict[str: int]) -> None:
        """
        Function adds nodes with correct sizes to the graph.
        Each node will have a different from the default highlight color.
        :param nodes: Dict containing {name: size}
        :return: None
        """
        for node in nodes:
            self.graph.add_node(node,
                                size=5*nodes[node],
                                borderWidth = self.graphStyle['borderWidth'],
                                labelHighlightBold = True,
                                # color = { "highlight" : self.graphStyle["fillColor"] },
                                # highlightColor = self.highlightStyle["fillColor"],
                                # highlightBorderColor = self.highlightStyle["borderColor"]
                                # physics = False
                                )

    def visualizeCommenters(self) -> None:
        """
        Function visualizes the commenters
        :return: None
        """

        self.resetGraph()

        self.__addEdges(self.__getCommenters())

        net = Network(notebook=True, directed=True)
        net.from_nx(self.graph)
        net.show("pyvisGraph.html")

    def __getCommenters(self) -> set[tuple[str, str]]:
        """
        Gets the commenter connections from the class dataFile and returns a set of tuples
        :return: Set of tuples representing oriented graph edges
        """

        with open(self.dataFile, "r") as file:
            data = json.load(file)

        retCommenters = set()

        for user in data:
            for connection in data[user]["commenters"]:
                retCommenters.add((connection, user))

        return retCommenters



    def __getConnections(self) -> set[tuple[str, str]]:
        """
        Gets the connections from the class dataFile and returns a set of tuples
        :return: Set of tuples representing oriented graph edges
        """

        with open(self.dataFile, "r") as file:
            data = json.load(file)

        retConnections = set()

        for user in data:
            for connection in data[user]["connections"]:
                retConnections.add((user, connection))

        return retConnections

    def visualizeHashtags(self) -> None:
        """
        Function visualizes the hashtags
        :return: None
        """

        self.resetGraph()

        sizes, edges = self.__getHashtags()

        self.__addSizedNodes(sizes)
        self.__addEdges(edges)

        net = Network(notebook=True)
        # net.barnes_hut()
        net.force_atlas_2based()
        net.from_nx(self.graph)
        net.show("hashtagsGraph.html")

    def __getHashtags(self) -> (dict[str: int], set[tuple[str, str]]):
        """
        Gets the connections from the class hashtagFile and returns the node sizes as well as a set of tuples
        :return: Dict containing node sizes and a set of tuples representing oriented graph edges
        """

        with open(self.hashtagFile, "r") as file:
            data = json.load(file)

        sizes: dict[str: int] = {}
        edges: set[tuple[str, str]] = set()

        for hashtag in data:
            sizes[hashtag] = data[hashtag]["count"]
            for connection in data[hashtag]["connections"]:
                if not (hashtag, connection) in edges and not (connection, hashtag) in edges:
                    edges.add((hashtag, connection))

        return sizes, edges


if __name__ == "__main__":
    b = BubbleGraph("../Data/Information/data.json", "../Data/Information/hashtags.json")
    b.visualizeHashtags()