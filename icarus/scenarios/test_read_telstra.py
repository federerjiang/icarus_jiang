from os import path
import operator

import networkx as nx
import fnss


def read_telstra():
    """ Read telstra topology from telstra-link.txt

    return : all the links and nodes
    """
    # node_label_runner = 0
    # labels= {}
    filepath_data_set = "/Users/federerjiang/icarus_jiang/icarus/scenarios/telstra-link.txt"
    graph = []
    f_read_topology = open(filepath_data_set, 'r')
    # f_read_topology = open(path.join(TOPOLOGY_RESOURCES_DIR,
                                    # 'telstra-link.txt'))

    list_bb = []
    list_gw = []
    list_leaf = []
    bb_labels = {}
    gw_labels = {}
    leaf_labels = {}

    node_runner = 0
    labels = {}
    list_node = []

    for line in f_read_topology:
        splt = line.split()
  
        node1 = splt[0]
        if node1 not in list_node:
            list_node.append(node1)
            node_runner = node_runner + 1
            labels[node1] = node_runner
            if "bb" in node1:
                if labels[node1] not in list_bb:
                    list_bb.append(labels[node1])

            # labels[node1] = " "
      
            elif "gw" in node1:
                if labels[node1] not in list_gw:
                    list_gw.append(labels[node1])
                # labels[node1] = " "
      
            elif "leaf" in node1:
                if labels[node1] not in list_leaf:
                    list_leaf.append(labels[node1])
                # node_label_runner = node_label_runner + 1
                # labels[node1] = node_label_runner
    
    
        node2 = splt[1]
        if node2 not in list_node:
            list_node.append(node2)
            node_runner = node_runner + 1
            labels[node2] = node_runner
            if "bb" in node2:
                if labels[node2] not in list_bb:
                    list_bb.append(labels[node2])
                # labels[node2] = " "
      
            elif "gw" in node2:
                if labels[node2] not in list_gw:
                   list_gw.append(labels[node2])
               # labels[node2] = " "
      
            elif "leaf" in node2:
                if labels[node2] not in list_leaf:
                    list_leaf.append(labels[node2])
                # node_label_runner = node_label_runner + 1
                # labels[node2] = node_label_runner
  
        graph.append((labels[node1], labels[node2]))
    f_read_topology.close()

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
    highest = sorted_degrees[0]
    # print "Node with the highest degree:"
    # print sorted_degrees[0]
    return graph, list_leaf, list_gw, list_bb, labels, highest, list_node


graph, list_leaf, list_gw, list_bb, labels, highest, list_node = read_telstra()
print len(list_node)
print len(list_bb)
print len(list_gw)
print len(list_leaf)
count = 0
for (u, v) in graph:
    count = count + 1
print(count)


