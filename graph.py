from parse import get_dependencies
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
from jinja2 import Template

def build_graph(json_file, os):
    first_tier = ['BiocManager', 'BiocVersion', 'DESeq2', 'Rcpp', 'VennDiagram', 'WGCNA', 'apeglm', 'aws.signature', 'circlize', 'cluster', 'data.table', 'fastcluster', 'fgsea', 'ggfortify', 'ggplot2', 'jsonlite', 'limma', 'pheatmap', 'renv', 'rjson', 'tidyverse']

    data = get_dependencies(json_file)

    # Create graph
    G = nx.DiGraph()

    # adding nodes and edges
    for package, details in data.items():
        if os == "mac":
            # title contains info
            G.add_node(package, title=f"Version: {details['Version']}\nSource: {details['Source']}")
            for dependency in details.get("Requirements", []):
                if dependency in data:  # ensure dependency exists in dataset before adding edge (ignores R or system libs)
                    G.add_edge(package, dependency)
        else:
            # title contains info
            G.add_node(package, title=f"Version: {details['Version']}\nSource: {details['Source']}")
            for dependency in details.get("Depends", []):
                dependency_stripped = dependency.split(maxsplit=1)
                if dependency_stripped[0] in data:  # ensure dependency exists in dataset before adding edge (ignores R or system libs)
                    G.add_edge(package, dependency_stripped[0])
            for dependency in details.get("Imports", []):
                dependency_stripped = dependency.split(maxsplit=1)
                if dependency_stripped[0] in data:
                    G.add_edge(package, dependency_stripped[0])
            for dependency in details.get("LinkingTo", []):
                dependency_stripped = dependency.split(maxsplit=1)
                if dependency_stripped[0] in data:
                    G.add_edge(package, dependency_stripped[0])


    # create interactive graph
    net = Network(height="800px", width="100%", directed=True, notebook=False)

    # prevent jittering
    net.toggle_physics(False)

    # Convert to Pyvis
    net.from_nx(G)

    # First tier nodes different color
    for node in net.nodes:
        if node["id"] in first_tier:
            node["color"] = {"background": "orange", "border": "darkorange"} 

    # Set custom template for the HTML file, temporary workaround
    net.template = Template("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dependency Graph</title>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>
        <style>
            body {
                text-align: center;  
            }
            #mynetwork { width: 100%; height: 800px; border: 1px solid lightgray; }
            #infoBox { position: fixed; top: 10px; left: 10px; background-color: white; padding: 10px; border: 1px solid gray; display: none; z-index: 999; }
            #closeInfoBox { position: absolute; top: 5px; right: 5px; font-size: 16px; cursor: pointer; }
            #nodeVersion, #nodeSource {
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <h2>visAPPprot Dependencies macOS</h2>
        <div id="mynetwork"></div>
        <div id="infoBox">
            <span id="closeInfoBox">X</span>
            <strong>Node Info:</strong><br>
            <div id="nodeVersion">Version: </div>
            <div id="nodeSource">Source: </div>
        </div>
        <script type="text/javascript">
            var nodes = new vis.DataSet({{ nodes|tojson|safe }});
            var edges = new vis.DataSet({{ edges|tojson|safe }});
            var container = document.getElementById("mynetwork");
            var data = { nodes: nodes, edges: edges };
            var options = {
                physics: { enabled: false },  // Disable physics to prevent jittering
                interaction: { hover: true, tooltipDelay: 200 },
                nodes: {
                    color: { 
                        background: "#e0e0e0",  // Lighter background color for nodes
                        border: "#b0b0b0"  // Lighter border color for nodes
                    },
                    font: {
                        color: "#000000"  // Black color for node labels
                    }
                },
                edges: {
                    color: { 
                        color: "#c0c0c0",  // Lighter color for edges
                        highlight: "#999999",  // Highlighted edge color
                        hover: "#999999"  // Edge color when hovered
                    },
                    smooth: { enabled: false },  // Disable curve in edges, making them straight
                    arrows: {
                        to: { enabled: true, scaleFactor: 0.5 }
                    }
                }
            };
            var network = new vis.Network(container, data, options);

            // Function to display node information in a box when a node is clicked
            network.on("click", function(params) {
                var nodeId = params.nodes[0]; // Get clicked node ID
                var node = nodes.get(nodeId);
                if (node) {
                    // Display node info in the box
                    document.getElementById("nodeVersion").innerHTML = "Version: " + node.title.split("\\n")[0].split(": ")[1];
                    document.getElementById("nodeSource").innerHTML = "Source: " + node.title.split("\\n")[1].split(": ")[1];
                    document.getElementById("infoBox").style.display = "block"; // Show the info box
                }
            });

            // Close the info box on X
            document.getElementById("closeInfoBox").onclick = function() {
                document.getElementById("infoBox").style.display = "none"; // Hide the info box
            };
        </script>
    </body>
    </html>
    """)

    net.show("graph.html")
