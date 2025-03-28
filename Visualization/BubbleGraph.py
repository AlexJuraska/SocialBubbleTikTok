import json
from pyvis.network import Network
import networkx as nx
import random
import time

class BubbleGraph:
    def __init__(self, dataFile: str, hashtagFile:str):
        self.dataFile: str = dataFile
        self.hashtagFile: str = hashtagFile

        self.graph: nx.Graph = nx.Graph()

    def resetGraph(self) -> None:
        """
        Function clears the graph of all nodes and edges
        :return: None
        """
        self.graph.clear()

    def visualizeGraph(self, webFileName:str = "graph.html",
                             coloringStyle:str = "none",
                       ) -> None:
        """
        Function visualizes the graph of all the selected nodes and edges.
        If no nodes or edges detected, raises an error.

        coloringStyle
        -------------
        "select": Selected node cluster,
        "cluster": All clusters in a separate color,
        "none": No coloring will take place

        :param webFileName: Name of the resulting html file (Must end with .html!)
        :param coloringStyle: Type of coloring in
        :return: None
        :raises Exception: If no nodes or edges detected
        :raises ValueError: If coloringStyle is not one of the supported ones or filename does not end with .html
        """
        if self.graph.number_of_edges() == 0 and self.graph.number_of_nodes() == 0:
            raise Exception('Graph has no edges nor nodes')

        if not webFileName.endswith(".html"):
            raise ValueError("File name must end with .html")

        if not isinstance(coloringStyle, str) or coloringStyle.lower() not in ["none", "select", "cluster"]:
            raise ValueError("Incorrect coloring style option - read function description")

        pyvisNet = Network(notebook=True, height="780px", width="100%")
        pyvisNet.from_nx(self.graph)
        pyvisNet.show_buttons(filter_=["physics"])
        pyvisNet.force_atlas_2based()

        if coloringStyle.lower() == "cluster":
            self.__colorNodeClusters(pyvisNet)

        pyvisNet.write_html(webFileName)

        if coloringStyle.lower() == "select":
            with open(webFileName, "r") as file:
                oldHtml = file.read()

            with open("graphScripts/selectedClusterHighlighting.js", "r") as file:
                selectedClusterHighlightCode = file.read()

            newHtml = oldHtml.replace("</body>", f"<script>{selectedClusterHighlightCode}</script></body>")

            with open(webFileName, "w") as file:
                file.write(newHtml)

    def __addEdges(self, newEdges: set[tuple[str, str]]) -> None:
        """
        Function adds edges to the graph
        :param newEdges: Set of tuples of strings representing edges
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
        those sizes will be reflected on each node. Sizes must be bigger than 0.
        :param nodes: Dict containing {name: size} or Set of str usernames
        :return: None
        """

        if not isinstance(nodes, dict) and not isinstance(nodes, set):
            raise TypeError('nodes must be a dict[str, int] or set[str]')

        if len(nodes) < 1:
            raise Exception('nodes must not be empty')

        for node in nodes:
            if isinstance(nodes, dict):

                if not isinstance(node, str) or not isinstance(nodes[node], int):
                    raise TypeError('Dictionary contents must be str: int')

                if nodes[node] <= 0:
                    raise ValueError("Node size must be higher than 0")

                self.graph.add_node(node, size=5*nodes[node], labelHighlightBold = True)
            else:
                if not isinstance(node, str):
                    self.resetGraph()
                    raise TypeError("Node usernames must be of type string!")

                self.graph.add_node(node, labelHighlightBold = True)

    def addCommentersToGraph(self, filterDict: dict[str: list] = {}) -> None:
        """
        Adds the commenter nodes and edges to the graph

        Filter
        ------
        "users": List of usernames whose connections we want to show,
        "showAllUsers": True/False whether to show all users,
        "hashtags": List of hashtags whose users we want to show

        :param filterDict: Dict containing things we want to leave
        :return: None
        """

        if not isinstance(filterDict, dict):
            sendFilter = {}
        else:
            sendFilter = filterDict

        commenters, connections = self.__getCommenters(sendFilter)

        self.__addNodes(commenters)

        self.__addEdges(connections)


    def __getCommenters(self, filterDict: dict) -> (set[str], set[tuple[str, str]]):
        """
        Gets the commenter connections from the class dataFile and returns a set of usernames
        and a set of tuples representing connections

        Filter
        ------
        "users": List of usernames whose connections we want to show,
        "showAllUsers": True/False whether to show all users,
        "hashtags": List of hashtags whose users we want to show

        :param filterDict: Dict containing things we want to leave
        :return: Set of commenters usernames and a set of tuples representing non-oriented graph edges
        """

        if "showAllUsers" in filterDict:
            showAllUsers = filterDict["showAllUsers"]
        else:
            showAllUsers = False

        with open(self.dataFile, "r") as file:
            data = json.load(file)

        retConnections = set()
        retCommenters = set()

        for user, info in data.items():

            if showAllUsers:
                retCommenters.add(user)

            if ("users" in filterDict.keys() and
                user not in filterDict["users"] and
                "hashtags" in filterDict.keys() and
                not any(filterHash in info["hashtags"] for filterHash in filterDict["hashtags"])):
                continue

            retCommenters.add(user)
            for connection in data[user]["commenters"]:
                if (connection, user) not in retConnections and (user, connection) not in retConnections:
                    retConnections.add((connection, user))

            for creator in data[user]["commentedOn"]:
                if (creator, user) not in retConnections and (user, creator) not in retConnections:
                    retConnections.add((creator, user))

        return retCommenters, retConnections

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

    def __colorNodeClusters(self, pyvisNet: Network) -> None:
        """
        Function colors each node cluster in the graph in a separate color
        :return: None
        """

        clusters = self.__getClusters()
        clusterColors =  [self.__getColorCombo() for i in range(len(clusters))]

        for cluster in clusters:
            colorCombo: tuple[str,str] = clusterColors.pop()
            for node in cluster:
                pyvisNet.get_node(node)["color"] = {"background": colorCombo[0], "border": colorCombo[1]}

    def __getClusters(self) -> list[list]:
        """
        Gets the separate clusters of nodes from the Graph
        :return: A list of lists of nodes representing the clusters
        """

        visitedNodes = set()
        clusters = []

        def dfs(node, cluster):
            stack = [node]
            while stack:
                currentNode = stack.pop()
                if currentNode not in visitedNodes:
                    visitedNodes.add(currentNode)
                    cluster.append(currentNode)
                    stack.extend(set(self.graph.neighbors(currentNode)) - visitedNodes)

        for node in self.graph.nodes():
            if node not in visitedNodes:
                newCluster = []
                dfs(node, newCluster)
                clusters.append(newCluster)

        return clusters

    def __getColorCombo(self) -> (str, str):
        """
        Function provides 2 node colors - first for the background and a second darker matching color for the border
        :return: Fill and Border colors in HEX format
        """

        R = random.randint(50, 200)
        G = random.randint(50, 200)
        B = random.randint(50, 200)
        backgroundColor = f"#{R:02x}{G:02x}{B:02x}"

        darkeningConstant = 0.7
        borderColor = f"#{int(R*darkeningConstant):02x}{int(G*darkeningConstant):02x}{int(B*darkeningConstant):02x}"

        return backgroundColor, borderColor


if __name__ == "__main__":
    b = BubbleGraph("../Data/Information/data.json", "../Data/Information/hashtags.json")
    # b.addHashtagsToGraph()
    # b.visualizeGraph(webFileName="hashtagGraph.html",coloringStyle="cluster")
    # b.resetGraph()

    filterInput = {
        "hashtags" : ["#racing"],
        "showAllUsers" : False,
        "users" : ["@hotehai"]
    }
    b.addCommentersToGraph(filterDict=filterInput)
    b.visualizeGraph(webFileName="commentersGraph.html",coloringStyle="cluster")