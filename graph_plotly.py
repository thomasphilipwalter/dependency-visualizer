import sys
import networkx as nx
import matplotlib.pyplot as plt
from parse import get_dependencies, clean_data

# Validating input
if len(sys.argv) < 4:
    print("need json file and OS and title")
    sys.exit()

# Parse command line
json_file = sys.argv[1]
os = sys.argv[2]
title = sys.argv[3]
if len(sys.argv) == 5:
    sort = True
else:
    sort = False

# Parse data
data_rough = get_dependencies(json_file)
data = clean_data(data_rough, os)

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

    plt.figure(figsize=(220, 100))
    plt.title(title, fontsize=180, fontweight='bold', color='darkblue', loc='center', pad=20)
    plt.tight_layout()
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=30000,  
        font_size=45,  
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

    plt.figure(figsize=(220, 100)) 
    plt.title(title, fontsize=180, fontweight='bold', color='darkblue', loc='center', pad=20)
    plt.tight_layout()
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=30000,
        font_size=45,
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