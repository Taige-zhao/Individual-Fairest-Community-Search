import sys
import math
import time
import networkx as nx
from Advance_enumeration import Advanced_algorithm, generate_dictionary, max_Out_and_In_edge_hops, Advanced_Refine, calculate_fairness_score
from fliter_enumeration import divide_graph
import numpy as np
import psutil
from utils import generate_motif
import random

print("2")
print("start")
# IMDB = nx.read_gpickle('./IMDB.gpickle')
# IMDB = nx.read_gpickle('./DBLP.gpickle')
IMDB = nx.read_gpickle('./Amazon_Product.gpickle')
# IMDB = nx.read_gpickle('./Amazon_Product.gpickle')
IMDB_motif = nx.DiGraph()

average_time = []

for i in range(5, 8):
    motifs = generate_motif(IMDB, i, 2)
    time_array = []
    count = 1
    for IMDB_motif in motifs:
        start = time.time()
        target_vertex_id = random.sample(IMDB_motif.nodes(), 1)[0]
        S, D = generate_dictionary(IMDB_motif, IMDB, target_vertex_id)
        if len(S) != 0:
            subgraph = IMDB.subgraph(S).copy()
            # np.save("./DBLP_motif_6_nodes_original_dic.npy", D)
            # nx.write_gpickle(subgraph,'./DBLP_motif_6_nodes_original_community.gpickle')
            motif_hops = max_Out_and_In_edge_hops(IMDB_motif, target_vertex_id)
            G_small, D_small = Advanced_Refine(subgraph, D, IMDB_motif, target_vertex_id, motif_hops)

            maxC = None
            FS_max = 1
            for i in nx.weakly_connected_components(G_small):
                if len(i) >= 2:
                    D_i = {key: value for key, value in D.items() if key in i}
                    FS_small = calculate_fairness_score(D_i)
                    if FS_small < FS_max:
                        maxC = D_i
                        FS_max = FS_small

            print("finish enumeration " + str(count) + ", time: " + str(time.time() - start) )
            time_array.append(time.time() - start)
            count = count + 1
            nx.write_gpickle(IMDB_motif,'./Amazon_Product_motif_' + str(count) + '.gpickle')

    print("Average Time: " + str(np.average(time_array)))
    average_time.append(np.average(time_array))

print(average_time)

# This motif can be processed.
# This process loading: 10.192119598388672 GB, Total momery is:93.08795166015625 GB, maximal 10^4 times.
# IMDB_motif.add_node(0, type="paper")
# IMDB_motif.add_node(1, type="paper")
# IMDB_motif.add_node(2, type="paper")
# IMDB_motif.add_node(3, type="paper")
# IMDB_motif.add_node(4, type="paper")
# IMDB_motif.add_node(5, type="field_of_study")
#
# IMDB_motif.add_edge(0, 1)
# IMDB_motif.add_edge(0, 5)
# IMDB_motif.add_edge(1, 5)
# IMDB_motif.add_edge(2, 5)
# IMDB_motif.add_edge(3, 5)
# IMDB_motif.add_edge(4, 5)

# IMDB_motif.add_node(0, type="author")
# IMDB_motif.add_node(1, type="author")
# IMDB_motif.add_node(2, type="author")
# IMDB_motif.add_node(3, type="author")
# IMDB_motif.add_node(4, type="author")
# IMDB_motif.add_node(5, type="author")
# IMDB_motif.add_node(6, type="institution")
#
# IMDB_motif.add_edge(0, 6)
# IMDB_motif.add_edge(1, 6)
# IMDB_motif.add_edge(2, 6)
# IMDB_motif.add_edge(3, 6)
# IMDB_motif.add_edge(4, 6)
# IMDB_motif.add_edge(5, 6)

#
# start = time.time()
# print("start enumeration motif instance with vertex number = 6 in motif...")
# generate_dictionary(IMDB_motif, IMDB, target_vertex_id)
# print("finish enumeration" + str(time.time() - start))

