import networkx as nx
import numpy as np
import time
from utils import *

def propagation_based_filter_test(G, q, k, v_t): #返回一个 list,每个元素是一个子图

    # forward progagtion
    in_neighbor_q, out_neighbor_q = get_q_neighbor_count(q)
    G_labels = nx.get_node_attributes(G, 'type')
    q_labels = nx.get_node_attributes(q, 'type')

    BFS_order, candidate_set_q = get_BFS_order(q, v_t); S = set() # Line 1
    C = [i for i in G.nodes() if NLF(G, i, v_t, in_neighbor_q, out_neighbor_q, G_labels) and G_labels[i] == q_labels[v_t]] # Line 2-3
    N_q = get_neighbor_of_query_vertex_with_small_index(q, v_t) # 得到 所有的 N_u_

    for hat_v in C: # Line 4
        S_ = set(); i_add = True

        temp_candidate_set_q = generate_candidate_set(BFS_order)
        temp_candidate_set_q[v_t] = set([hat_v])

        for u in BFS_order[1:]: # Line 6
            N_u_ = N_q[u]
            u_b = N_u_[0]

            for v in temp_candidate_set_q[u_b]: # Line 10
                v_set = set()

                # 对于新的候选点来说，0：既有in又有out；1：只有in （老点指向新点）；2：只有out
                if q.has_edge(u_b, u) and q.has_edge(u, u_b):
                    v_set = set(G.pred[v].keys()).intersection(set(G.adj[v].keys()))
                elif q.has_edge(u_b, u):
                    v_set = set(G.adj[v].keys())
                elif q.has_edge(u, u_b):
                    v_set = set(G.pred[v].keys())

                for v_ in [i for i in v_set if G_labels[i] == q_labels[u] and NLF(G, i, u, in_neighbor_q, out_neighbor_q, G_labels)]:
                    E_t = []; c_add = True
                    if q.has_edge(u_b, u):
                        E_t.append((v, v_))
                    if q.has_edge(u, u_b):
                        E_t.append((v_, v))

                    for hat_u in (set(N_u_)-set([u_b])): # Line 13
                        E_t_ = []  #后面这一块都是 Line 14
                        for v_bar in temp_candidate_set_q[hat_u]:
                            if q.has_edge(u, hat_u) and q.has_edge(hat_u, u) and G.has_edge(v_, v_bar) and G.has_edge(v_bar, v_):
                                E_t_.append((v_bar, v_), (v_, v_bar))
                            elif q.has_edge(u, hat_u) and G.has_edge(v_, v_bar):
                                E_t_.append((v_, v_bar))
                            elif q.has_edge(hat_u, u) and G.has_edge(v_bar, v_):
                                E_t_.append((v_bar, v_))

                        if len(E_t_) == 0: # Line 15
                            c_add = False; break # Line 16
                        else: # Line 17
                            E_t = E_t + E_t_

                    if c_add == True: # Line 18
                        S_ = S_.union(set(E_t)); temp_candidate_set_q[u].add(v_) # Line 19

            if len(temp_candidate_set_q[u]) == 0: # Line 20
                i_add = False; break

        if i_add == True:
            S = S.union(S_)
            for u in BFS_order:
                candidate_set_q[u] = candidate_set_q[u].union(temp_candidate_set_q[u])


    # quality filter
    mm = [0, 5, 10, 15, 20]

    for quality_limit in mm:
        connected_graphs = quality_filter(G, S, candidate_set_q, quality_limit, G_labels, q_labels[v_t], v_t)
        print("Doing FVA with motif size: " + str(len(q.nodes())) + ", and quality limit: " + str(quality_limit))
        count = 0
        for subgraph in connected_graphs:
            count = count + len([i for i in subgraph.nodes() if graph_label[i] == taget_vertex_label])


        print("FVA visited vertices: " + str(count))


# DBLP = nx.read_gpickle('../Amazon_Product.gpickle')
# DBLP = nx.read_gpickle('../DBLP.gpickle')
# DBLP = nx.read_gpickle('../IMDB.gpickle')
DBLP = nx.read_gpickle('../Freebase.gpickle')

# DBLP = divide_graph(DBLP, 0.2)

print(len(DBLP.nodes()))

for m in range(3,8):
    motifs = []
    q, target_vertex_id, target_type = select_motif(DBLP, m)
    motifs.append(q)

    number_of_motifs = len(motifs)

    for motif in range(0, number_of_motifs):
        print("Doing baseline with motif size: " + str(m) )

        q = motifs[motif]
        taget_vertex_label = nx.get_node_attributes(q, "type")[target_vertex_id]
        graph_label = nx.get_node_attributes(DBLP, "type")

        print("Baseline visited vertices: " + str(len([i for i in DBLP.nodes() if graph_label[i] == taget_vertex_label])))

        start_itr = time.time()
        propagation_based_filter_test(DBLP, q, None, target_vertex_id)
        print("Time used of propogation: " + str(time.time()-start_itr) + "s")


