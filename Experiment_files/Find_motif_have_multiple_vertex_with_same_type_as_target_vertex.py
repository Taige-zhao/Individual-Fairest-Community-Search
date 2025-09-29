import os
import copy
import glob
import shutil

import numpy as np
from utils import get_BFS_order, generate_candidate_set, generate_motif, select_motif
import time
import random

# from  navie_enumeration import generate_dictionary, calculate_fairness_score
from utils import count_target_vertex_instance_number_in_community, EFS, BaseLine, generate_dictionary, propagation_based_filter
from Advance_enumeration import max_Out_and_In_edge_hops, Advanced_Refine

# import ssl
# ssl.match_hostname = lambda cert, hostname: True

import networkx as nx
from collections import Counter

start = time.time()
Amazon = nx.read_gpickle('../Amazon_Product.gpickle')
# Amazon = nx.read_gpickle('../IMDB.gpickle')

q, target_vertex_id, target_type = select_motif(Amazon, 5)
# q = nx.edge_subgraph(Amazon, [(7239, 4137), (4137, 4806), (4137, 7754), (4137, 7679)])
# q = generate_motif(Amazon, 5, 1)[0]
# target_vertex_id = start_node = random.sample(q.nodes(), 1)[0]

# target_vertex_id = 7239
quality_limitation = 0

# q = nx.read_gpickle('../toy_motif_of_Amazon_Product.gpickle')
# target_vertex_id = 156356; target_type = 97

nx.write_gpickle(q,'../toy_motif_of_Amazon_Product.gpickle')

print("loading graph: time " + str(time.time() - start) + "s")

print(q.nodes(data=True))
print(q.edges())
print(target_vertex_id)
# print(target_type)

start = time.time()

connected_graphs = propagation_based_filter(Amazon, q, quality_limitation, target_vertex_id)
print("Candidate region generation time: " + str(time.time() - start) + "s")

print(len(connected_graphs))
nodes = []
for i in connected_graphs:
    print(i)
    for v in i:
        nodes.append(v)

EFS_graph = nx.subgraph(Amazon, nodes).copy()
nx.write_gpickle(EFS_graph,'../EFS_Amazon_Graph.gpickle')
# #
#

graphs = []
start = time.time()
for connected_graph in connected_graphs:
    graphs.append(nx.subgraph(Amazon, connected_graph).copy())
print("Transfer Time: " + str(time.time() - start) + "s")

start = time.time()
for graph in graphs:
    S, D = generate_dictionary(q, graph, target_vertex_id)
print("Enumeration Time: " + str(time.time() - start) + "s")

start = time.time()

S, D = generate_dictionary(q, Amazon
                           , target_vertex_id)
print("Directly Enumeration Time: " + str(time.time() - start) + "s")


# v_t = 0; theta = 1; quality_limitation=10; best_fairness_score = 0
# # q_labels = nx.get_node_attributes(q, 'type')
#
# # maxC = EFS(IMDB, q, v_t, quality_limitation, theta)
# maxC = BaseLine(IMDB, q, v_t, quality_limitation, theta)
# print(maxC)
# # start = time.time()
# # S, D = generate_dictionary(q, IMDB, v_t)
# # print(str(time.time() - start) + "s")


