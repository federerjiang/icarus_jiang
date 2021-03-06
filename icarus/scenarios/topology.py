"""Functions for creating or importing topologies for experiments.

To create a custom topology, create a function returning an instance of the
`IcnTopology` class. An IcnTopology is simply a subclass of a Topology class
provided by FNSS.

A valid ICN topology must have the following attributes:
 * Each node must have one stack among: source, receiver, router
 * The topology must have an attribute called `icr_candidates` which is a set
   of router nodes on which a cache may be possibly deployed. Caches are not
   deployed directly at topology creation, instead they are deployed by a
   cache placement algorithm.
"""
from __future__ import division

from os import path
import operator
import json

import networkx as nx
import fnss

from icarus.registry import register_topology_factory


__all__ = [
        'IcnTopology',
        'topology_random',
        'topology_random2',
        'topology_random3',
        'topology_random4',
        'topology_tree',
        'topology_tree_edge',
        'topology_tree_coor_edge',
        'topology_telstra',
        'topology_telstra_edge',
        'topology_telstra_coor_edge',
        'topology_sinet',
        'topology_sinet_edge',
        'topology_asymmetric_tree',
        'topology_asymmetric_tree_edge',
        'topology_asymmetric_tree_coor_edge',
        'topology_asymmetric_tree_coor_edge_new',
        'topology_path',
        'topology_ring',
        'topology_mesh',
        'topology_geant',
        'topology_tiscali',
        'topology_wide',
        'topology_garr',
        'topology_rocketfuel_latency'
           ]


# Delays
# These values are suggested by this Computer Networks 2011 paper:
# http://www.cs.ucla.edu/classes/winter09/cs217/2011CN_NameRouting.pdf
# which is citing as source of this data, measurements from this IMC'06 paper:
# http://www.mpi-sws.org/~druschel/publications/ds2-imc.pdf
INTERNAL_LINK_DELAY = 2
EXTERNAL_LINK_DELAY = 34

# Path where all topologies are stored
TOPOLOGY_RESOURCES_DIR = path.abspath(path.join(path.dirname(__file__),
                                                path.pardir, path.pardir,
                                                'resources', 'topologies'))


class IcnTopology(fnss.Topology):
    """Class modelling an ICN topology

    An ICN topology is a simple FNSS Topology with addition methods that
    return sets of caching nodes, sources and receivers.
    """

    def cache_nodes(self):
        """Return a dictionary mapping nodes with a cache and respective cache
        size

        Returns
        -------
        cache_nodes : dict
            Dictionary mapping node identifiers and cache size
        """
        return {v: self.node[v]['stack'][1]['cache_size']
                for v in self
                if 'stack' in self.node[v]
                and 'cache_size' in self.node[v]['stack'][1]
                }

    def sources(self):
        """Return a set of source nodes

        Returns
        -------
        sources : set
            Set of source nodes
        """
        return set(v for v in self
                   if 'stack' in self.node[v]
                   and self.node[v]['stack'][0] == 'source')

    def receivers(self):
        """Return a set of receiver nodes

        Returns
        -------
        receivers : set
            Set of receiver nodes
        """
        return set(v for v in self
                   if 'stack' in self.node[v]
                   and self.node[v]['stack'][0] == 'receiver')

@register_topology_factory('TREE')
def topology_tree(k, h, delay=1, **kwargs):
    """Returns a tree topology, with a source at the root, receivers at the
    leafs and caches at all intermediate nodes.

    Parameters
    ----------
    h : int
        The height of the tree
    k : int
        The branching factor of the tree
    delay : float
        The link delay in milliseconds

    Returns
    -------
    topology : IcnTopology
        The topology object
    """
    topology = fnss.k_ary_tree_topology(k, h)

    leafs = [v for v in topology.nodes_iter()
             if topology.node[v]['depth'] == h]
    sources = [v for v in topology.nodes_iter()
               if topology.node[v]['depth'] == 0]
    routers = [v for v in topology.nodes_iter()
              if topology.node[v]['depth'] > 0
              and topology.node[v]['depth'] <= h]
              
    total_node = k ** (h+1) - 1
    for v in range(0, len(leafs)):
        topology.add_node(total_node + v, type="requester")
        topology.add_edge(total_node + v, leafs[v])

    receivers = [v for v in topology.nodes_iter() 
                if topology.node[v]['type'] == "requester"]

    topology.graph['icr_candidates'] = set(routers)
    for v in sources:
        fnss.add_stack(topology, v, 'source')
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver')
    for v in routers:
        fnss.add_stack(topology, v, 'router')
    # set weights and delays on all links
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_constant(topology, delay, 'ms')
    # label links as internal
    for u, v in topology.edges_iter():
        topology.edge[u][v]['type'] = 'internal'
    return IcnTopology(topology)



@register_topology_factory('TREE-EDGE')
def topology_tree_edge(k, h, delay=1, **kwargs):
    """Returns a tree topology, with a source at the root, caches at only leaf nodes,
    and receivers connect to only leaf nodes.


    Cooresponding strategy : MEDGE


    Parameters
    ----------
    h : int
        The height of the tree
    k : int
        The branching factor of the tree
    delay : float
        The link delay in milliseconds

    Returns
    -------
    topology : IcnTopology
        The topology object
    """
    topology = IcnTopology()
    sources = [0]
    routers = range(1, k+1)
    receivers = range(101, 101+k)
    gateways = range(1000, 998+6)

    # topology.add_path([1,2,3,4,5,6,7,8])
    for v in routers:
        topology.add_node(v)
    for v in sources:
        topology.add_node(v)
    for v in receivers:
        topology.add_node(v)
    for v in gateways:
        topology.add_node(v)

    topology.add_edge(0,1000)
    topology.add_edge(1000, 1001)
    topology.add_edge(1001, 1002)
    topology.add_edge(1002, 1003)
    for v in routers:
        topology.add_edge(1003, v)              
    for v in receivers:
        topology.add_edge(v-100, v)


    topology.graph['icr_candidates'] = set(routers)
    for v in sources:
        fnss.add_stack(topology, v, 'source')
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver')
    for v in routers:
        fnss.add_stack(topology, v, 'router')
    for v in gateways:
        fnss.add_stack(topology, v, 'gateway')
    # set weights and delays on all links
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_constant(topology, delay, 'ms')
    return IcnTopology(topology)



