import networkx as nx
import matplotlib.pyplot as plt
import os, sys, operator, random, os.path

def draw_graph():
    # extract nodes from graph
    # nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])

    # create networkx graph
    topology=nx.DiGraph()
    nodes = range(1, 26)
    labels = {}
    for v in nodes:
        labels[v] = v
    # add nodes
    for node in nodes:
        topology.add_node(node)
    
    topology.add_edge(1, 2)
    topology.add_edge(1, 3)

    topology.add_edge(2, 4)
    topology.add_edge(2, 5)
    topology.add_edge(3, 6)
    topology.add_edge(3, 7)
    
    topology.add_edge(4, 8)
    topology.add_edge(4, 9)
    topology.add_edge(4,10)
    topology.add_edge(5, 11)
    topology.add_edge(5, 12)
    topology.add_edge(5, 13)
    topology.add_edge(5, 14)
    topology.add_edge(5, 15)
    topology.add_edge(6, 16)
    topology.add_edge(6, 17)
    topology.add_edge(7, 18)
    topology.add_edge(7, 19)
    topology.add_edge(7, 20)
    topology.add_edge(7, 21)
    topology.add_edge(7, 22)
    topology.add_edge(7, 23)
    topology.add_edge(7, 24)
    topology.add_edge(7, 25)
    # add edges
    # for edge in graph:
        # G.add_edge(edge[0], edge[1])

    # degrees = {}    
    # for node in nodes:
      # degrees[node] = nx.degree(G, node)    
    # sorted_degrees = sorted(degrees.items(), key=operator.itemgetter(0))
    # print "Node with the highest degree:"
    # print sorted_degrees[0]
    
    G = topology
    # draw graph
    pos = nx.pygraphviz_layout(G, prog='dot')
    # pos = nx.circular_layout(G)
    nx.draw_networkx(G, pos=pos, labels=labels, arrows=False, node_color='w')
           
    # nx.draw_networkx_nodes(G,pos,nodelist=nodes,node_color='w',node_size=300) 
                   
    # nx.draw_networkx_edges(G,pos,width=1.0)
    
    # nx.draw_networkx_labels(G,pos,labels,font_size=8)
    # nx.draw(G, pos, labels)
    
    # show graph
    
    # nx.draw_shell(G, node_size=300)
    plt.show()


#Expected input: edge.txt
draw_graph()
