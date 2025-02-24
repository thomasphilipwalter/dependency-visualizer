from parse import get_dependencies
import networkx as nx
import matplotlib.pyplot as plt

def build_graph(json_file):
    data = get_dependencies(json_file)

    # Create directed graph
    G = nx.DiGraph()

    # Adding nodes and edges
    for package, details in data.items():
        G.add_node(package)  # Add package nodes
        for dependency in details.get("Requirements", []):  
            if dependency in data:  # Make sure dependency exists in data set before adding edge
                G.add_edge(package, dependency)

    # Create/draw graph
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G, seed=42)  
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
    plt.title("Package Dependency Graph")
    plt.show()