# IMDB = nx.read_gpickle('./OGB_MAG.gpickle')
# # IMDB = nx.read_gpickle('./IMDB.gpickle')
# # IMDB = divide_graph(IMDB, 0.03)
# start = time.time()
# target_vertex_id = 0
# # a = nx.weakly_connected_components(IMDB)
#
# target_vertex_id = 0
# IMDB_motif = nx.DiGraph()
#
# IMDB_motif.add_node(0, type="author")
# IMDB_motif.add_node(1, type="paper")
# IMDB_motif.add_node(2, type="paper")
# IMDB_motif.add_node(3, type="paper")
# # IMDB_motif.add_node(4, type="paper")
# # IMDB_motif.add_node(5, type="paper")
#
# IMDB_motif.add_edge(0, 1)
# IMDB_motif.add_edge(0, 2)
# IMDB_motif.add_edge(0, 3)
# # IMDB_motif.add_edge(0, 4)
# # IMDB_motif.add_edge(0, 5)
#
# generate_dictionary(IMDB_motif, IMDB, target_vertex_id)
# for i in nx.weakly_connected_components(IMDB):
#     if len(i) > 2000:
#         subgraph = IMDB.subgraph(i).copy()
#         nx.write_gpickle(subgraph,'./test.gpickle')
#         print(len(subgraph.nodes()))
#         print("finish load graph")
#         print((time.time() - start))
#
#         target_vertex_id = 0
#         IMDB_motif = nx.DiGraph()
#
#         IMDB_motif.add_node(0, type="author")
#         IMDB_motif.add_node(1, type="paper")
#         IMDB_motif.add_node(2, type="paper")
#         IMDB_motif.add_node(3, type="author")
#         IMDB_motif.add_node(4, type="author")
#         IMDB_motif.add_node(5, type="author")
#
#         IMDB_motif.add_edge(0, 1)
#         IMDB_motif.add_edge(0, 2)
#         IMDB_motif.add_edge(3, 2)
#         IMDB_motif.add_edge(4, 2)
#         IMDB_motif.add_edge(5, 2)
#
#         start = time.time()
#         print("start enumeration motif instance with vertex number = 6 in motif...")
#         # S, D = generate_dictionary(IMDB_motif, IMDB, target_vertex_id)
#         # D = generate_dictionary(IMDB_motif, IMDB, target_vertex_id)
#         generate_dictionary(IMDB_motif, subgraph, target_vertex_id)
#         # print("finish enumeration, start refine")
#         print("finish enumeration" + str(time.time() - start))
#
# print("Finish find community")


# print("start")
# start = time.time()
# IMDB = IMDB.copy()
# print("finish copying graph")

# IMDB_motif=nx.DiGraph()
# IMDB_motif.add_node(0, type="actor")
# IMDB_motif.add_node(1, type="movie")
# IMDB_motif.add_node(2, type="movie")
# IMDB_motif.add_node(3, type="actor")
# IMDB_motif.add_node(4, type="actor")
# IMDB_motif.add_node(5, type="actor")


# IMDB_motif.add_node(0, type="author")
# IMDB_motif.add_node(1, type="paper")
# IMDB_motif.add_node(2, type="paper")
# IMDB_motif.add_node(3, type="author")


# IMDB_motif.add_edge(0, 1)
# IMDB_motif.add_edge(0, 2)
# IMDB_motif.add_edge(3, 2)
# IMDB_motif.add_edge(3, 2)
# IMDB_motif.add_edge(4, 2)
# IMDB_motif.add_edge(5, 2)
#
# generate_dictionary(IMDB_motif, IMDB, target_vertex_id)

# start = time.time()

# print("start enumeration motif instance...")
# target_vertex_id = 0

# graph_label = nx.get_node_attributes(IMDB, "type")
# taget_vertex_label = nx.get_node_attributes(IMDB_motif, "type")[target_vertex_id]
# labels_in_graph = [i[0] for i in graph_label.items() if i[1] == taget_vertex_label]

# S, D = generate_dictionary(IMDB_motif, IMDB, target_vertex_id)
# D = generate_dictionary(IMDB_motif, IMDB, target_vertex_id)
# print("finish enumeration, start refine")
# print("finish enumeration" + str(time.time() - start) )
# subgraph = IMDB.subgraph( IMDB.nodes() - (set(labels_in_graph) - set(D.keys()) )).copy()

# subgraph = IMDB.subgraph(S).copy()
# np.save("OGB_MAG_motif_3_nodes_original_dic.npy", D)
# nx.write_gpickle(subgraph,'./OGB_MAG_motif_3_nodes_original_community.gpickle')


# start = time.time()
# S, D = generate_dictionary(IMDB_motif, subgraph, target_vertex_id)
# G_small = IMDB.subgraph(S)
# S, D = generate_dictionary(IMDB_motif, G_small, target_vertex_id)
# motif_hops = max_Out_and_In_edge_hops(IMDB_motif, target_vertex_id)
# G_small, D_small = Advanced_Refine(G_small, D, IMDB_motif, target_vertex_id, motif_hops)
#

# print((time.time() - start) )
# print("finish refine")
# print((time.time() - start) )


# IMDB_motif.add_node(0, type="actor")
# IMDB_motif.add_node(1, type="movie")
# IMDB_motif.add_node(2, type="movie")
# IMDB_motif.add_node(3, type="actor")
# IMDB_motif.add_node(4, type="actor")


