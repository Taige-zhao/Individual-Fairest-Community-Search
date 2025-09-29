import sys
import math
import time
import networkx as nx
# from Advance_enumeration import Advanced_algorithm, generate_dictionary, max_Out_and_In_edge_hops, Advanced_Refine, calculate_fairness_score
from fliter_enumeration import divide_graph
import numpy as np
import psutil
import random
# from utils import generate_dictionary
from navie_enumeration import generate_dictionary
from utils import generate_motif

print("333")
start = time.time()
# IMDB = nx.read_gpickle('./DBLP.gpickle')
# IMDB = nx.read_gpickle('./OGB_MAG.gpickle')
IMDB = nx.read_gpickle('./Amazon_Product.gpickle')
# target_vertex_id = 0

print("finish load graph")
print((time.time() - start))

# target_vertex_id = 0
IMDB_motif = nx.DiGraph()

motifs = generate_motif(IMDB, 5, 1)
IMDB_motif = motifs[0]
target_vertex_id = random.sample(IMDB_motif.nodes(), 1)[0]

print("Motif nodes are: ")
print(IMDB_motif.nodes())

print("Motif edges are: ")
print(IMDB_motif.edges())

# IMDB_motif.add_node(0, type="author")
# IMDB_motif.add_node(1, type="paper")
# IMDB_motif.add_node(2, type="author")
# IMDB_motif.add_node(3, type="author")
# IMDB_motif.add_node(4, type="author")

# IMDB_motif.add_node(0, type="paper")
# IMDB_motif.add_node(1, type="paper")
# IMDB_motif.add_node(2, type="paper")
# IMDB_motif.add_node(3, type="paper")
# # IMDB_motif.add_node(4, type="paper")
# IMDB_motif.add_node(5, type="field_of_study")

# IMDB_motif.add_edge(1, 0)
# IMDB_motif.add_edge(2, 0)
# IMDB_motif.add_edge(3, 0)
# # IMDB_motif.add_edge(0, 4)
# # IMDB_motif.add_edge(0, 5)
# IMDB_motif.add_edge(0, 5)
# IMDB_motif.add_edge(1, 5)
# IMDB_motif.add_edge(3, 5)
# IMDB_motif.add_edge(4, 5)


# IMDB_motif.add_edge(0, 1)
# IMDB_motif.add_edge(2, 1)
# IMDB_motif.add_edge(3, 1)
# IMDB_motif.add_edge(4, 1)
# IMDB_motif.add_edge(3, 2)

start = time.time()
print("start enumeration motif instance...")
S, D = generate_dictionary(IMDB_motif, IMDB, target_vertex_id)
# D = generate_dictionary(IMDB_motif, IMDB, target_vertex_id)
# generate_dictionary(IMDB_motif, test, target_vertex_id)
# print("finish enumeration, start refine")
print("finish enumeration" + str(time.time() - start))

subgraph = IMDB.subgraph(S).copy()
# np.save("OGB_MAG_motif_5_nodes_original_dic.npy", D)
# nx.write_gpickle(subgraph,'./OGB_MAG_motif_5_nodes_original_community.gpickle')
np.save("Amazon_Product_motif_5_nodes_original_dic.npy", D)
nx.write_gpickle(subgraph,'./Amazon_Product_motif_5_nodes_original_community.gpickle')