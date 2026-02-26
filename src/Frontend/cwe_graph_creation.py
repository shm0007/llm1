import plotly.graph_objects as go
import networkx as nx
import xml.etree.ElementTree as ET
import os

# Function to parse the XML file and create a graph from a given file path
def parse_xml_to_graph(xml_path):
    if not os.path.isfile(xml_path):  # Check if the file exists
        return f"Error: File not found at {xml_path}"

    try:
        tree = ET.parse(xml_path)  # Load the XML from the file
        root = tree.getroot()

        # Define the namespace
        ns = {"cwe": "http://cwe.mitre.org/cwe-7"}

        G = nx.DiGraph()  # Directed graph since relationships have a direction

        # Extract nodes from <Weakness>
        for weakness in root.findall(".//cwe:Weakness", ns):
            node_id = weakness.get("ID")
            node_name = weakness.get("Name")
            G.add_node(node_id, name=node_name)

        # Extract edges from <Related_Weaknesses>
        for weakness in root.findall(".//cwe:Weakness", ns):
            source_id = weakness.get("ID")
            for related in weakness.findall(".//cwe:Related_Weakness", ns):
                target_id = related.get("CWE_ID")
                relationship = related.get("Nature")  # e.g., "ChildOf"
                G.add_edge(source_id, target_id, relationship=relationship)

        return G
    except Exception as e:
        return str(e)  # Return error message if XML parsing fails

def create_plot(G, highlight_nodes):
    # Get positions for nodes
    pos = nx.spring_layout(G)  # You can use other layouts like circular_layout or random_layout
    
    # Create edge traces (lines between nodes)
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])  # None creates breaks between edges
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode='lines',
        line=dict(width=2, color='gray'),
        hoverinfo='none'
    )
    
    # Create node traces (points representing nodes)
    node_x = []
    node_y = []
    node_text = []
    node_colors = []
    node_sizes = []
    node_labels = []
    highlight_color = 'red'  # Color for highlighted nodes
    default_color = 'blue'  # Default color for nodes
    #print(highlight_nodes)
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(str(node))
        node_labels.append(node + ':' + G.nodes[node].get('name', ''))
       
        # Check if the node is in the highlight list
        if highlight_nodes and str(node) in highlight_nodes:
            node_colors.append(highlight_color)
            node_sizes.append(30) 
        else:
            node_colors.append(default_color)
            node_sizes.append(10) 

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers',
        marker=dict(
            size=node_sizes, 
            color=node_colors, 
            line=dict(width=2, color='black')
        ),
        text=node_labels,
        textposition='top center',
        hoverinfo='text'
    )

    # Create the final figure with edges and nodes
    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        showlegend=False,
        title="Interactive CWE Graph Visualization",
        margin=dict(b=0, l=0, r=0, t=0),
                    xaxis=dict(
                        showgrid=False,
                        zeroline=False,
                        scaleanchor="y",  # Lock aspect ratio
                    ),
                    yaxis=dict(
                        showgrid=False,
                        zeroline=False,
                    ),
                    hovermode='closest',  # Enable hover
                    dragmode='pan',  # Allow panning and dragging
    )
    
    return fig
