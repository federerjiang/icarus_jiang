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
    pos = nx.pygraphviz_layout(G)
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

node_label_runner = 0
labels= {}
graph = []
f_read_topology = open(filepath_data_set)
list_bb = []
list_gw = []
list_leaf = []
for line in f_read_topology:
  splt = line.split("\t")
  
  node1 = splt[0]
  
  if "bb" in node1:
    if node1 not in list_bb:
      list_bb.append(node1)
      labels[node1] = " "
      
  elif "gw" in node1:
    if node1 not in list_gw:
      list_gw.append(node1)
      labels[node1] = " "
      
  elif "leaf" in node1:
    if node1 not in list_leaf:
      list_leaf.append(node1)
      node_label_runner = node_label_runner + 1
      labels[node1] = node_label_runner
    
    
  node2 = splt[1]
  
  if "bb" in node2:
    if node2 not in list_bb:
      list_bb.append(node2)
      labels[node2] = " "
      
  elif "gw" in node2:
    if node2 not in list_gw:
      list_gw.append(node2)
      labels[node2] = " "
      
  elif "leaf" in node2:
    if node2 not in list_leaf:
      list_leaf.append(node2)
      node_label_runner = node_label_runner + 1
      labels[node2] = node_label_runner
  
  graph.append((node1, node2))
f_read_topology.close()

#print len(list_bb), list_bb
#print len(list_gw), list_gw
#print len(list_leaf), list_leaf
f_write = open(filepath_data_set.rstrip(".txt") + "-label.txt", 'w')

sorted_labels = sorted(labels.items(), key=operator.itemgetter(1))
for node in sorted_labels:
  if node[1] != " ":
    f_write.write(str(node[1]) + "\t" + str(node[0]) + "\n")
f_write.close()  

draw_graph(graph, list_bb, list_gw, list_leaf, labels)
  
