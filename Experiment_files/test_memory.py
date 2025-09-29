import networkx as nx
import numpy as np
import time
from utils import *
from test_util import *


DBLP = nx.read_gpickle('../Amazon_Product.gpickle')
# DBLP = nx.read_gpickle('../DBLP.gpickle')
# DBLP = nx.read_gpickle('../IMDB.gpickle')
# DBLP = nx.read_gpickle('../Freebase.gpickle')

DBLP = divide_graph(DBLP, 0.2)

# print("Doing DBLP...")
# print(len(DBLP.nodes()))
#
# motifs = []

# q=nx.DiGraph()
#
# q.add_node(0, type="author")
# q.add_node(1, type="paper")
# q.add_node(3, type="paper")
# q.add_node(4, type="author")
#
# q.add_edge(0, 1)
# q.add_edge(0, 3)
# q.add_edge(4, 1)

# q, target_vertex_id, target_type = select_motif(DBLP, 5)
#
# motifs.append(q)

# target_vertex_id = 0
# q, target_vertex_id, target_type = select_motif(DBLP, 3)
# motifs.append(q)
#
# number_of_motifs = len(motifs)
#
# for motif in range(0, number_of_motifs):
#     print("Doing baseline")
#
#     q = motifs[motif]

    # start_itr = time.time()
    # Adv_BaseLine_test_memory(DBLP, q, target_vertex_id, 10)
    # print("Time used of baseline: " + str(time.time()-start_itr) + "s")

    # _, _, time_temp = EFS_test_memory(DBLP, q, target_vertex_id, 10)
    # print("Time used of EFS: " + str(time_temp) + "s")


# print("Doing IMDB...")
#
# DBLP = nx.read_gpickle('../IMDB.gpickle')
#
# print(len(DBLP.nodes()))
#
# motifs = []
#
# # q=nx.DiGraph()
# #
# # q.add_node(0, type="author")
# # q.add_node(1, type="paper")
# # q.add_node(3, type="paper")
# # q.add_node(4, type="author")
# #
# # q.add_edge(0, 1)
# # q.add_edge(0, 3)
# # q.add_edge(4, 1)
#
# q, target_vertex_id, target_type = select_motif(DBLP, 5)
#
# motifs.append(q)
#
# # target_vertex_id = 0
# # q, target_vertex_id, target_type = select_motif(DBLP, 3)
# # motifs.append(q)
#
# number_of_motifs = len(motifs)
#
# for motif in range(0, number_of_motifs):
#     print("Doing baseline")
#
#     q = motifs[motif]
#
#     start_itr = time.time()
#     Adv_BaseLine_test_memory(DBLP, q, target_vertex_id, 10)
#     print("Time used of baseline: " + str(time.time()-start_itr) + "s")
#
#     _, _, time_temp = EFS_test_memory(DBLP, q, target_vertex_id, 10)
#     print("Time used of EFS: " + str(time_temp) + "s")




# DBLP = nx.read_gpickle('../DBLP.DBLPgpickle')
# DBLP = nx.read_gpickle('../IMDB.gpickle')
# DBLP = nx.read_gpickle('../Freebase.gpickle')
#
# DBLP = divide_graph(DBLP, 0.25)
#
# print("Doing Freebase...")
print(len(DBLP.nodes()))

motifs = []

q=nx.DiGraph()
#
# q.add_node(0, type="author")
# q.add_node(1, type="paper")
# q.add_node(3, type="paper")
# q.add_node(4, type="author")
#
# q.add_edge(0, 1)
# q.add_edge(0, 3)
# q.add_edge(4, 1)

for _ in range(0,1):
    q, target_vertex_id, target_type = select_motif(DBLP, 5)
    motifs.append((q, target_vertex_id))

# target_vertex_id = 0
# q, target_vertex_id, target_type = select_motif(DBLP, 3)
# motifs.append(q)

number_of_motifs = len(motifs)

print("finish form motif")

average_memory_Baseline = []
average_memory_EFS = []

for motif in range(0, number_of_motifs):
    print("Doing " + str(motif) + " motif...")

    q = motifs[motif][0]

    target_vertex_id = motifs[motif][1]

    # start_itr = time.time()
    # _, _, _, _, baseline_memory = Adv_BaseLine_test_memory(DBLP, q, target_vertex_id, 10)
    # print("Time used of baseline: " + str(time.time()-start_itr) + "s")
    #
    # average_memory_Baseline.append(baseline_memory)

    _, _, time_temp, EFS_memory = EFS_test_memory(DBLP, q, target_vertex_id, 10)
    print("Time used of EFS: " + str(time_temp) + "s")

    average_memory_EFS.append(EFS_memory)

    print("\n\n")

from numpy import mean
# print("Average Baseline Memory: " + str( mean(average_memory_Baseline) ))

print("Average EFS Memory: " + str( mean(average_memory_EFS) ))


# print("Doing Amazon...")
# # DBLP = nx.read_gpickle('../DBLP.DBLPgpickle')
# # DBLP = nx.read_gpickle('../IMDB.gpickle')
# DBLP = nx.read_gpickle('../Amazon_Product.gpickle')
#
# DBLP = divide_graph(DBLP, 0.2)
#
# print(len(DBLP.nodes()))
#
# motifs = []
#
# # q=nx.DiGraph()
# #
# # q.add_node(0, type="author")
# # q.add_node(1, type="paper")
# # q.add_node(3, type="paper")
# # q.add_node(4, type="author")
# #
# # q.add_edge(0, 1)
# # q.add_edge(0, 3)
# # q.add_edge(4, 1)
#
# q, target_vertex_id, target_type = select_motif(DBLP, 5)
#
# motifs.append(q)
#
# # target_vertex_id = 0
# # q, target_vertex_id, target_type = select_motif(DBLP, 3)
# # motifs.append(q)
#
# number_of_motifs = len(motifs)
#
# for motif in range(0, number_of_motifs):
#     print("Doing baseline")
#
#     q = motifs[motif]
#
#     start_itr = time.time()
#     Adv_BaseLine_test_memory(DBLP, q, target_vertex_id, 10)
#     print("Time used of baseline: " + str(time.time()-start_itr) + "s")
#
#     _, _, time_temp = EFS_test_memory(DBLP, q, target_vertex_id, 10)
#     print("Time used of EFS: " + str(time_temp) + "s")