import sys
import networkx as nx
import matplotlib.pyplot as plt
from parse import get_dependencies, clean_data, get_dependencies_python, clean_data_python

# Validating input
if len(sys.argv) < 5:
    print("need json file, type, OS and title")
    sys.exit()

# Parse command line
json_file = sys.argv[1]
json_type = sys.argv[2]
os = sys.argv[3]
title = sys.argv[4]
if len(sys.argv) == 6:
    sort = True
else:
    sort = False

if json_type == "R":
    # Parse data
    data_rough = get_dependencies(json_file)
    data = clean_data(data_rough, os)
else:
    data_rough = get_dependencies_python(json_file)
    data = clean_data_python(data_rough)

# Create empty graph
G = nx.DiGraph()

# Add edges
for node, neighbors in data.items():
    for neighbor in neighbors:
        G.add_edge(node, neighbor)

# first_tier = ['ggfortify']
first_tier = ['BiocManager', 'BiocVersion', 'DESeq2', 'Rcpp', 'VennDiagram', 'WGCNA', 'apeglm', 'aws.signature', 'circlize', 'cluster', 'data.table', 'fastcluster', 'fgsea', 'ggfortify', 'ggplot2', 'jsonlite', 'limma', 'pheatmap', 'renv', 'rjson', 'tidyverse']

node_colors = [
    'red' if node in first_tier else 'lightblue' for node in G.nodes()
]

# higherarchical (topological-ish) grpah
if sort:

    # higherarchical graph
    pos = nx.nx_agraph.graphviz_layout(G, prog='dot', args="-Granksep=0 -Gnodesep=0")

    plt.figure(figsize=(150, 80))
    plt.title(title, fontsize=180, fontweight='bold', color='darkblue', loc='center', pad=20)
    plt.tight_layout()
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=40000,  
        font_size=55,  
        edge_color="gray",
        alpha=0.6,
        arrows=True,
        font_weight='bold',
        font_color='black',
        width=3,
        arrowsize=30,
        node_color=node_colors
    )
    plt.savefig('random.png')
    plt.show()

else:

    # Spread out graph
    pos = nx.nx_agraph.graphviz_layout(G, prog="sfdp", args="-Goverlap=scale -Grepulsiveforce=40 -Gscale=2")

    plt.figure(figsize=(150, 80)) 
    plt.title(title, fontsize=180, fontweight='bold', color='darkblue', loc='center', pad=20)
    plt.tight_layout()
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=40000,
        font_size=55,
        edge_color="gray",
        alpha=0.6,
        arrows=True,
        font_weight='bold',  
        font_color='black', 
        width=3,
        arrowsize=30,
        node_color=node_colors   
    )
    plt.savefig('random.png')
    plt.show()