@register_topology_factory('TREE-COOR-EDGE')
def topology_tree_coor_edge(k, h, delay=1, **kwargs):
    """Returns a tree topology, with a source at the root, receivers at the
    leafs and caches at all intermediate nodes.

    Cooresponding strategy : CTEDGE

    Parameters
    ----------
    h : int
        The height of the tree
    k : int
        The branching factor of the tree
    delay : float
        The link delay in milliseconds

    Returns
    -------
    topology : IcnTopology
        The topology object
    """
    topology = fnss.k_ary_tree_topology(k, h)

    leafs = [v for v in topology.nodes_iter()
             if topology.node[v]['depth'] == h]
    sources = [v for v in topology.nodes_iter()
               if topology.node[v]['depth'] == 0]
    routers = [v for v in topology.nodes_iter()
              if topology.node[v]['depth'] >= h-1
              and topology.node[v]['depth'] <= h]
    gateways = [v for v in topology.nodes_iter()
                if topology.node[v]['depth'] > 0
                and topology.node[v]['depth'] < h-1]
              
    total_node = k ** (h+1) - 1
    for v in range(0, len(leafs)):
        topology.add_node(total_node + v, type="requester")
        topology.add_edge(total_node + v, leafs[v])

    receivers = [v for v in topology.nodes_iter() 
                if topology.node[v]['type'] == "requester"]

    topology.graph['icr_candidates'] = set(routers)
    for v in sources:
        fnss.add_stack(topology, v, 'source')
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver')
    for v in routers:
        fnss.add_stack(topology, v, 'router')
    for v in gateways:
        fnss.add_stack(topology, v, 'gateway')
    # set weights and delays on all links
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_constant(topology, delay, 'ms')
    # label links as internal
    for u, v in topology.edges_iter():
        topology.edge[u][v]['type'] = 'internal'
    return IcnTopology(topology)



'''
def read_telstra():
    """ Read telstra topology from telstra-link.txt

    return : all the links and nodes
    """
    # node_label_runner = 0
    # labels= {}
    # filepath_data_set = "/Users/federerjiang/icarus_jiang/icarus/scenarios/telstra-link.txt"
    graph = []
    # f_read_topology = open(filepath_data_set, 'r')
    f_read_topology = open(path.join(TOPOLOGY_RESOURCES_DIR,
                                    'telstra-link.txt'))

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
    return graph, list_leaf, list_gw, list_bb, highest
'''


# def read_random():
#     """ Read telstra topology from random_1.json

#     return : all the links and nodes
#     """
#     # f_read_topology = open(path.join(TOPOLOGY_RESOURCES_DIR,
#                                     # 'random_1.json'))
#     with open(path.join(TOPOLOGY_RESOURCES_DIR, "random_1.json")) as data_file:
#         data = json.load(data_file)

#     graph = []
#     nodes = []
#     connections = data["connections"]
#     for item in connections:
#         des = item["destination_id"]
#         src = item["source_id"]
#         graph.append((des, src))
#         if des not in nodes:
#             nodes.append(des)
#         if src not in nodes:
#             nodes.append(src)
#     deg = {}
#     for node in nodes:
#         deg[node] = 0
#     for edge in graph:
#         deg[edge[0]] = deg[edge[0]] + 1
#         deg[edge[1]] = deg[edge[1]] + 1
#     for node in nodes:
#         if deg[node] == 7:
#             highest = node
#             break

#     return graph, nodes, highest


# @register_topology_factory('RANDOM')
# def topology_random(delay=1, **kwargs):
#     """Returns a telstra topology, with source to the core nodes, receivers connected to all
#     the leaf nodes in the network.


#     Returns
#     -------
#     topology : IcnTopology
#         The topology object
#     """
#     graph, nodes, highest = read_random()
#     # nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])

#     topology = IcnTopology()
#     for node in nodes:
#         topology.add_node(node)
#     for edge in graph:
#         topology.add_edge(edge[0], edge[1])

#     # sources = [0]
#     routers = nodes
#     receivers = range(1000, 1000+len(nodes))
#     sources = range(10000, 10000+len(nodes))

              
#     for v in receivers:
#         topology.add_node(v)
#         topology.add_edge(routers[v-1000], v)
#     for v in sources:
#         topology.add_node(v)
#         topology.add_edge(routers[v-10000], v)


#     topology.graph['icr_candidates'] = set(routers)
#     for v in sources:
#         fnss.add_stack(topology, v, 'source')
#     for v in receivers:
#         fnss.add_stack(topology, v, 'receiver')
#     for v in routers:
#         fnss.add_stack(topology, v, 'router')
#     # set weights and delays on all links
#     fnss.set_weights_constant(topology, 1.0)
#     fnss.set_delays_constant(topology, delay, 'ms')
#     # label links as internal
#     for u, v in topology.edges_iter():
#         topology.edge[u][v]['type'] = 'internal'
#     return IcnTopology(topology)

def read_random():
    """ Read telstra topology from random_1.json

    return : all the links and nodes
    """
    # f_read_topology = open(path.join(TOPOLOGY_RESOURCES_DIR,
                                    # 'random_1.json'))
    with open(path.join(TOPOLOGY_RESOURCES_DIR, "random_1.json")) as data_file:
        data = json.load(data_file)

    graph = []
    nodes = []
    connections = data["connections"]
    for item in connections:
        des = item["destination_id"]
        src = item["source_id"]
        graph.append((des, src))
        if des not in nodes:
            nodes.append(des)
        if src not in nodes:
            nodes.append(src)
    deg = {}
    for node in nodes:
        deg[node] = 0
    for edge in graph:
        deg[edge[0]] = deg[edge[0]] + 1
        deg[edge[1]] = deg[edge[1]] + 1
    for node in nodes:
        if deg[node] == 20:
            highest = node
            break

    return graph, nodes, highest


@register_topology_factory('RANDOM')
def topology_random(delay=1, **kwargs):
    """Returns a telstra topology, with source to the core nodes, receivers connected to all
    the leaf nodes in the network.


    Returns
    -------
    topology : IcnTopology
        The topology object
    """
    graph, nodes, highest = read_random()
    # nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])

    topology = IcnTopology()
    for node in nodes:
        topology.add_node(node)
    for edge in graph:
        topology.add_edge(edge[0], edge[1])

    # sources = [0]
    routers = nodes
    receivers = range(1000, 1000+len(nodes))
    # sources = range(10000, 10000+len(nodes))
    sources = [10000,]
    server = 10000

              
    for v in receivers:
        topology.add_node(v)
        topology.add_edge(routers[v-1000], v)
    # for v in sources:
    #     topology.add_node(v)
    #     topology.add_edge(routers[v-10000], v)
    topology.add_node(server)
    topology.add_edge(highest, server)


    topology.graph['icr_candidates'] = set(routers)
    for v in sources:
        fnss.add_stack(topology, v, 'source')
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver')
    for v in routers:
        fnss.add_stack(topology, v, 'router')
    # set weights and delays on all links
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_constant(topology, delay, 'ms')
    # label links as internal
    for u, v in topology.edges_iter():
        topology.edge[u][v]['type'] = 'internal'
    return IcnTopology(topology)

