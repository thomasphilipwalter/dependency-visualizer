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
        G.add_node(package, title=f"Version: {details['Version']}\nSource: {details['Source']}")
        for dependency in details.get("Requirements", []):
            if dependency in data:  # Only add an edge if the dependency exists in the dataset
                G.add_edge(package, dependency)

    # Create interactive visualization
    net = Network(height="800px", width="100%", directed=True, notebook=False)
    net.toggle_physics(False)

    # Convert NetworkX graph to Pyvis
    net.from_nx(G)

    net.template = Template("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dependency Graph</title>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>
        <style>
            #mynetwork { width: 100%; height: 800px; border: 1px solid lightgray; }
        </style>
    </head>
    <body>
        <h2>Package Dependency Graph</h2>
        <div id="mynetwork"></div>
        <script type="text/javascript">
            var nodes = new vis.DataSet({{ nodes|tojson|safe }});
            var edges = new vis.DataSet({{ edges|tojson|safe }});
            var container = document.getElementById("mynetwork");
            var data = { nodes: nodes, edges: edges };
            var options = { physics: { enabled: false }, interaction: { hover: true } };
            var network = new vis.Network(container, data, options);
        </script>
    </body>
    </html>
    """)

    # Save and open the interactive HTML file
    net.show("dependency_graph.html")