# IMDB_motif.add_node(0, type="author")
# IMDB_motif.add_node(1, type="paper")
# IMDB_motif.add_node(2, type="author")
# IMDB_motif.add_node(3, type="author")
# IMDB_motif.add_node(4, type="author")
# IMDB_motif.add_node(5, type="author")
#
#
#
# IMDB_motif.add_edge(0, 1)
# IMDB_motif.add_edge(2, 1)
# IMDB_motif.add_edge(3, 1)
# IMDB_motif.add_edge(4, 1)
# IMDB_motif.add_edge(5, 1)

# target_vertex_id = 0
# IMDB_motif=nx.DiGraph()
#
# IMDB_motif.add_node(0, type="author")
# IMDB_motif.add_node(1, type="paper")
# IMDB_motif.add_node(2, type="paper")
# IMDB_motif.add_node(3, type="author")
# IMDB_motif.add_node(4, type="author")
# IMDB_motif.add_node(5, type="author")
#
# IMDB_motif.add_edge(0, 1)
# IMDB_motif.add_edge(0, 2)
# IMDB_motif.add_edge(3, 2)
# IMDB_motif.add_edge(4, 2)
# IMDB_motif.add_edge(5, 2)
#
# start = time.time()
# print("start enumeration motif instance with vertex number = 6 in motif...")
# # S, D = generate_dictionary(IMDB_motif, IMDB, target_vertex_id)
# # D = generate_dictionary(IMDB_motif, IMDB, target_vertex_id)
# generate_dictionary(IMDB_motif, IMDB, target_vertex_id)
# # print("finish enumeration, start refine")
# print("finish enumeration" + str(time.time() - start) )
# subgraph = IMDB.subgraph( IMDB.nodes() - (set(labels_in_graph) - set(D.keys()) )).copy()
#
# subgraph = IMDB.subgraph(S).copy()
# np.save("OGB_MAG_motif_4_nodes_original_dic.npy", D)
# nx.write_gpickle(subgraph,'./OGB_MAG_motif_4_nodes_original_community.gpickle')











# author_to_paper = dataset[0][("author", "to", "paper")]["edge_index"].tolist()
# paper_to_author = dataset[0][("paper", "to", "author")]["edge_index"].tolist()
# paper_to_term = dataset[0][("paper", "to", "term")]["edge_index"].tolist()
# paper_to_conference = dataset[0][("paper", "to", "conference")]["edge_index"].tolist()
# term_to_paper = dataset[0][("term", "to", "paper")]["edge_index"].tolist()
# conference_to_paper = dataset[0][("conference", "to", "paper")]["edge_index"].tolist()
#
# author_id = set(author_to_paper[0] + paper_to_author[1])
# paper_id = set([i + len(author_id) for i in (author_to_paper[1] + paper_to_author[0] + paper_to_term[0] + paper_to_conference[0] + term_to_paper[1] + conference_to_paper[1]) ])
# term_id = set( [i + len(author_id) + len(paper_id) for i in (paper_to_term[1] + term_to_paper[0])])
# conference_id = set( [i + len(author_id) + len(paper_id) + len(term_id) for i in (paper_to_conference[1] + conference_to_paper[0])])
#
# node_label_list = []
#
# for i in author_id:
#     node_label_list.append((i, {"type": "author"}))
#
# for i in paper_id:
#     node_label_list.append((i, {"type": "paper"}))
#
# for i in term_id:
#     node_label_list.append((i, {"type": "term"}))
#
# for i in conference_id:
#     node_label_list.append((i, {"type": "conference"}))
# #
# edges = [author_to_paper[0] + [i + len(author_id) for i in paper_to_author[0]] + [i + len(author_id) for i in paper_to_term[0]] + [i + len(author_id) for i in paper_to_conference[0]] + [i + len(author_id) + len(paper_id) for i in term_to_paper[0]] + [i + len(author_id) + len(paper_id) + len(term_id) for i in conference_to_paper[0]],
#          [i + len(author_id) for i in author_to_paper[1]] + paper_to_author[1] + [i + len(author_id) + len(paper_id) for i in paper_to_term[1]] + [i + len(author_id) + len(paper_id) + len(term_id) for i in paper_to_conference[1]] + [i + len(author_id) for i in term_to_paper[1]] + [i + len(author_id) for i in conference_to_paper[1]]]
#
# edge_tuple = []
# for i in range(np.array(edges).shape[1]):
#     edge_tuple.append((edges[0][i], edges[1][i]))
#
# DBLP=nx.DiGraph()
# DBLP.add_nodes_from(node_label_list)
# DBLP.add_edges_from(edge_tuple)
#
# nx.write_gpickle(DBLP,'/Users/taigezhao/Desktop/Data/DBLP/DBLP.gpickle')