def read_random2():
    """ Read telstra topology from random_1.json

    return : all the links and nodes
    """
    # f_read_topology = open(path.join(TOPOLOGY_RESOURCES_DIR,
                                    # 'random_1.json'))
    with open(path.join(TOPOLOGY_RESOURCES_DIR, "random_1.json")) as data_file:
        data = json.load(data_file)

    graph = []
    nodes = []
    connections = data["connections"]
    for item in connections:
        des = item["destination_id"]
        src = item["source_id"]
        graph.append((des, src))
        if des not in nodes:
            nodes.append(des)
        if src not in nodes:
            nodes.append(src)
    deg = {}
    for node in nodes:
        deg[node] = 0
    for edge in graph:
        deg[edge[0]] = deg[edge[0]] + 1
        deg[edge[1]] = deg[edge[1]] + 1
    for node in nodes:
        if deg[node] == 20:
            highest = node
            break

    return graph, nodes, highest


@register_topology_factory('RANDOM2')
def topology_random2(delay=1, **kwargs):
    """Returns a telstra topology, with source to the core nodes, receivers connected to all
    the leaf nodes in the network.


    Returns
    -------
    topology : IcnTopology
        The topology object
    """
    graph, nodes, highest = read_random2()
    # nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])

    topology = IcnTopology()
    for node in nodes:
        topology.add_node(node)
    for edge in graph:
        topology.add_edge(edge[0], edge[1])

    # sources = [0]
    routers = nodes
    receivers = range(1000, 1000+len(nodes))
    # sources = range(10000, 10000+len(nodes))
    # sources = []
    # sources.append(highest)

              
    for v in receivers:
        topology.add_node(v)
        topology.add_edge(routers[v-1000], v)

    # for v in sources:
        # topology.add_node(v)
        # topology.add_edge(routers[v-10000], v)


    topology.graph['icr_candidates'] = set(routers)
    for v in sources:
        fnss.add_stack(topology, v, 'source')
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver')
    for v in routers:
        fnss.add_stack(topology, v, 'router')
    # set weights and delays on all links
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_constant(topology, delay, 'ms')
    # label links as internal
    for u, v in topology.edges_iter():
        topology.edge[u][v]['type'] = 'internal'
    return IcnTopology(topology)

def read_random3():
    """ Read telstra topology from random_1.json

    return : all the links and nodes
    """
    # f_read_topology = open(path.join(TOPOLOGY_RESOURCES_DIR,
                                    # 'random_1.json'))
    with open(path.join(TOPOLOGY_RESOURCES_DIR, "random_750.json")) as data_file:
        data = json.load(data_file)

    graph = []
    nodes = []
    connections = data["connections"]
    for item in connections:
        des = item["destination_id"]
        src = item["source_id"]
        graph.append((des, src))
        if des not in nodes:
            nodes.append(des)
        if src not in nodes:
            nodes.append(src)
    deg = {}
    for node in nodes:
        deg[node] = 0
    for edge in graph:
        deg[edge[0]] = deg[edge[0]] + 1
        deg[edge[1]] = deg[edge[1]] + 1
    for node in nodes:
        if deg[node] == 7:
            highest = node
            break

    return graph, nodes, highest


@register_topology_factory('RANDOM3')
def topology_random3(delay=1, **kwargs):
    """Returns a telstra topology, with source to the core nodes, receivers connected to all
    the leaf nodes in the network.


    Returns
    -------
    topology : IcnTopology
        The topology object
    """
    graph, nodes, highest = read_random3()
    # nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])

    topology = IcnTopology()
    for node in nodes:
        topology.add_node(node)
    for edge in graph:
        topology.add_edge(edge[0], edge[1])

    # sources = [0]
    routers = nodes
    receivers = range(1000, 1000+len(nodes))
    sources = range(10000, 10000+len(nodes))

              
    for v in receivers:
        topology.add_node(v)
        topology.add_edge(routers[v-1000], v)
    for v in sources:
        topology.add_node(v)
        topology.add_edge(routers[v-10000], v)


    topology.graph['icr_candidates'] = set(routers)
    for v in sources:
        fnss.add_stack(topology, v, 'source')
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver')
    for v in routers:
        fnss.add_stack(topology, v, 'router')
    # set weights and delays on all links
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_constant(topology, delay, 'ms')
    # label links as internal
    for u, v in topology.edges_iter():
        topology.edge[u][v]['type'] = 'internal'
    return IcnTopology(topology)

def read_random4():
    """ Read telstra topology from random_1.json

    return : all the links and nodes
    """
    # f_read_topology = open(path.join(TOPOLOGY_RESOURCES_DIR,
                                    # 'random_1.json'))
    with open(path.join(TOPOLOGY_RESOURCES_DIR, "random_1000.json")) as data_file:
        data = json.load(data_file)

    graph = []
    nodes = []
    connections = data["connections"]
    for item in connections:
        des = item["destination_id"]
        src = item["source_id"]
        graph.append((des, src))
        if des not in nodes:
            nodes.append(des)
        if src not in nodes:
            nodes.append(src)
    deg = {}
    for node in nodes:
        deg[node] = 0
    for edge in graph:
        deg[edge[0]] = deg[edge[0]] + 1
        deg[edge[1]] = deg[edge[1]] + 1
    for node in nodes:
        if deg[node] == 7:
            highest = node
            break

    return graph, nodes, highest


@register_topology_factory('RANDOM4')
def topology_random4(delay=1, **kwargs):
    """Returns a telstra topology, with source to the core nodes, receivers connected to all
    the leaf nodes in the network.


    Returns
    -------
    topology : IcnTopology
        The topology object
    """
    graph, nodes, highest = read_random4()
    # nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])

    topology = IcnTopology()
    for node in nodes:
        topology.add_node(node)
    for edge in graph:
        topology.add_edge(edge[0], edge[1])

    # sources = [0]
    routers = nodes
    receivers = range(1000, 1000+len(nodes))
    sources = range(10000, 10000+len(nodes))

              
    for v in receivers:
        topology.add_node(v)
        topology.add_edge(routers[v-1000], v)
    for v in sources:
        topology.add_node(v)
        topology.add_edge(routers[v-10000], v)


    topology.graph['icr_candidates'] = set(routers)
    for v in sources:
        fnss.add_stack(topology, v, 'source')
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver')
    for v in routers:
        fnss.add_stack(topology, v, 'router')
    # set weights and delays on all links
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_constant(topology, delay, 'ms')
    # label links as internal
    for u, v in topology.edges_iter():
        topology.edge[u][v]['type'] = 'internal'
    return IcnTopology(topology)


