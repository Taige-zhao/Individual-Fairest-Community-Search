import networkx as nx
import numpy as np
import time
from utils import generate_dictionary
from utils import generate_dictionary_of_target_vertex_instance
from utils import Baseline, Adv_BaseLine

DBLP = nx.read_gpickle('../DBLP.gpickle')

q=nx.DiGraph()

q.add_node(0, type="author")
q.add_node(1, type="paper")
q.add_node(2, type="paper")
q.add_node(3, type="author")
q.add_node(4, type="author")
q.add_node(5, type="author")

q.add_edge(0, 1)
q.add_edge(0, 2)
q.add_edge(3, 2)
q.add_edge(4, 2)
# q.add_edge(3, 2)
q.add_edge(5, 2)

target_vertex_id = 0

# taget_vertex_label = nx.get_node_attributes(q, "type")[target_vertex_id]
# graph_label = nx.get_node_attributes(DBLP, "type")
# vertices_id_with_target_type_in_graph = [i[0] for i in graph_label.items() if i[1] == taget_vertex_label]

start = time.time()
D_, M_graph, maxC, best_score = Adv_BaseLine(DBLP, q, target_vertex_id, 5, 1)
print(str(time.time() - start) + "s")

print("\n-------------------------0000-------------------------\n")


start = time.time()
S, D, maxC_, best_score_ = Baseline(DBLP, q, target_vertex_id, 5, 1)
print(str(time.time() - start) + "s")
#

print(set(S) == set(M_graph.nodes()))
print(D == D_)
print(set(maxC[0]) == set(maxC_[0]))
print(best_score == best_score_)

print(maxC)
print(maxC_)

print(best_score_) # baseline
print(best_score) # adv









#
# start = time.time()
# S, D = generate_dictionary(q, DBLP, target_vertex_id)
# print(str(time.time() - start) + "s")
#
# start = time.time()
# S_small, D_small = generate_dictionary_of_target_vertex_instance(q, DBLP, target_vertex_id, vertices_id_with_target_type_in_graph)
# print(S_small)
# print(D_small)
# print(str(time.time() - start) + "s")
#
# print(S == S_small)
# print(D == D_small)

