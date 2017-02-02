import networkx as nx
import matplotlib.pyplot as plt
import os, sys, operator, random, os.path

def draw_graph(graph, list_bb, list_gw, list_leaf, labels):
    # extract nodes from graph
    nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])

    # create networkx graph
    G=nx.Graph()

    # add nodes
    for node in nodes:
        G.add_node(node)
    
    # add edges
    for edge in graph:
        G.add_edge(edge[0], edge[1])

    degrees = {}    
    for node in nodes:
      degrees[node] = nx.degree(G, node)    
    sorted_degrees = sorted(degrees.items(), key=operator.itemgetter(0))
    print "Node with the highest degree:"
    print sorted_degrees[0]
    
    # draw graph
    pos = nx.graphviz_layout(G)
    #nx.draw(G, pos)

    nx.draw_networkx_nodes(G,pos,nodelist=list_bb,node_color='r',node_size=100)              
    nx.draw_networkx_nodes(G,pos,nodelist=list_gw,node_color='y',node_size=100)               
    nx.draw_networkx_nodes(G,pos,nodelist=list_leaf,node_color='w',node_size=300) 
                   
    nx.draw_networkx_edges(G,pos,width=1.0)
    
    nx.draw_networkx_labels(G,pos,labels,font_size=8)
    
    # show graph
    
    plt.show()


#Expected input: Telstra-link.txt
argument = sys.argv
filepath_data_set = argument[1]