def read_telstra():
    """ Read telstra topology from telstra-link.txt

    return : all the links and nodes
    """
    f_read_topology = open(path.join(TOPOLOGY_RESOURCES_DIR,
                                    'telstra-link.txt'))
    node_label_runner = 0
    labels= {}
    graph = []
    # f_read_topology = open(filepath_data_set)
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

    highest = 'bb-1784'
    return graph, list_leaf, list_gw, list_bb, highest


@register_topology_factory('TELSTRA')
def topology_telstra(delay=1, **kwargs):
    """Returns a telstra topology, with source to the core nodes, receivers connected to all
    the leaf nodes in the network.


    Returns
    -------
    topology : IcnTopology
        The topology object
    """
    graph, list_leaf, list_gw, list_bb, highest = read_telstra()
    nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])

    topology = IcnTopology()
    for node in nodes:
        topology.add_node(node)
    for edge in graph:
        topology.add_edge(edge[0], edge[1])

    sources = [0]
    routers = list_leaf + list_gw + list_bb
    receivers = range(1000, 1000+len(list_leaf))

              
    for v in receivers:
        topology.add_node(v)
        topology.add_edge(list_leaf[v-1000], v)
    for v in sources:
        topology.add_node(v)
        topology.add_edge(v, highest)


    topology.graph['icr_candidates'] = set(routers)
    for v in sources:
        fnss.add_stack(topology, v, 'source')
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver')
    for v in routers:
        fnss.add_stack(topology, v, 'router')
    # set weights and delays on all links
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_constant(topology, delay, 'ms')
    # label links as internal
    for u, v in topology.edges_iter():
        topology.edge[u][v]['type'] = 'internal'
    return IcnTopology(topology)


@register_topology_factory('TELSTRA-EDGE')
def topology_telstra_edge(delay=1, **kwargs):
    """Returns a telstra topology, with source to the core nodes, receivers connected to all
    the leaf nodes in the network.


    Returns
    -------
    topology : IcnTopology
        The topology object
    """
    graph, list_leaf, list_gw, list_bb, highest = read_telstra()
    nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])

    topology = IcnTopology()
    for node in nodes:
        topology.add_node(node)
    for edge in graph:
        topology.add_edge(edge[0], edge[1])

    sources = [0]
    routers = list_leaf
    receivers = range(1000, 1000+len(list_leaf))
    gateways = list_gw + list_bb

              
    for v in receivers:
        topology.add_node(v)
        topology.add_edge(list_leaf[v-1000], v)
    for v in sources:
        topology.add_node(v)
        topology.add_edge(v, highest)


    topology.graph['icr_candidates'] = set(routers)
    for v in sources:
        fnss.add_stack(topology, v, 'source')
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver')
    for v in routers:
        fnss.add_stack(topology, v, 'router')
    for v in gateways:
        fnss.add_stack(topology, v, 'gateway')
    # set weights and delays on all links
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_constant(topology, delay, 'ms')
    # label links as internal
    for u, v in topology.edges_iter():
        topology.edge[u][v]['type'] = 'internal'
    return IcnTopology(topology)


@register_topology_factory('TELSTRA-COOR-EDGE')
def topology_telstra_coor_edge(delay=1, **kwargs):
    """Returns a telstra topology, with source to the core nodes, receivers connected to all
    the leaf nodes in the network.


    Returns
    -------
    topology : IcnTopology
        The topology object
    """
    graph, list_leaf, list_gw, list_bb, highest = read_telstra()
    nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])

    topology = IcnTopology()
    for node in nodes:
        topology.add_node(node)
    for edge in graph:
        topology.add_edge(edge[0], edge[1])

    sources = [0]
    routers = list_leaf + list_gw
    receivers = range(1000, 1000+len(list_leaf))
    gateways = list_bb

              
    for v in receivers:
        topology.add_node(v)
        topology.add_edge(list_leaf[v-1000], v)
    for v in sources:
        topology.add_node(v)
        topology.add_edge(v, highest)


    topology.graph['icr_candidates'] = set(routers)
    for v in sources:
        fnss.add_stack(topology, v, 'source')
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver')
    for v in routers:
        fnss.add_stack(topology, v, 'router')
    for v in gateways:
        fnss.add_stack(topology, v, 'gateway')
    # set weights and delays on all links
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_constant(topology, delay, 'ms')
    # label links as internal
    for u, v in topology.edges_iter():
        topology.edge[u][v]['type'] = 'internal'
    return IcnTopology(topology)


@register_topology_factory('SINET')
def topology_sinet(delay=1, **kwargs):
    """Returns a sinet topology, with a source at the node "server", receivers connected to all
    the nodes in the network.


    Cooresponding strategy : CMEDGE


    Returns
    -------
    topology : IcnTopology
        The topology object
    """
    topology = IcnTopology()
    sources = [0]
    routers = range(1, 51)
    receivers = range(101, 151)

    topology.add_path([1,2,3,4,5,6,7,8])
    topology.add_edge(8,1)
    topology.add_edge(1,7)
    topology.add_edge(1,4)
    topology.add_edge(1,3)
    topology.add_edge(4,7)
    topology.add_edge(5,7)

    topology.add_node(0)
    topology.add_edge(0,1)

    for v in range(9,51):
        topology.add_node(v)
    for u in range(9,20):
        topology.add_edge(u, 1)
    for u in range(20, 21):
        topology.add_edge(u, 2)
    for u in range(21, 26):
        topology.add_edge(u, 3)
    for u in range(26, 28):
        topology.add_edge(u, 4)
    for u in range(28, 32):
        topology.add_edge(u, 5)
    for u in range(32, 40):
        topology.add_edge(u, 6)
    for u in range(40,49):
        topology.add_edge(u, 7)
    for u in range(49, 51):
        topology.add_edge(u, 8)
              
    for v in receivers:
        topology.add_node(v)
        topology.add_edge(int(v-100), v)


    topology.graph['icr_candidates'] = set(routers)
    for v in sources:
        fnss.add_stack(topology, v, 'source')
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver')
    for v in routers:
        fnss.add_stack(topology, v, 'router')
    # set weights and delays on all links
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_constant(topology, delay, 'ms')
    # label links as internal
    for u, v in topology.edges_iter():
        topology.edge[u][v]['type'] = 'internal'
    return IcnTopology(topology)


