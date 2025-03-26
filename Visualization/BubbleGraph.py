import json
from pyvis.network import Network
import networkx as nx

class BubbleGraph:
    def __init__(self, dataFile: str, hashtagFile:str):
        self.dataFile: str = dataFile
        self.hashtagFile: str = hashtagFile

        self.graph: nx.Graph = nx.Graph()

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

    def visualizeGraph(self, webFileName:str = "graph.html"):
        """
        Function visualizes the graph of all the selected nodes and edges.
        If no nodes or edges detected, raises an error.
        :param webFileName:
        :return:
        """
        if self.graph.number_of_edges() == 0 and self.graph.number_of_nodes() == 0:
            raise Exception('Graph has no edges nor nodes')

        if not webFileName.endswith(".html"):
            raise ValueError("File name must end with .html")

        pyvisNet = Network(notebook=True)
        pyvisNet.from_nx(self.graph)

        #TODO javascript

        pyvisNet.show_buttons(filter_=["physics"])
        pyvisNet.show(webFileName)

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

    def __addNodes(self, nodes: dict[str: int] | set[str]) -> None:
        """
        Function adds nodes to the graph. If nodes is a dictionary containing size,
        those sizes will be reflected on each node.
        :param nodes: Dict containing {name: size}
        :return: None
        """

        if not isinstance(nodes, dict) and not isinstance(nodes, set):
            raise TypeError('nodes must be a dict[str, int] or set[str]')

        if len(nodes) < 1:
            raise Exception('nodes must not be empty')

        for node in nodes:
            if isinstance(nodes, dict):
                self.graph.add_node(node, size=5*nodes[node], labelHighlightBold = True)
            else:
                self.graph.add_node(node, labelHighlightBold = True)

    def addCommentersToGraph(self) -> None:
        """
        Adds the commenter nodes and edges to the graph
        :return: None
        """

        commenters, connections = self.__getCommenters()

        self.__addNodes(commenters)

        self.__addEdges(connections)


    def __getCommenters(self) -> (set[str], set[tuple[str, str]]):
        """
        Gets the commenter connections from the class dataFile and returns a set of tuples
        :return: Set of commenters usernames and a set of tuples representing graph edges
        """

        with open(self.dataFile, "r") as file:
            data = json.load(file)

        retConnections = set()
        retCommenters = set(data.keys())

        for user in data:
            for connection in data[user]["commenters"]:
                if (connection, user) not in retConnections and (user, connection) not in retConnections:
                    retConnections.add((connection, user))

        return retCommenters, retConnections

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

    def addHashtagsToGraph(self) -> None:
        """
        Adds the hashtag nodes and edges to the graph
        :return: None
        """
        sizes, edges = self.__getHashtags()

        self.__addNodes(sizes)
        self.__addEdges(edges)

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
    # b.addHashtagsToGraph()
    # b.visualizeGraph("hashtagGraph.html")