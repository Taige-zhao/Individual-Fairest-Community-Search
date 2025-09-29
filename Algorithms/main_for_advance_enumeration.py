import numpy as np
import time

from typing import Dict, Generator, Hashable, List, Optional, Union, Tuple

import networkx as nx
# from grandiso.queues import SimpleQueue
import random
from Advance_enumeration import Advanced_algorithm, generate_dictionary, max_Out_and_In_edge_hops, Advanced_Refine, calculate_fairness_score
from navie_enumeration import baseline
from navie_enumeration import gini_coefficient

# processed 970 enumerations. Time: 1154.600664138794

# processed 10 enumerations. Time: 24.934698820114136
# processed 20 enumerations. Time: 39.61201596260071
# processed 30 enumerations. Time: 62.701754331588745
# processed 40 enumerations. Time: 81.28060913085938
# processed 50 enumerations. Time: 96.76211762428284
# processed 60 enumerations. Time: 107.5894980430603
# processed 70 enumerations. Time: 117.54463291168213
# processed 80 enumerations. Time: 135.2267382144928
# processed 90 enumerations. Time: 156.72251319885254
# processed 100 enumerations. Time: 167.36266088485718

# processed 10 enumerations. Time: 3.5048434734344482
# processed 20 enumerations. Time: 5.680452823638916
# processed 30 enumerations. Time: 9.128271102905273
# processed 40 enumerations. Time: 12.086328268051147
# processed 50 enumerations. Time: 14.59267807006836
# processed 60 enumerations. Time: 17.169113874435425
# processed 70 enumerations. Time: 20.056951761245728
# processed 80 enumerations. Time: 22.993520498275757
# processed 90 enumerations. Time: 26.41484808921814
# processed 100 enumerations. Time: 28.653048276901245
# processed 110 enumerations. Time: 30.989360332489014


import networkx as nx
import numpy as np
import time

import sys
sys.setrecursionlimit(int(10e8))

IMDB = nx.read_gpickle('./IMDB.gpickle')

IMDB_motif=nx.DiGraph()

# IMDB_motif.add_node(0, type="actor")
# IMDB_motif.add_node(1, type="movie")
# # IMDB_motif.add_node(2, type="movie")
# IMDB_motif.add_node(2, type="actor")
# IMDB_motif.add_node(3, type="actor")

# IMDB_motif.add_edge(0, 1)
# # IMDB_motif.add_edge(0, 2)
# IMDB_motif.add_edge(2, 1)
# IMDB_motif.add_edge(3, 1)

from  AAN_search import generate_AAN, in_degree_k_core, vertex_id_with_the_same_type_of_target_vertex_except_target_vertex_in_motif, calculate_fairness_score_from_AAN
import operator

# IMDB_motif.add_node(0, type="actor")
# IMDB_motif.add_node(1, type="movie")
# IMDB_motif.add_node(2, type="movie")
# IMDB_motif.add_node(3, type="actor")
#
# IMDB_motif.add_edge(0, 1)
# IMDB_motif.add_edge(0, 2)
# IMDB_motif.add_edge(3, 2)

IMDB_motif.add_node(0, type="actor")
IMDB_motif.add_node(1, type="movie")
IMDB_motif.add_node(2, type="movie")
# IMDB_motif.add_node(3, type="actor")
IMDB_motif.add_node(4, type="actor")

IMDB_motif.add_edge(0, 1)
IMDB_motif.add_edge(0, 2)
# IMDB_motif.add_edge(3, 2)
IMDB_motif.add_edge(4, 2)

# time_start = time.time()
# maxC = []; now_existing_target_vertex_number = 0; count = 0
# communities = Advanced_algorithm(IMDB, IMDB_motif, 0, 0.2)
target_vertex_id = 0
S, D = generate_dictionary(IMDB_motif, IMDB, target_vertex_id)
G_small = IMDB.subgraph(S)
motif_hops = max_Out_and_In_edge_hops(IMDB_motif, target_vertex_id)
G_small, D_small = Advanced_Refine(G_small, D, IMDB_motif, target_vertex_id, motif_hops)
# time_end = time.time()

# AAN = generate_AAN(IMDB_motif, IMDB, target_vertex_id, "IMDB_AAN_1")

# target_label_except_target_vertex_in_motif = vertex_id_with_the_same_type_of_target_vertex_except_target_vertex_in_motif(IMDB_motif, target_vertex_id)
# refined_AAN, node_participation_dict = in_degree_k_core(AAN, len(target_label_except_target_vertex_in_motif))
#
# print(operator.eq(list(D_small.keys()).sort(), list(refined_AAN.nodes()).sort()))
# print(operator.eq(list(D.keys()).sort(), list(AAN.nodes()).sort()))
# print(D_small)
print(calculate_fairness_score(D_small))

# print(gini_coefficient(list(node_participation_dict.values())))
# print(len(S))
# print("time cost: ", time_end - time_start, "s")