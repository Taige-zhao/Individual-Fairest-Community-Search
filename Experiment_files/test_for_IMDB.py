import os
import copy
import glob
import shutil

import numpy as np
from utils import get_BFS_order, generate_candidate_set, generate_motif, select_motif
import time
import random

# from  navie_enumeration import generate_dictionary, calculate_fairness_score
from utils import count_target_vertex_instance_number_in_community, EFS, BaseLine, generate_dictionary, propagation_based_filter, divide_graph
from Advance_enumeration import max_Out_and_In_edge_hops, Advanced_Refine

# import ssl
# ssl.match_hostname = lambda cert, hostname: True

import networkx as nx
from collections import Counter

# [(9991, 1549), (9991, 18417), (9991, 19026), (1549, 6819)]  --171s candidate generation
# 18417

start = time.time()
Amazon = nx.read_gpickle('../DBLP.gpickle')

# Amazon = divide_graph(Amazon,0.2)

q=nx.DiGraph()

q.add_node(0, type="author")
q.add_node(1, type="paper")
# q.add_node(2, type="paper")
q.add_node(3, type="author")
# q.add_node(4, type="author")

q.add_edge(0, 1)
# q.add_edge(0, 2)
q.add_edge(3, 1)
# q.add_edge(4, 2)

# q, target_vertex_id, target_type = select_motif(Amazon, 5)
# q = nx.edge_subgraph(Amazon, [(9991, 1549), (9991, 18417), (9991, 19026), (1549, 6819)])
# q = generate_motif(Amazon, 5, 1)[0]
# target_vertex_id = start_node = random.sample(q.nodes(), 1)[0]

# target_vertex_id = 18417
quality_limitation = 10

# q = nx.read_gpickle('../toy_motif_of_IMDB.gpickle')
target_vertex_id = 0; target_type = "author"

# nx.write_gpickle(q,'../toy_motif_of_IMDB.gpickle')

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
    # print(i)
    for v in i:
        nodes.append(v)

EFS_graph = nx.subgraph(Amazon, nodes).copy()
nx.write_gpickle(EFS_graph,'../toy_EFS_IMDB_Graph.gpickle')
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


