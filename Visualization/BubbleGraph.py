import json
from pyvis.network import Network
import networkx as nx

class BubbleGraph:
    def __init__(self, dataFile: str, hashtagFile:str):
        self.dataFile: str = dataFile
        self.hashtagFile: str = hashtagFile

        self.graph: nx.DiGraph = nx.DiGraph()

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


if __name__ == "__main__":
    b = BubbleGraph("../Data/Information/data.json", "../Data/Information/hashtags.json")
    b.visualizeCommenters()