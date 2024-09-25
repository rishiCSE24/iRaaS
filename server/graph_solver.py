import networkx as nx 
import requests
import json
import matplotlib.pyplot as plt

def get_weighted_topo(mon_uri:str):
    try:
        weighted_edge_list = json.loads(requests.get(mon_uri).text)
    except Exception as e:
        print(f'Error:{str(e)}')
        weighted_edge_list=None
    finally:
        return weighted_edge_list

def render_graph(mon_uri):
    # Desired size in pixels
    width_px = 1920
    height_px = 1080

    # DPI (dots per inch)
    dpi = 100

    # Convert pixels to inches
    width_in = width_px / dpi
    height_in = height_px / dpi

    # Create a figure with the specified size in inches and DPI
    plt.figure(figsize=(width_in, height_in), dpi=dpi)

    print('STATUS: Fetching Topology...',end=' ')
    weighted_edge_list=get_weighted_topo(mon_uri)
    print('Done!\n')
    
    if weighted_edge_list:
        print('STATUS: Rendedring Graph...', end=' ')

        # Create a graph
        G = nx.Graph()
        for edge in weighted_edge_list:
            G.add_edge(edge['v1'],edge['v2'],weight=edge['w'])
        
        # Define edge colors based on edge weights
        edge_colors = [G[u][v]['weight'] for u, v in G.edges()]
        
        # Draw the graph with node labels and edge colors
        pos = nx.spring_layout(G)  # Positions for all nodes
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_size=700)
        
        # Draw edges with color
        nx.draw_networkx_edges(G, pos, 
                               edgelist=G.edges(), 
                               edge_color=edge_colors, 
                               edge_cmap=plt.cm.RdYlGn, width=2)
        
        # Draw node labels
        nx.draw_networkx_labels(G, pos, font_size=10, font_color="black")

        # Draw edge labels (optional, showing weights)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        # Create a full-screen figure
        plt.savefig("topology.png", bbox_inches='tight')
        print('Done!')
        return G
    else:
        print('\nError: Topology could not be fetched!')
        return None
    
render_graph(mon_uri='http://127.0.0.1:5003/get_weighted_edges')