@register_topology_factory('SINET-EDGE')
def topology_sinet_edge(delay=1, **kwargs):
    """Returns a sinet topology, with a source at the node "server", receivers connected to all
    the nodes in the network.


    Cooresponding strategy : CTEDGE/...


    Returns
    -------
    topology : IcnTopology
        The topology object
    """
    topology = IcnTopology()
    sources = [0]
    routers = range(1, 51)
    receivers = range(109, 151)

    topology.add_path([1,2,3,4,5,6,7,8])
    topology.add_edge(8,1)
    topology.add_edge(1,7)
    topology.add_edge(1,4)
    topology.add_edge(1,3)
    topology.add_edge(4,7)
    topology.add_edge(5,7)

    topology.add_node(0)
    topology.add_edge(0,1)

    for v in range(9,51):
        topology.add_node(v)
    for u in range(9,20):
        topology.add_edge(u, 1)
    for u in range(20, 21):
        topology.add_edge(u, 2)
    for u in range(21, 26):
        topology.add_edge(u, 3)
    for u in range(26, 28):
        topology.add_edge(u, 4)
    for u in range(28, 32):
        topology.add_edge(u, 5)
    for u in range(32, 40):
        topology.add_edge(u, 6)
    for u in range(40,49):
        topology.add_edge(u, 7)
    for u in range(49, 51):
        topology.add_edge(u, 8)
              
    for v in receivers:
        topology.add_node(v)
        topology.add_edge(int(v-100), v)


    topology.graph['icr_candidates'] = set(routers)
    for v in sources:
        fnss.add_stack(topology, v, 'source')
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver')
    for v in routers:
        fnss.add_stack(topology, v, 'router')
    # set weights and delays on all links
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_constant(topology, delay, 'ms')
    # label links as internal
    for u, v in topology.edges_iter():
        topology.edge[u][v]['type'] = 'internal'
    return IcnTopology(topology)



@register_topology_factory('ATREE')
def topology_asymmetric_tree(delay=1, **kwargs):
    """Returns a sinet topology, with a source at the node "server", receivers connected to all
    the nodes in the network.


    Cooresponding strategy : CMEDGE


    Returns
    -------
    topology : IcnTopology
        The topology object
    """
    topology = IcnTopology()
    sources = [0]
    routers = range(1, 26)
    receivers = range(108, 126)

    # topology.add_path([1,2,3,4,5,6,7,8])
    for v in routers:
        topology.add_node(v)
    for v in sources:
        topology.add_node(v)
    for v in receivers:
        topology.add_node(v)

    topology.add_edge(0,1)

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
    # topology.add_edge(7, 26)

              
    for v in receivers:
        topology.add_edge(v-100, v)


    topology.graph['icr_candidates'] = set(routers)
    for v in sources:
        fnss.add_stack(topology, v, 'source')
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver')
    for v in routers:
        fnss.add_stack(topology, v, 'router')
    # set weights and delays on all links
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_constant(topology, delay, 'ms')
    return IcnTopology(topology)


@register_topology_factory('EATREE')
def topology_asymmetric_tree_edge(delay=1, **kwargs):
    """Returns a sinet topology, with a source at the node "server", receivers connected to all
    the nodes in the network.


    Cooresponding strategy : CMEDGE


    Returns
    -------
    topology : IcnTopology
        The topology object
    """
    topology = IcnTopology()
    sources = [0]
    gateways = range(1, 8)
    routers = range(8, 26)
    receivers = range(108, 126)

    # topology.add_path([1,2,3,4,5,6,7,8])
    for v in routers:
        topology.add_node(v)
    for v in sources:
        topology.add_node(v)
    for v in receivers:
        topology.add_node(v)
    for v in gateways:
        topology.add_node(v)

    topology.add_edge(0,1)

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

              
    for v in receivers:
        topology.add_edge(v-100, v)


    topology.graph['icr_candidates'] = set(routers)
    for v in sources:
        fnss.add_stack(topology, v, 'source')
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver')
    for v in routers:
        fnss.add_stack(topology, v, 'router')
    for v in gateways:
        fnss.add_stack(topology, v, 'gateway')
    # set weights and delays on all links
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_constant(topology, delay, 'ms')
    return IcnTopology(topology)


@register_topology_factory('CEATREE')
def topology_asymmetric_tree_coor_edge(delay=1, **kwargs):
    """Returns a sinet topology, with a source at the node "server", receivers connected to all
    the nodes in the network.


    Cooresponding strategy : CMEDGE


    Returns
    -------
    topology : IcnTopology
        The topology object
    """
    topology = IcnTopology()
    sources = [0]
    gateways = range(1, 4)
    routers = range(4, 26)
    receivers = range(108, 126)

    # topology.add_path([1,2,3,4,5,6,7,8])
    for v in routers:
        topology.add_node(v)
    for v in sources:
        topology.add_node(v)
    for v in receivers:
        topology.add_node(v)
    for v in gateways:
        topology.add_node(v)

    topology.add_edge(0,1)

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


              
    for v in receivers:
        topology.add_edge(v-100, v)


    topology.graph['icr_candidates'] = set(routers)
    for v in sources:
        fnss.add_stack(topology, v, 'source')
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver')
    for v in routers:
        fnss.add_stack(topology, v, 'router')
    for v in gateways:
        fnss.add_stack(topology, v, 'gateway')
    # set weights and delays on all links
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_constant(topology, delay, 'ms')
    return IcnTopology(topology)


@register_topology_factory('NCEATREE')
def topology_asymmetric_tree_coor_edge_new(delay=1, **kwargs):
    """Returns a sinet topology, with a source at the node "server", receivers connected to all
    the nodes in the network.


    Cooresponding strategy : CMEDGE


    Returns
    -------
    topology : IcnTopology
        The topology object
    """
    topology = IcnTopology()
    sources = [1]
    gateways = range(2, 4)
    routers = range(4, 26)
    receivers = range(108, 126)

    # topology.add_path([1,2,3,4,5,6,7,8])
    for v in routers:
        topology.add_node(v)
    for v in sources:
        topology.add_node(v)
    for v in receivers:
        topology.add_node(v)
    for v in gateways:
        topology.add_node(v)

    # topology.add_edge(0,1)

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


              
    for v in receivers:
        topology.add_edge(v-100, v)


    topology.graph['icr_candidates'] = set(routers)
    for v in sources:
        fnss.add_stack(topology, v, 'source')
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver')
    for v in routers:
        fnss.add_stack(topology, v, 'router')
    for v in gateways:
        fnss.add_stack(topology, v, 'gateway')
    # set weights and delays on all links
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_constant(topology, delay, 'ms')
    return IcnTopology(topology)


