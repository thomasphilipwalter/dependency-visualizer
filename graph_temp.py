from parse import get_dependencies
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
from jinja2 import Template

def build_graph(json_file):
    data = get_dependencies(json_file)

    # Create directed graph
    G = nx.DiGraph()

    # Add nodes and edges
    for package, details in data.items():
        # Set the title to contain version and source information
        G.add_node(package, title=f"Version: {details['Version']}\nSource: {details['Source']}")
        for dependency in details.get("Requirements", []):
            if dependency in data:  # Only add an edge if the dependency exists in the dataset
                G.add_edge(package, dependency)

    # Create interactive visualization
    net = Network(height="800px", width="100%", directed=True, notebook=False)

    # Toggle physics off to prevent jittering
    net.toggle_physics(False)

    # Calculate positions for nodes using NetworkX's shell layout or custom layout
    pos = nx.shell_layout(G)  # This ensures nodes without incoming edges are left and without outgoing are right

    # Convert NetworkX graph to Pyvis
    net.from_nx(G)

    # Set custom positions for the nodes based on the layout calculated
    for node in net.nodes:
        node['x'] = pos[node['id']][0]  # Set x position
        node['y'] = pos[node['id']][1]  # Set y position

    # Set custom template for the HTML file
    net.template = Template("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dependency Graph</title>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>
        <style>
            body {
                text-align: center;  /* Center the title */
            }
            #mynetwork { width: 100%; height: 800px; border: 1px solid lightgray; }
            #infoBox { position: fixed; top: 10px; left: 10px; background-color: white; padding: 10px; border: 1px solid gray; display: none; z-index: 999; }
            #closeInfoBox { position: absolute; top: 5px; right: 5px; font-size: 16px; cursor: pointer; }
            /* Bold the node title text */
            #nodeVersion, #nodeSource {
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <h2>visAPPprot Dependency Graph MacOS</h2>
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
                edges: {
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

            // Close the info box when the 'X' button is clicked
            document.getElementById("closeInfoBox").onclick = function() {
                document.getElementById("infoBox").style.display = "none"; // Hide the info box
            };
        </script>
    </body>
    </html>
    """)

    # Save and open the interactive HTML file
    net.show("dependency_graph.html")
