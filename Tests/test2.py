import networkx as nx
import time

from typing import Dict, Generator, Hashable, List, Optional, Union, Tuple

import networkx as nx
import random

from test7_for_Community import generate_AAN_and_refined_graphs

from Advance_enumeration import generate_dictionary_of_target_vertex_instance
from  navie_enumeration import generate_dictionary, Refine
from fliter_enumeration import divide_graph
from Advance_enumeration import max_Out_and_In_edge_hops, Advanced_Refine
__version__ = "2.1.1"

from enumerate_motif import _is_node_attr_match, _is_node_structural_match, _is_edge_attr_match, find_motifs_iter
from utils import count_target_vertex_instance_number_in_community

# 1939743
# 21111007
# generate from original: 100.46603393554688
# Count: 7145660
# generate original motif_refined graph: 132.89213180541992
# 1871038
# 7145660
# refine后的graph超过1000秒了，所以不能refine。

# def naive_filter(G, )

IMDB_motif=nx.DiGraph()
target_vertex_id = 0
IMDB_motif.add_node(0, type="actor")
IMDB_motif.add_node(1, type="movie")
IMDB_motif.add_node(2, type="movie")
# # IMDB_motif.add_node(3, type="movie")
# # IMDB_motif.add_node(4, type="movie")
# IMDB_motif.add_node(5, type="actor")
# IMDB_motif.add_node(4, type="actor")

# IMDB_motif.add_node(0, type="author")
# IMDB_motif.add_node(1, type="paper")
# IMDB_motif.add_node(2, type="paper")
# # IMDB_motif.add_node(3, type="paper")
# IMDB_motif.add_node(4, type="author")
# IMDB_motif.add_node(3, type="author")
# IMDB_motif.add_node(4, type="author")

IMDB_motif.add_edge(0, 1)
# IMDB_motif.add_edge(4, 1)
# IMDB_motif.add_edge(2, 1)
# IMDB_motif.add_edge(3, 1)
# IMDB_motif.add_edge(4, 1)
IMDB_motif.add_edge(0, 2)
# IMDB_motif.add_edge(0, 3)
# IMDB_motif.add_edge(0, 4)
# IMDB_motif.add_edge(5, 2)
# IMDB_motif.add_edge(4, 2)

IMDB = nx.read_gpickle('./IMDB.gpickle')
# IMDB = nx.read_gpickle('./DBLP.gpickle')
# IMDB = divide_graph(IMDB, 0.4)
# print(len(IMDB.nodes()))
# print(len(IMDB.edges()))

# print(sum([1 for _ in nx.weakly_connected_components(IMDB_motif)]))

# start_time = time.time()
S, D = generate_dictionary(IMDB_motif, IMDB, 0)
G_small = IMDB.subgraph(S).copy()
motif_hops = max_Out_and_In_edge_hops(IMDB_motif, target_vertex_id)
G_small, D_small = Advanced_Refine(G_small, D, IMDB_motif, target_vertex_id, motif_hops)
# G_small, D_small = Refine(G_small, IMDB_motif, target_vertex_id)
# print(sum([1 for _ in nx.weakly_connected_components(G_small)]))


for i in nx.weakly_connected_components(G_small):
    count = count_target_vertex_instance_number_in_community(G_small.subgraph(i), IMDB_motif, target_vertex_id)
    print(count_target_vertex_instance_number_in_community(G_small.subgraph(i), IMDB_motif, target_vertex_id))

# print("generate from original: " + str(time.time()-start_time))
#
# # print(D.keys())
# # print("Count: " + str(count))
# #
# # start_time0 = time.time()
# # graph = generate_AAN_and_refined_graphs(IMDB_motif, IMDB)
# # print("generate original motif_refined graph: " + str(time.time()-start_time0))
#
# # print(len(graph.nodes()))
# # print(len(graph.edges()))
#
# # start_time1 = time.time()
# # count = generate_dictionary(IMDB_motif, graph)
# # print("generate from original: " + str(time.time()-start_time1))
# # print("Count: " + str(count))
#
# start_time = time.time()
# S, D = generate_dictionary_of_target_vertex_instance(IMDB_motif, IMDB, 0, list(D.keys()))
# print(str(time.time()-start_time))
#
# print(S)
# print(D)