@register_topology_factory('PATH')
def topology_path(n, delay=1, **kwargs):
    """Return a path topology with a receiver on node `0` and a source at node
    'n-1'

    Parameters
    ----------
    n : int (>=3)
        The number of nodes
    delay : float
        The link delay in milliseconds

    Returns
    -------
    topology : IcnTopology
        The topology object
    """
    topology = fnss.line_topology(n)
    receivers = [0]
    routers = range(1, n - 1)
    sources = [n - 1]
    topology.graph['icr_candidates'] = set(routers)
    for v in sources:
        fnss.add_stack(topology, v, 'source')
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver')
    for v in routers:
        fnss.add_stack(topology, v, 'router')
    # set weights and delays on all links
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_constant(topology, delay, 'ms')
    # label links as internal or external
    for u, v in topology.edges_iter():
        topology.edge[u][v]['type'] = 'internal'
    return IcnTopology(topology)


@register_topology_factory('RING')
def topology_ring(n, delay_int=1, delay_ext=5, **kwargs):
    """Returns a ring topology

    This topology is comprised of a ring of *n* nodes. Each of these nodes is
    attached to a receiver. In addition one router is attached to a source.
    Therefore, this topology has in fact 2n + 1 nodes.

    It models the case of a metro ring network, with many receivers and one
    only source towards the core network.

    Parameters
    ----------
    n : int
        The number of routers in the ring
    delay_int : float
        The internal link delay in milliseconds
    delay_ext : float
        The external link delay in milliseconds

    Returns
    -------
    topology : IcnTopology
        The topology object
    """
    topology = fnss.ring_topology(n)
    routers = range(n)
    receivers = range(n, 2 * n)
    source = 2 * n
    internal_links = zip(routers, receivers)
    external_links = [(routers[0], source)]
    for u, v in internal_links:
        topology.add_edge(u, v, type='internal')
    for u, v in external_links:
        topology.add_edge(u, v, type='external')
    topology.graph['icr_candidates'] = set(routers)
    fnss.add_stack(topology, source, 'source')
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver')
    for v in routers:
        fnss.add_stack(topology, v, 'router')
    # set weights and delays on all links
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_constant(topology, delay_int, 'ms', internal_links)
    fnss.set_delays_constant(topology, delay_ext, 'ms', external_links)
    return IcnTopology(topology)


@register_topology_factory('MESH')
def topology_mesh(n, m, delay_int=1, delay_ext=5, **kwargs):
    """Returns a ring topology

    This topology is comprised of a mesh of *n* nodes. Each of these nodes is
    attached to a receiver. In addition *m* router are attached each to a source.
    Therefore, this topology has in fact 2n + m nodes.

    Parameters
    ----------
    n : int
        The number of routers in the ring
    m : int
        The number of sources
    delay_int : float
        The internal link delay in milliseconds
    delay_ext : float
        The external link delay in milliseconds

    Returns
    -------
    topology : IcnTopology
        The topology object
    """
    if m > n:
        raise ValueError("m cannot be greater than n")
    topology = fnss.full_mesh_topology(n)
    routers = range(n)
    receivers = range(n, 2 * n)
    sources = range(2 * n, 2 * n + m)
    internal_links = zip(routers, receivers)
    external_links = zip(routers[:m], sources)
    for u, v in internal_links:
        topology.add_edge(u, v, type='internal')
    for u, v in external_links:
        topology.add_edge(u, v, type='external')
    topology.graph['icr_candidates'] = set(routers)
    for v in sources:
        fnss.add_stack(topology, v, 'source')
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver')
    for v in routers:
        fnss.add_stack(topology, v, 'router')
    # set weights and delays on all links
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_constant(topology, delay_int, 'ms', internal_links)
    fnss.set_delays_constant(topology, delay_ext, 'ms', external_links)
    return IcnTopology(topology)


def highest(topology, deg):
    high_deg = 0
    high_node = None
    for v in topology.nodes():
        if deg[v] > high_deg:
            high_deg = deg[v]
            high_node = v
    return [high_node]

@register_topology_factory('GEANT')
def topology_geant(delay=1, **kwargs):
    """Return a scenario based on GEANT topology

    Parameters
    ----------
    seed : int, optional
        The seed used for random number generation

    Returns
    -------
    topology : fnss.Topology
        The topology object
    """
    # 240 nodes in the main component
    topology = fnss.parse_topology_zoo(path.join(TOPOLOGY_RESOURCES_DIR,
                                                 'Geant2012.graphml')
                                       ).to_undirected()
    topology = list(nx.connected_component_subgraphs(topology))[0]

    leafs = topology.nodes()  
    print ("FEANT : %d, %d", len(leafs), len(topology.edges()))
    deg = nx.degree(topology)
    source_attachments = highest(topology, deg) 

    sources = []
    for v in source_attachments:
        u = v + 1000  # node ID of source
        topology.add_edge(v, u)
        sources.append(u)
    receivers = []
    for v in leafs:
        u = v + 2000
        topology.add_edge(v, u)
        receivers.append(u)

    routers = [v for v in topology.nodes() if v not in sources + receivers]

    # add stacks to nodes
    topology.graph['icr_candidates'] = set(routers)
    for v in sources:
        fnss.add_stack(topology, v, 'source')
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver')
    for v in routers:
        fnss.add_stack(topology, v, 'router')

    # set weights and delays on all links
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_constant(topology, delay, 'ms')
    return IcnTopology(topology)


@register_topology_factory('TISCALI')
def topology_tiscali(delay=1, **kwargs):
    """Return a scenario based on Tiscali topology, parsed from RocketFuel dataset

    Parameters
    ----------
    seed : int, optional
        The seed used for random number generation

    Returns
    -------
    topology : fnss.Topology
        The topology object
    """
    # 240 nodes in the main component
    topology = fnss.parse_rocketfuel_isp_map(path.join(TOPOLOGY_RESOURCES_DIR,
                                                       '3257.r0.cch')
                                             ).to_undirected()
    topology = list(nx.connected_component_subgraphs(topology))[0]
    # degree of nodes
    leafs = topology.nodes()
    print ("TISCALI : %d, %d", len(leafs), len(topology.edges()))  
    deg = nx.degree(topology)
    source_attachments = highest(topology, deg) 

    sources = []
    for v in source_attachments:
        u = v + 1000  # node ID of source
        topology.add_edge(v, u)
        sources.append(u)
    receivers = []
    for v in leafs:
        u = v + 2000
        topology.add_edge(v, u)
        receivers.append(u)

    routers = [v for v in topology.nodes() if v not in sources + receivers]

    # add stacks to nodes
    topology.graph['icr_candidates'] = set(routers)
    for v in sources:
        fnss.add_stack(topology, v, 'source')
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver')
    for v in routers:
        fnss.add_stack(topology, v, 'router')

    # set weights and delays on all links
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_constant(topology, delay, 'ms')
    return IcnTopology(topology)


