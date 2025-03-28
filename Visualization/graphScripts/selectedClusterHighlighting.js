var defaultNodeColor = '#97c2fc';
var defaultBorderColor = '#2b7ce9';
var highlightNodeColor = '#14bf3d';
var highlightBorderColor = '#0d8328';

function resetColors() {
    var nodes = network.body.nodes;
    for (var nodeId in nodes) {
        nodes[nodeId].setOptions({color: {background: defaultNodeColor, border: defaultBorderColor}});
    }
}

function colorConnectedNodes(nodeId) {
    resetColors();
    var nodes = network.body.nodes;
    var edges = network.body.edges;
    var visited = new Set();
    var queue = [nodeId];

    while (queue.length > 0) {
        var currentNode = queue.shift();
        if (!visited.has(currentNode)) {
            visited.add(currentNode);
            nodes[currentNode].setOptions({color: {background: highlightNodeColor, border: highlightBorderColor}});
            for (var edgeId in edges) {
                var edge = edges[edgeId];
                if (edge.fromId === currentNode && !visited.has(edge.toId)) {
                    queue.push(edge.toId);
                } else if (edge.toId === currentNode && !visited.has(edge.fromId)) {
                    queue.push(edge.fromId);
                }
            }
        }
    }
}

network.on("click", function(params) {
    if (params.nodes.length > 0) {
        colorConnectedNodes(params.nodes[0]);
    } else {
        resetColors();
    }
});

network.on("dragStart", function(params) {
    if (params.nodes.length > 0) {
        colorConnectedNodes(params.nodes[0]);
    } else {
        resetColors();
    }
});