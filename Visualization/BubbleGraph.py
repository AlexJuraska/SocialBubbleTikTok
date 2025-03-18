import json
from pyvis.network import Network
import networkx as nx

class BubbleGraph:
    def __init__(self, dataFile: str):
        self.dataFile: str = dataFile

        self.edges: set[tuple[int, int]] = set()

        self.graph: nx.DiGraph = nx.DiGraph()

    def visualize(self) -> None:
        """
        Function visualizes the selected edges
        :return: None
        """

        if len(self.edges) == 0:
            raise Exception('No added edges')

        self.graph.add_edges_from(self.edges)

        net = Network(notebook=True, directed=True)
        net.from_nx(self.graph)
        net.show("pyvisGraph.html")

    def addEdges(self, connections:bool = False) -> None:
        """
        Function adds edges to the graph
        :param connections: True/False whether to add connection edges
        :return: None
        """

        if not any([connections]):
            raise Exception('At least one of the entry parameters must be True')

        if connections:
            self.edges = self.edges.union(self.__getConnections())

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

if __name__ == "__main__":
    b = BubbleGraph("../Data/Information/data.json")
    b.addEdges(True)
    print(len(b.edges))
    # b.visualize()