@register_topology_factory('WIDE')
def topology_wide(delay=1, **kwargs):
    """Return a scenario based on GARR topology

    Parameters
    ----------
    seed : int, optional
        The seed used for random number generation

    Returns
    -------
    topology : fnss.Topology
        The topology object
    """
    topology = fnss.parse_topology_zoo(path.join(TOPOLOGY_RESOURCES_DIR, 'WideJpn.graphml')).to_undirected()
    # sources are nodes representing neighbouring AS's
    leafs = topology.nodes()
    print ("WIDE : %d, %d", len(leafs), len(topology.edges()))  
    deg = nx.degree(topology)
    source_attachments = highest(topology, deg) 

    sources = []
    for v in source_attachments:
        u = v + 1000  # node ID of source
        topology.add_edge(v, u)
        sources.append(u)
    receivers = []
    for v in leafs:
        u = v + 2000
        topology.add_edge(v, u)
        receivers.append(u)

    routers = [v for v in topology.nodes() if v not in sources + receivers]

    # add stacks to nodes
    topology.graph['icr_candidates'] = set(routers)
    for v in sources:
        fnss.add_stack(topology, v, 'source')
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver')
    for v in routers:
        fnss.add_stack(topology, v, 'router')

    # set weights and delays on all links
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_constant(topology, delay, 'ms')
    return IcnTopology(topology)


@register_topology_factory('GARR')
def topology_garr(delay=1, **kwargs):
    """Return a scenario based on GARR topology

    Parameters
    ----------
    seed : int, optional
        The seed used for random number generation

    Returns
    -------
    topology : fnss.Topology
        The topology object
    """
    topology = fnss.parse_topology_zoo(path.join(TOPOLOGY_RESOURCES_DIR, 'Garr201201.graphml')).to_undirected()
    # sources are nodes representing neighbouring AS's
    leafs = topology.nodes()  
    print ("GARR : %d, %d", len(leafs), len(topology.edges()))
    deg = nx.degree(topology)
    source_attachments = highest(topology, deg) 

    sources = []
    for v in source_attachments:
        u = v + 1000  # node ID of source
        topology.add_edge(v, u)
        sources.append(u)
    receivers = []
    for v in leafs:
        u = v + 2000
        topology.add_edge(v, u)
        receivers.append(u)

    routers = [v for v in topology.nodes() if v not in sources + receivers]

    # add stacks to nodes
    topology.graph['icr_candidates'] = set(routers)
    for v in sources:
        fnss.add_stack(topology, v, 'source')
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver')
    for v in routers:
        fnss.add_stack(topology, v, 'router')

    # set weights and delays on all links
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_constant(topology, delay, 'ms')
    return IcnTopology(topology)


@register_topology_factory('GARR_2')
def topology_garr2(**kwargs):
    """Return a scenario based on GARR topology.

    Differently from plain GARR, this topology some receivers are appended to
    routers and only a subset of routers which are actually on the path of some
    traffic are selected to become ICN routers. These changes make this
    topology more realistic.

    Parameters
    ----------
    seed : int, optional
        The seed used for random number generation

    Returns
    -------
    topology : fnss.Topology
        The topology object
    """
    topology = fnss.parse_topology_zoo(path.join(TOPOLOGY_RESOURCES_DIR, 'Garr201201.graphml')).to_undirected()

    # sources are nodes representing neighbouring AS's
    sources = [0, 2, 3, 5, 13, 16, 23, 24, 25, 27, 51, 52, 54]
    # receivers are internal nodes with degree = 1
    receivers = [1, 7, 8, 9, 11, 12, 19, 26, 28, 30, 32, 33, 41, 42, 43, 47, 48, 50, 53, 57, 60]
    # routers are all remaining nodes --> 27 caches
    routers = [n for n in topology.nodes_iter() if n not in receivers + sources]
    artificial_receivers = list(range(1000, 1000 + len(routers)))
    for i in range(len(routers)):
        topology.add_edge(routers[i], artificial_receivers[i])
    receivers += artificial_receivers
    # Caches to nodes with degree > 3 (after adding artificial receivers)
    degree = nx.degree(topology)
    icr_candidates = [n for n in topology.nodes_iter() if degree[n] > 3.5]
    # set weights and delays on all links
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_constant(topology, INTERNAL_LINK_DELAY, 'ms')

    # Deploy stacks
    topology.graph['icr_candidates'] = set(icr_candidates)
    for v in sources:
        fnss.add_stack(topology, v, 'source')
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver')
    for v in routers:
        fnss.add_stack(topology, v, 'router')
    # label links as internal or external
    for u, v in topology.edges():
        if u in sources or v in sources:
            topology.edge[u][v]['type'] = 'external'
            # this prevents sources to be used to route traffic
            fnss.set_weights_constant(topology, 1000.0, [(u, v)])
            fnss.set_delays_constant(topology, EXTERNAL_LINK_DELAY, 'ms', [(u, v)])
        else:
            topology.edge[u][v]['type'] = 'internal'
    return IcnTopology(topology)


