import os
import copy
import glob
import shutil

import numpy as np
from utils import get_BFS_order, generate_candidate_set
import time

from  navie_enumeration import generate_dictionary, calculate_fairness_score
from utils import count_target_vertex_instance_number_in_community, EFS, BaseLine
from Advance_enumeration import max_Out_and_In_edge_hops, Advanced_Refine

# import ssl
# ssl.match_hostname = lambda cert, hostname: True

# dataset = attributed_graph_dataset.AttributedGraphDataset(root="./data/cora", name="PubMed")
# dataset = imdb.IMDB(root='./data/IMDB')
# dataset = dblp.DBLP(root='./data/DBLP')
# data = dataset[0]


# print(data)

# print(data.x)   # 有多少个user，从1编号到2024
# print(data.edge_index)  # 根据编号 有哪些边 连着哪两个编号
# print(data.edge_type[0:10])   # 每个边的类型 用 1 2 3 代替
# print(data.edge_index[1][1:10])
# print(data.edge_norm[0:10])   # 好像是每个边的权重
# print(data.train_gt)    # ground true
# print(data.num_users)   # 用户的总数量


import networkx as nx
from collections import Counter


# def get_neighbor_count(G, v, labels_of_G):
#
#     in_neighbor_count = Counter([labels_of_G[n] for n in set([t[0] for t in G.in_edges(v)])])
#     out_neighbor_count = Counter([labels_of_G[n] for n in set([t[1] for t in G.out_edges(v)])])
#
#     return in_neighbor_count, out_neighbor_count
#
# # {0: Counter(), 1: Counter({'author': 1}), 2: Counter({'author': 1, 'paper': 1}), 3: Counter({'paper': 1}), 4: Counter(), 5: Counter({'paper': 1}), 6: Counter({'paper': 1})}
# def get_q_neighbor_count(q):
#     q_labels = nx.get_node_attributes(q, 'type')
#     in_neighbor_dict = dict()
#     out_neighbor_dict = dict()
#     for node in q.nodes():
#         in_neighbor_dict[node], out_neighbor_dict[node] = get_neighbor_count(q, node, q_labels)
#
#     return in_neighbor_dict, out_neighbor_dict
#
# def NLF(G, v, u, in_neighbor_q, out_neighbor_q, labels_of_G):
#     in_neighbor_count, out_neighbor_count = get_neighbor_count(G, v, labels_of_G)
#
#     for l in in_neighbor_q[u].keys():
#         if l in in_neighbor_count:
#             if in_neighbor_q[u][l] > in_neighbor_count[l]:
#                 return False
#         else:
#             return False
#
#     for l in out_neighbor_q[u].keys():
#         if l in out_neighbor_count:
#             if out_neighbor_q[u][l] > out_neighbor_count[l]:
#                 return False
#         else:
#             return False
#
#     return True

# Test q
# q=nx.DiGraph()
# q.add_node(0, type="A")
# q.add_node(1, type="B")
# q.add_node(2, type="C")
# q.add_node(3, type="C")
#
#
# q.add_edge(0, 1)
# q.add_edge(0, 2)
# q.add_edge(1, 2)
# q.add_edge(3, 1)
# q.add_edge(3, 2)

# q_labels = nx.get_node_attributes(q, 'type')
# v_t = 0
# in_neighbor_q, out_neighbor_q = get_q_neighbor_count(q) # dic = {0: set(), 1: set(), 2: set(), 3: set()}


