import json
import plotly.graph_objects as go
import networkx as nx
import xml.etree.ElementTree as ET
from pathlib import Path

def read_attack_files():

    datasetJSON = {}
    
    # base directory where all subdirectories are (e.g., enterprise-attack)
    baseDir = Path('C:\\ACodes\\cwe\\datasets\\Attack.json')
    target_subdirectories = ["attack-pattern", "course-of-action", "malware", "relationship"]

    # iterate through each subdirectory and load the JSON files
    #print("subdirectories:")
    for subdirectory in baseDir.iterdir() :
        #print("\t", subdirectory.name)
        if subdirectory.is_dir():  # Only process directories
           for nested_subdirectory in subdirectory.iterdir():
                if nested_subdirectory.is_dir() and nested_subdirectory.name in target_subdirectories:
                    #print(f"  Focusing on: {nested_subdirectory.name}")
                    # Get all JSON files in the nested subdirectory
                    jsonFiles = getAllJsonFiles(nested_subdirectory)
                    for i, jsonFile in enumerate(jsonFiles):
                        #if i % 500 == 0:
                            #print("\t\t",jsonFile)
                        # load the JSON file and store it in the dataset dictionary
                        datasetJSON[jsonFile.name] = loadJson(jsonFile) 
        #print('\t\t ...')

    #print("\nExamples of info gathered from json files:")
    #printSummary(datasetJSON)
    
    # convert dataset from JSON objects to string array
    return datasetJSON
        
# load and parse a JSON file
def loadJson(filePath):
    with open(filePath, 'r') as f:
        return json.load(f)
    
def save_to_json(data):
    output_file = "C:\ACodes\cwe\src\Frontend\\attack_graph_info.json"
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {output_file}")

# find all JSON files
def getAllJsonFiles(directory):
    # Recursively find all JSON files in a directory and subdirectories
    return list(directory.rglob('*.json'))

# print basic information from each file
def printSummary(data):
    counter = 5
    for fileName, content in data.items():
        # each file contains a 'bundle' with 'objects' array
        for obj in content['objects']:
            print(f"File: {fileName}")
            print(f"ID: {obj.get('id')}")
            print(f"Type: {obj.get('type')}")
            print(f"Name: {obj.get('name', 'N/A')}")
            print(f"Description: {obj.get('description', 'N/A')}")
            print("-" * 50)
            break
        if counter <0: break
        else: counter -= 1

def create_graph_from_json(TOP_5_ATTACKS):
    #print(TOP_5_ATTACKS)
    data = loadJson('C:\\ACodes\\cwe\\src\\Frontend\\attack_graph_info.json')
    # Create an empty graph
    G = nx.Graph()

    # Loop through each item in the data
    for item_name, item_data in data.items():
        
        # Extract objects from the bundle
        objects = item_data.get('objects', [])

        # Process nodes based on their type (attack-pattern, malware, course-of-action)
        for obj in objects:
            obj_id = obj.get('id')
            name = obj.get('name', 'Unknown')
            description = obj.get('description', 'No description provided')
            node_type = obj.get('type')

            if node_type in ['attack-pattern', 'malware', 'course-of-action']:
                G.add_node(obj_id, label=name, description=description, type=node_type)

            # Now, let's check for relationships (edges)
            if node_type == 'relationship':
                # Extract the source_ref and target_ref to create edges
                source = obj.get('source_ref')
                target = obj.get('target_ref')
                if source and target:
                    # Add edge between source and target nodes
                    G.add_edge(source, target)

    # Layout for plotting the graph
    pos = nx.spring_layout(G)  # positions for nodes
    # Edge traces
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    # Node traces
    node_x = []
    node_y = []
    node_labels = []
    node_colors = []
    node_sizes = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_labels.append(node + ':' +  G.nodes[node].get('label', '') )
        node_type = G.nodes[node].get('type')

        # Assign different colors based on the node type
        if str(G.nodes[node].get('label', '')) in TOP_5_ATTACKS:
            node_colors.append('purple')
            node_sizes.append(30) 
        elif node_type == 'attack-pattern':
            node_colors.append('red')
            node_sizes.append(10) 
        elif node_type == 'malware':
            node_colors.append('green')
            node_sizes.append(10) 
        elif node_type == 'course-of-action':
            node_colors.append('blue')
            node_sizes.append(10) 
        else:
            node_colors.append('gray')
            node_sizes.append(10) 

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=node_labels,
        marker=dict(
            showscale=False,
            colorscale='Viridis',
            size=node_sizes,
            color=node_colors,
            colorbar=dict(
                thickness=15,
                xanchor='left',
                titleside='right'
            )
        )
    )

    # Create the final figure with edges and nodes
    fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title="Interactive Attack Graph Visualization",
                    showlegend=False,
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
                ))

    return fig