@register_topology_factory('GEANT_2')
def topology_geant2(**kwargs):
    """Return a scenario based on GEANT topology.

    Differently from plain GEANT, this topology some receivers are appended to
    routers and only a subset of routers which are actually on the path of some
    traffic are selected to become ICN routers. These changes make this
    topology more realistic.

    Parameters
    ----------
    seed : int, optional
        The seed used for random number generation

    Returns
    -------
    topology : fnss.Topology
        The topology object
    """
    # 53 nodes
    topology = fnss.parse_topology_zoo(path.join(TOPOLOGY_RESOURCES_DIR,
                                                 'Geant2012.graphml')
                                       ).to_undirected()
    topology = list(nx.connected_component_subgraphs(topology))[0]
    deg = nx.degree(topology)
    receivers = [v for v in topology.nodes() if deg[v] == 1]  # 8 nodes
    # attach sources to topology
    source_attachments = [v for v in topology.nodes() if deg[v] == 2]  # 13 nodes
    sources = []
    for v in source_attachments:
        u = v + 1000  # node ID of source
        topology.add_edge(v, u)
        sources.append(u)
    routers = [v for v in topology.nodes() if v not in sources + receivers]
    # Put caches in nodes with top betweenness centralities
    betw = nx.betweenness_centrality(topology)
    routers = sorted(routers, key=lambda k: betw[k])
    # Select as ICR candidates the top 50% routers for betweenness centrality
    icr_candidates = routers[len(routers) // 2:]
    # add stacks to nodes
    topology.graph['icr_candidates'] = set(icr_candidates)
    for v in sources:
        fnss.add_stack(topology, v, 'source')
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver')
    for v in routers:
        fnss.add_stack(topology, v, 'router')
    # set weights and delays on all links
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_constant(topology, INTERNAL_LINK_DELAY, 'ms')
    # label links as internal or external
    for u, v in topology.edges_iter():
        if u in sources or v in sources:
            topology.edge[u][v]['type'] = 'external'
            # this prevents sources to be used to route traffic
            fnss.set_weights_constant(topology, 1000.0, [(u, v)])
            fnss.set_delays_constant(topology, EXTERNAL_LINK_DELAY, 'ms', [(u, v)])
        else:
            topology.edge[u][v]['type'] = 'internal'
    return IcnTopology(topology)

@register_topology_factory('TISCALI_2')
def topology_tiscali2(**kwargs):
    """Return a scenario based on Tiscali topology, parsed from RocketFuel dataset

    Differently from plain Tiscali, this topology some receivers are appended to
    routers and only a subset of routers which are actually on the path of some
    traffic are selected to become ICN routers. These changes make this
    topology more realistic.

    Parameters
    ----------
    seed : int, optional
        The seed used for random number generation

    Returns
    -------
    topology : fnss.Topology
        The topology object
    """
    # 240 nodes in the main component
    topology = fnss.parse_rocketfuel_isp_map(path.join(TOPOLOGY_RESOURCES_DIR,
                                                       '3257.r0.cch')
                                             ).to_undirected()
    topology = list(nx.connected_component_subgraphs(topology))[0]
    # degree of nodes
    deg = nx.degree(topology)
    # nodes with degree = 1
    onedeg = [v for v in topology.nodes() if deg[v] == 1]  # they are 80
    # we select as caches nodes with highest degrees
    # we use as min degree 6 --> 36 nodes
    # If we changed min degrees, that would be the number of caches we would have:
    # Min degree    N caches
    #  2               160
    #  3               102
    #  4                75
    #  5                50
    #  6                36
    #  7                30
    #  8                26
    #  9                19
    # 10                16
    # 11                12
    # 12                11
    # 13                 7
    # 14                 3
    # 15                 3
    # 16                 2
    icr_candidates = [v for v in topology.nodes() if deg[v] >= 6]  # 36 nodes
    # Add remove caches to adapt betweenness centrality of caches
    for i in [181, 208, 211, 220, 222, 250, 257]:
        icr_candidates.remove(i)
    icr_candidates.extend([232, 303, 326, 363, 378])
    # sources are node with degree 1 whose neighbor has degree at least equal to 5
    # we assume that sources are nodes connected to a hub
    # they are 44
    sources = [v for v in onedeg if deg[list(topology.edge[v].keys())[0]] > 4.5]  # they are
    # receivers are node with degree 1 whose neighbor has degree at most equal to 4
    # we assume that receivers are nodes not well connected to the network
    # they are 36
    receivers = [v for v in onedeg if deg[list(topology.edge[v].keys())[0]] < 4.5]
    # we set router stacks because some strategies will fail if no stacks
    # are deployed
    routers = [v for v in topology.nodes() if v not in sources + receivers]

    # set weights and delays on all links
    fnss.set_weights_constant(topology, 1.0)
    fnss.set_delays_constant(topology, INTERNAL_LINK_DELAY, 'ms')

    # deploy stacks
    topology.graph['icr_candidates'] = set(icr_candidates)
    for v in sources:
        fnss.add_stack(topology, v, 'source')
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver')
    for v in routers:
        fnss.add_stack(topology, v, 'router')

    # label links as internal or external
    for u, v in topology.edges():
        if u in sources or v in sources:
            topology.edge[u][v]['type'] = 'external'
            # this prevents sources to be used to route traffic
            fnss.set_weights_constant(topology, 1000.0, [(u, v)])
            fnss.set_delays_constant(topology, EXTERNAL_LINK_DELAY, 'ms', [(u, v)])
        else:
            topology.edge[u][v]['type'] = 'internal'
    return IcnTopology(topology)


@register_topology_factory('ROCKET_FUEL')
def topology_rocketfuel_latency(asn, source_ratio=0.1, ext_delay=EXTERNAL_LINK_DELAY, **kwargs):
    """Parse a generic RocketFuel topology with annotated latencies

    To each node of the parsed topology it is attached an artificial receiver
    node. To the routers with highest degree it is also attached a source node.

    Parameters
    ----------
    asn : int
        AS number
    source_ratio : float
        Ratio between number of source nodes (artificially attached) and routers
    ext_delay : float
        Delay on external nodes
    """
    if source_ratio < 0 or source_ratio > 1:
        raise ValueError('source_ratio must be comprised between 0 and 1')
    f_topo = path.join(TOPOLOGY_RESOURCES_DIR, 'rocketfuel-latency', str(asn), 'latencies.intra')
    topology = fnss.parse_rocketfuel_isp_latency(f_topo).to_undirected()
    topology = list(nx.connected_component_subgraphs(topology))[0]
    # First mark all current links as inernal
    for u, v in topology.edges_iter():
        topology.edge[u][v]['type'] = 'internal'
    # Note: I don't need to filter out nodes with degree 1 cause they all have
    # a greater degree value but we compute degree to decide where to attach sources
    routers = topology.nodes()
    # Source attachment
    n_sources = int(source_ratio * len(routers))
    sources = ['src_%d' % i for i in range(n_sources)]
    deg = nx.degree(topology)

    # Attach sources based on their degree purely, but they may end up quite clustered
    routers = sorted(routers, key=lambda k: deg[k], reverse=True)
    for i in range(len(sources)):
        topology.add_edge(sources[i], routers[i], delay=ext_delay, type='external')

    # Here let's try attach them via cluster
#     clusters = compute_clusters(topology, n_sources, distance=None, n_iter=1000)
#     source_attachments = [max(cluster, key=lambda k: deg[k]) for cluster in clusters]
#     for i in range(len(sources)):
#         topology.add_edge(sources[i], source_attachments[i], delay=ext_delay, type='external')

    # attach artificial receiver nodes to ICR candidates
    receivers = ['rec_%d' % i for i in range(len(routers))]
    for i in range(len(routers)):
        topology.add_edge(receivers[i], routers[i], delay=0, type='internal')
    # Set weights to latency values
    for u, v in topology.edges_iter():
        topology.edge[u][v]['weight'] = topology.edge[u][v]['delay']
    # Deploy stacks on nodes
    topology.graph['icr_candidates'] = set(routers)
    for v in sources:
        fnss.add_stack(topology, v, 'source')
    for v in receivers:
        fnss.add_stack(topology, v, 'receiver')
    for v in routers:
        fnss.add_stack(topology, v, 'router')
    return IcnTopology(topology)