# Test data graph
# IMDB = nx.read_gpickle('./IMDB.gpickle')
# IMDB = nx.DiGraph()
# IMDB.add_node(1, type="A")
# IMDB.add_node(2, type="A")
# IMDB.add_node(3, type="A")
# IMDB.add_node(4, type="C")
# IMDB.add_node(5, type="B")
# IMDB.add_node(6, type="B")
# IMDB.add_node(7, type="C")
# IMDB.add_node(8, type="B")
# IMDB.add_node(9, type="C")
# IMDB.add_node(10, type="B")
# IMDB.add_node(11, type="C")
# IMDB.add_node(12, type="C")
# IMDB.add_node(13, type="C")
# IMDB.add_node(14, type="C")
# IMDB.add_node(15, type="C")
#
# IMDB.add_edge(1, 4)
# IMDB.add_edge(1, 5)
# IMDB.add_edge(1, 6)
# IMDB.add_edge(1, 7)
# IMDB.add_edge(1, 8)
# IMDB.add_edge(2, 8)
# IMDB.add_edge(2, 9)
# IMDB.add_edge(10, 2)
# IMDB.add_edge(3, 10)
# IMDB.add_edge(3, 11)
# IMDB.add_edge(4, 5)
# IMDB.add_edge(6, 7)
# IMDB.add_edge(8, 7)
# IMDB.add_edge(8, 9)
# IMDB.add_edge(10, 11)
#
# IMDB.add_edge(12, 4)
# IMDB.add_edge(12, 5)
# IMDB.add_edge(12, 6)
# IMDB.add_edge(13, 7)
# IMDB.add_edge(13, 8)
# IMDB.add_edge(6, 13)
# IMDB.add_edge(14, 8)
# IMDB.add_edge(14, 9)
# IMDB.add_edge(14, 10)
# IMDB.add_edge(15, 9)
# IMDB.add_edge(15, 11)


# def quality_filter(G, S, candidate_set, k, G_labels, v_t_label, v_t):
#     G = G.edge_subgraph(list(S))
#     connected_graph = []
#
#     for g in nx.weakly_connected_components(G):
#         if len( set([n for n in g if G_labels[n] == v_t_label]).intersection(candidate_set[v_t]) ) >= k:
#             connected_graph.append(g)
#
#     return connected_graph
#
# def propagation_based_filter(G, q, k): #返回一组已经被fliter好的点集合
#
#     # forward progagtion
#     in_neighbor_q, out_neighbor_q = get_q_neighbor_count(q)
#     G_labels = nx.get_node_attributes(G, 'type')
#     BFS_order, candidate_set_q = get_BFS_order(q, 0); S = set() # Line 1
#     C = [i for i in G.nodes() if NLF(G, i, v_t, in_neighbor_q, out_neighbor_q, G_labels) and G_labels[i] == q_labels[v_t]] # Line 2-3
#
#     for hat_v in C: # Line 4
#         S_ = set(); i_add = True
#
#         temp_candidate_set_q = generate_candidate_set(BFS_order)
#         temp_candidate_set_q[v_t] = set([hat_v])
#
#         for u in list(set(BFS_order) - set([v_t])): # Line 6
#             u_C_ = set()
#             N_u_ = list(set(BFS_order[:BFS_order.index(u)]).intersection(set([t[0] for t in q.in_edges(u)]) | set([t[1] for t in q.out_edges(u)])))
#             u_b = N_u_[0]
#
#             for v in temp_candidate_set_q[u_b]: # Line 10
#                 v_set = set()
#
#                 # 对于新的候选点来说，0：既有in又有out；1：只有in （老点指向新点）；2：只有out
#                 if q.has_edge(u_b, u) and q.has_edge(u, u_b):
#                     v_set = set(G.pred[v].keys()).intersection(set(G.adj[v].keys()))
#                 elif q.has_edge(u_b, u):
#                     v_set = set(G.adj[v].keys())
#                 elif q.has_edge(u, u_b):
#                     v_set = set(G.pred[v].keys())
#
#                 for v_ in [i for i in v_set if G_labels[i] == q_labels[u] and NLF(G, i, u, in_neighbor_q, out_neighbor_q, G_labels)]:
#                     E_t = []; c_add = True
#                     if q.has_edge(u_b, u):
#                         E_t.append((v, v_))
#                     if q.has_edge(u, u_b):
#                         E_t.append((v_, v))
#
#                     for hat_u in (set(N_u_)-set([u_b])): # Line 13
#                         E_t_ = []  #后面这一块都是 Line 14
#                         for v_bar in temp_candidate_set_q[hat_u]:
#                             if q.has_edge(u, hat_u) and q.has_edge(hat_u, u) and G.has_edge(v_, v_bar) and G.has_edge(v_bar, v_):
#                                 E_t_.append((v_bar, v_), (v_, v_bar))
#                             elif q.has_edge(u, hat_u) and G.has_edge(v_, v_bar):
#                                 E_t_.append((v_, v_bar))
#                             elif q.has_edge(hat_u, u) and G.has_edge(v_bar, v_):
#                                 E_t_.append((v_bar, v_))
#
#                         if len(E_t_) == 0: # Line 15
#                             c_add = False; break # Line 16
#                         else: # Line 17
#                             E_t = E_t + E_t_
#
#                     if c_add == True: # Line 18
#                         S_ = S_.union(set(E_t)); temp_candidate_set_q[u].add(v_) # Line 19
#
#             if len(temp_candidate_set_q[u]) == 0: # Line 20
#                 i_add = False; break
#
#         if i_add == True:
#             S = S.union(S_)
#             for u in BFS_order:
#                 candidate_set_q[u] = candidate_set_q[u].union(temp_candidate_set_q[u])
#
#     # quality filter
#     connected_graphs = quality_filter(G, S, candidate_set_q, k, G_labels, q_labels[v_t], v_t)
#
#     # for i in connected_graphs:
#     #     print(len( set([n for n in i if G_labels[n] == q_labels[v_t]] ) ) )
#
#     # backward progagtion
#
#
#     # return S, candidate_set_q
#     return connected_graphs



