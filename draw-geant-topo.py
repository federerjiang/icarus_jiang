import networkx as nx
import matplotlib.pyplot as plt
from os import path
import fnss

TOPOLOGY_RESOURCES_DIR = path.abspath(path.join(path.dirname(__file__),'resources', 'topologies'))

def draw_graph():
	# G = nx.random_geometric_graph(20, 0.5)
	topology = fnss.parse_topology_zoo(path.join(TOPOLOGY_RESOURCES_DIR,'Geant2012.graphml')).to_undirected()
	topology = list(nx.connected_component_subgraphs(topology))[0]


	    # pos = nx.circular_layout(G)
	labels = {}
	for v in topology.nodes():
		labels[v] = v

	G = topology
	pos = nx.pygraphviz_layout(G)
	nx.draw_networkx(G, pos=pos, labels=labels, node_color='w')
	# nx.draw_networkx_nodes(G,pos,nodelist=gateway,node_color='y',node_size=100)              
	# nx.draw_networkx_nodes(G,pos,nodelist=leafs,node_color='w',node_size=100)               
	# nx.draw_networkx_edges(G,pos, arrows=False, width=1.0)
	# nx.draw_networkx_labels(G,pos,labels,font_size=8)
	
	plt.show()


draw_graph()