import networkx as nx
import matplotlib.pyplot as plt
from cwe_parser import parse_cwe_relations,get_all_children
#from cwe_parser import build_cwe_graph  
def build_graph(parent_map, child_map):
    G = nx.DiGraph()
    for parent, children in child_map.items():
        for child in children:
            G.add_edge(parent, child)
    for parent, children in parent_map.items():
        for child in children:
            G.add_edge(child, parent)
    
    return G

def draw_cwe_graph(G,child_map, start_node=None):
    plt.figure(figsize=(18, 14))
    pos = nx.spring_layout(G, k=0.3)
    ancestor_nodes = nx.ancestors(G, start_node) if start_node in G else set()
    if start_node:
        descendants = nx.descendants(G, start_node)
        #descendants = get_all_children(start_node,child_map)
        sub_nodes = ancestor_nodes | descendants | {start_node}
        subgraph = G.subgraph(sub_nodes)
        # sub_nodes = {start_node, *descendants}
        # subgraph = G.subgraph(sub_nodes)
        # node_colors = ["red" if node == start_node else "skyblue" for node in subgraph.nodes()]
        node_colors = ["red" if node == start_node else "skyblue" if node in ancestor_nodes else "green" for node in subgraph.nodes()]
        nx.draw(subgraph, pos, with_labels=True, node_color=node_colors, node_size=500, font_size=10, edge_color='gray')
    else:
        nx.draw(G, pos, with_labels=True, node_size=400, font_size=8, edge_color='gray')

    plt.title("CWE Parent-Child Graph", fontsize=16)
    plt.tight_layout()
    plt.show()
def draw_full_graph(G):
    plt.figure(figsize=(20, 15))  # Bigger figure for readability
    pos = nx.spring_layout(G, k=0.3)  # force-directed layout
    nx.draw(G, pos, with_labels=True, node_size=500, font_size=8, node_color="lightblue", arrows=True)
    plt.title("Full CWE Parent-Child Graph", fontsize=16)
    plt.tight_layout()
    plt.show()
#G = build_cwe_graph(graph_file)
#G = build_graph(parent_map, child_map)
#draw_full_graph(G)
if __name__ == "__main__":
    xml_path = "cwec_v4.17.xml"  # Adjust this path if needed
    parent_map, child_map = parse_cwe_relations(xml_path)
    print(child_map)
    target_cwe='696'

    anc = get_all_children(target_cwe,child_map)

    G = build_graph(parent_map, child_map)

    # Optionally highlight one CWE (e.g., CWE-119)
    #target_cwe = "284"  # Change to None to draw entire graph
    #target_cwe=None
    
    draw_cwe_graph(G, child_map,start_node=target_cwe)