# def Refine(G, q, target_vertex_id, quality_limitation):
#     back = False;
#     while back == False:
#         S, D = generate_dictionary(q, G, target_vertex_id)
#         if quality_limitation < len(D):
#
#             taget_vertex_label = nx.get_node_attributes(q, "type")[target_vertex_id]
#             graph_label = nx.get_node_attributes(G, "type")
#             S_with_target_vertex_label = [i for i in S if graph_label[i] == taget_vertex_label]
#             G = G.subgraph(S)
#
#             if len(D.keys()) != len(S_with_target_vertex_label):
#                 G = G.subgraph((set(G.nodes()) - set(S_with_target_vertex_label)).union(set(D.keys())))
#             else:
#                 back = True
#         else:
#             back = True
#     return G, D
#
# def EFS(G, q, target_vertex_id, quality_limitation):
#     maxC = []
#
#     start = time.time()
#     for i in connected_graphs:
#
#         G_small, D = Refine(G.subgraph(i), q, target_vertex_id, quality_limitation)
#
#         for i in nx.weakly_connected_components(G_small):
#             D_i = {key: value for key, value in D.items() if key in i}
#             G_copy_i = G_small.subgraph(i)
#             if len(D_i) > quality_limitation:
#                 FS_i = calculate_fairness_score(D_i)
#                 if FS_i > theta:
#                     if len(maxC) == 0:
#                         maxC.append(G_copy_i)
#                         best_fairness_score = FS_i
#                     else:
#                         if FS_i < best_fairness_score:
#                             maxC.clear()
#                             maxC.append(G_copy_i)
#                             best_fairness_score = FS_i
#     print(str(time.time() - start) + "s")
#
#     return maxC


Amazon_Product = nx.read_gpickle('./Amazon_Product.gpickle')
print(len(Amazon_Product.nodes()))
print(len(Amazon_Product.edges()))



# q=nx.DiGraph()
# q.add_node(0, type="actor")
# q.add_node(1, type="movie")
# q.add_node(2, type="movie")
# # q.add_node(3, type="actor")
# # q.add_node(4, type="actor")
#
# q.add_edge(0, 1)
# q.add_edge(0, 2)
# # q.add_edge(3, 1)
# # q.add_edge(4, 1)
#
#
# v_t = 0; theta = 1; quality_limitation=10; best_fairness_score = 0
# # q_labels = nx.get_node_attributes(q, 'type')
#
# # maxC = EFS(IMDB, q, v_t, quality_limitation, theta)
# maxC = BaseLine(IMDB, q, v_t, quality_limitation, theta)
# print(maxC)
# start = time.time()
# S, D = generate_dictionary(q, IMDB, v_t)
# print(str(time.time() - start) + "s")


