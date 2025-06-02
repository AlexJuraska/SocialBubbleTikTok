###################################
# Simple example of a pyvis graph #
###################################

import json
from pyvis.network import Network
import networkx as nx

graph = nx.DiGraph()

with open('../Data/Information/data.json', "r", encoding="utf-8") as f:
    data = json.load(f)

user = "@sanoman2003"

nodes = { user, }
edges = set()

for other in data[user]["following"]:
    nodes.add(other)
    edges.add((user, other))

for other in data[user]["followers"]:
    nodes.add(other)
    edges.add((other, user))

graph.add_nodes_from(nodes)
graph.add_edges_from(edges)

pyvisNet = Network(notebook=True, height="780px", width="100%", directed=True)
pyvisNet.from_nx(graph)

for node in pyvisNet.nodes:
    node["label"] = ""

pyvisNet.show_buttons(filter_=["physics"])
pyvisNet.force_atlas_2based()
pyvisNet.write_html("graphs/simplePyvis.html")