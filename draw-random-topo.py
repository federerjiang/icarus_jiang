import networkx as nx
import matplotlib.pyplot as plt
import os, sys, operator, random, os.path
import fnss

def draw_graph():
	# G = nx.random_geometric_graph(20, 0.5)
	topology=nx.DiGraph()
	gateway = [1]
	leafs = range(2, 7)

	for node in range(1, 7):
		topology.add_node(node)
	for leaf in leafs:
		topology.add_edge(leaf, 1)

	    # pos = nx.circular_layout(G)
	labels = {}
	labels[gateway[0]] = "Gateway"
	for v in leafs:
		labels[v] = v

	G = topology
	pos = nx.pygraphviz_layout(G)
	# nx.draw_networkx(G, pos=pos, node_color='w')
	nx.draw_networkx_nodes(G,pos,nodelist=gateway,node_color='y',node_size=100)              
	nx.draw_networkx_nodes(G,pos,nodelist=leafs,node_color='w',node_size=100)               
	nx.draw_networkx_edges(G,pos, arrows=False, width=1.0)
	nx.draw_networkx_labels(G,pos,labels,font_size=8)
	
	plt.show()


draw_graph()