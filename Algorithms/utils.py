import numpy as np
import time

from typing import Dict, Generator, Hashable, List, Optional, Union, Tuple

import networkx as nx
# from grandiso.queues import SimpleQueue
import random
# import psutil
import os
from enumerate_motif import uniform_node_interestingness, get_next_backbone_candidates
from inspect import isclass

__version__ = "2.1.1"

from SimpleQueue import SimpleQueue
import copy

from enumerate_motif import _is_node_attr_match, _is_node_structural_match, _is_edge_attr_match
from collections import Counter
from navie_enumeration import calculate_fairness_score, generate_dictionary


def divide_graph(G, percent):
    random.seed(1)
    G_nodes = G.nodes()
    node_number = int(len(G_nodes) * percent)

    return G.subgraph(random.sample(G_nodes, node_number)).copy()

def count_target_vertex_instance_number_in_community(G, motif, target_vertex_id):
    graph_label = nx.get_node_attributes(G, "type")
    taget_vertex_label = nx.get_node_attributes(motif, "type")[target_vertex_id]
    vertices_id_with_target_type_in_graph = [i[0] for i in graph_label.items() if i[1] == taget_vertex_label]

    return len(vertices_id_with_target_type_in_graph)

def get_BFS_order(q, target_vertex_id):

    nodes = set(q.pred[target_vertex_id].keys()).union(set(q.adj[target_vertex_id].keys()))  # query node的下一层
    q = q.copy()
    q.remove_node(target_vertex_id) #原来的树删除
    should_break = False
    BFS_order = [target_vertex_id]

    while should_break == False:

        temp_nodes = set([t[0] for t in q.in_edges(nodes)]) | set([t[1] for t in q.out_edges(nodes)])

        BFS_order.extend(set(nodes) - set(BFS_order))
        if temp_nodes.issubset(nodes):
            should_break = True
        else:
            q.remove_nodes_from(nodes)
            nodes = temp_nodes

    dic = generate_candidate_set(BFS_order)

    return BFS_order, dic


def generate_candidate_set(query_vertex_list):
    dic = dict()

    for i in query_vertex_list:
        dic[i] = set()

    return dic


def get_neighbor_count(G, v, labels_of_G):

    in_neighbor_count = Counter([labels_of_G[n] for n in G.pred[v].keys()])
    out_neighbor_count = Counter([labels_of_G[n] for n in G.adj[v].keys()])

    return in_neighbor_count, out_neighbor_count

# {0: Counter(), 1: Counter({'author': 1}), 2: Counter({'author': 1, 'paper': 1}), 3: Counter({'paper': 1}), 4: Counter(), 5: Counter({'paper': 1}), 6: Counter({'paper': 1})}
def get_q_neighbor_count(q):
    q_labels = nx.get_node_attributes(q, 'type')
    in_neighbor_dict = dict()
    out_neighbor_dict = dict()
    for node in q.nodes():
        in_neighbor_dict[node], out_neighbor_dict[node] = get_neighbor_count(q, node, q_labels)

    return in_neighbor_dict, out_neighbor_dict



def NLF(G, v, u, in_neighbor_q, out_neighbor_q, labels_of_G):
    in_neighbor_count, out_neighbor_count = get_neighbor_count(G, v, labels_of_G)

    for l in in_neighbor_q[u].keys():
        if l in in_neighbor_count:
            if in_neighbor_q[u][l] > in_neighbor_count[l]:
                return False
        else:
            return False

    for l in out_neighbor_q[u].keys():
        if l in out_neighbor_count:
            if out_neighbor_q[u][l] > out_neighbor_count[l]:
                return False
        else:
            return False

    return True

def generate_motif(G, motif_number, quatity): # motif_number: motif内节点的数量； quatity：想生成多少个motif
    motifs = []
    nodes = G.nodes()
    for _ in range(0, quatity):
        start_node = random.sample(nodes, 1)[0]
        subgraph_nodes = set([start_node])
        subgraph_edges = set()
        count = 0

        while len(subgraph_nodes) < motif_number:
            count = count + 1

            if count > 50:
                start_node = random.sample(nodes, 1)[0]
                subgraph_nodes = set([start_node])
                subgraph_edges = set()
                count = 0
            else:
                graph_node = random.sample(subgraph_nodes, 1)[0]
                neighbors = set(G.pred[graph_node].keys()).union(set(G.adj[graph_node].keys()))
                if len(neighbors) != 0:
                    next_node = random.sample(neighbors, 1)[0]
                    if next_node not in subgraph_nodes:
                        subgraph_nodes.add(next_node)

                        if next_node in [i[1] for i in G.out_edges(graph_node)]:
                            subgraph_edges.add( (graph_node, next_node) )
                        else:
                            subgraph_edges.add( (next_node, graph_node) )
                else:
                    count = count + 100

        subgraph = G.edge_subgraph(subgraph_edges).copy()

        motifs.append( subgraph )

    return motifs


def select_motif(G, motif_num):

    motifs = generate_motif(G, motif_num, 100)

    while True:
        m = False
        for motif in motifs:
            type_with_more_than_one_vertex = [g[0] for g in Counter([i[1]["type"] for i in motif.nodes(data=True)] ).items() if g[1]>1]
            if len(type_with_more_than_one_vertex) > 0:
                target_vertex_type = type_with_more_than_one_vertex[0]
                for i in motif.nodes(data=True):
                    if i[1]["type"] == target_vertex_type:
                        target_vertex_id = i[0]
                        break
                return motif, target_vertex_id, target_vertex_type
        if m == False:
            motifs = generate_motif(G, motif_num, 100)


def find_motifs_iter(
        motif: nx.Graph,
        host: nx.Graph,
        interestingness: dict = None,
        directed: bool = None,
        queue_=SimpleQueue,
        isomorphisms_only: bool = False,
        hints: List[Dict[Hashable, Hashable]] = None,
        is_node_structural_match=_is_node_structural_match,
        is_node_attr_match=_is_node_attr_match,
        is_edge_attr_match=_is_edge_attr_match,
) -> Generator[dict, None, None]:
    interestingness = interestingness or uniform_node_interestingness(motif)
    if directed is None:
        # guess directedness from motif
        if isinstance(motif, nx.DiGraph):
            # This will be a directed query.
            directed = True
        else:
            directed = False

    q = queue_() if isclass(queue_) else queue_

    if hints is None or hints == []:
        q.put({})
    else:
        for hint in hints:
            q.put(hint)

    count = 0
    # total = psutil.virtual_memory().total / 1024 / 1024 / 1024
    while not q.empty():
        new_backbone = q.get()
        next_candidate_backbones = get_next_backbone_candidates(
            new_backbone,
            motif,
            host,
            interestingness,
            directed=directed,
            isomorphisms_only=isomorphisms_only,
            is_node_structural_match=is_node_structural_match,
            is_node_attr_match=is_node_attr_match,
            is_edge_attr_match=is_edge_attr_match,
        )

        count = count + 1
        # if count % 1000000 == 0:
            # a = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024
            # print("This process loading: " + str(a) + " GB, Total momery is:" + str(total) + " GB")
            # if a > 60:
            #     break

        for candidate in next_candidate_backbones:
            if len(candidate) == len(motif):
                yield candidate
            else:
                q.put(candidate)

    # print("Finish motif iter")

def generate_dictionary(
        motif: nx.Graph,
        host: nx.Graph,
        target_vertex_id: int,
        *args,
        count_only: bool = False,
        limit: int = None,
        is_node_attr_match=_is_node_attr_match,
        is_node_structural_match=_is_node_structural_match,
        is_edge_attr_match=_is_edge_attr_match,
        **kwargs,
) -> Union[int, List[dict]]:

    S = set()
    D = {}

    for qresult in find_motifs_iter(
            motif,
            host,
            *args,
            is_node_attr_match=is_node_attr_match,
            is_node_structural_match=is_node_structural_match,
            is_edge_attr_match=is_edge_attr_match,
            **kwargs,
    ):

        result = qresult
        S.update(result.values())
        if result[target_vertex_id] in D.keys():
            D[result[target_vertex_id]] = D[result[target_vertex_id]] + 1
        else:
            D[result[target_vertex_id]] = 1

    return S, D


def quality_filter(G, S, candidate_set, k, G_labels, v_t_label, v_t):
    G = G.edge_subgraph(list(S))
    connected_graph = []

    for g in nx.weakly_connected_components(G):
        if len( set([n for n in g if G_labels[n] == v_t_label]).intersection(candidate_set[v_t]) ) >= k:
            connected_graph.append(G.subgraph(g).copy())

    return connected_graph


def get_neighbor_of_query_vertex_with_small_index(q, v_t):
    BFS_order, candidate_set_q = get_BFS_order(q, v_t)
    for u in q.nodes:
        candidate_set_q[u] = list(set(BFS_order[:BFS_order.index(u)]).intersection(set([t[0] for t in q.in_edges(u)]) | set([t[1] for t in q.out_edges(u)])))

    return candidate_set_q


def propagation_based_filter(G, q, k, v_t): #返回一个 list,每个元素是一个子图

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
    connected_graphs = quality_filter(G, S, candidate_set_q, k, G_labels, q_labels[v_t], v_t)

    # backward progagtion

    # return S, candidate_set_q
    return connected_graphs


def Adv_BaseLine(G, q, target_vertex_id, quality_limitation):

    taget_vertex_label = nx.get_node_attributes(q, "type")[target_vertex_id]
    graph_label = nx.get_node_attributes(G, "type")
    unvisited_vertices_with_target_type = [i for i in G.nodes() if graph_label[i] == taget_vertex_label]

    D = dict()
    M_graph = nx.DiGraph()
    N_R = set()
    while len(unvisited_vertices_with_target_type) > 0:
        N_R_, D_ = generate_dictionary_of_target_vertex_instance(q, G, target_vertex_id, unvisited_vertices_with_target_type)
        D.update(D_)
        N_R.update(N_R_)
        # print(N_R)

        M_graph = nx.DiGraph()
        M_graph.add_edges_from(N_R)
        G.remove_nodes_from((set(unvisited_vertices_with_target_type) - set(D.keys())))

        V_D = set(M_graph.nodes()) - set( D.keys() )

        UV = set()
        for i in V_D:
            UV.update( set(M_graph.pred[i].keys() ))
        unvisited_vertices_with_target_type = UV

        M_graph.remove_nodes_from(V_D)
        N_R = set(M_graph.edges())

        N_R = N_R - set(M_graph.out_edges(unvisited_vertices_with_target_type))
        for i in unvisited_vertices_with_target_type:
            if i in D:
                D.pop(i)


    maxC = []; best_fairness_score = 1

    for i in nx.weakly_connected_components(M_graph):
        D_i = {key: value for key, value in D.items() if key in i}
        if len(D_i) > quality_limitation:
            FS_i = calculate_fairness_score(D_i)
            # print("Score is: " + str(FS_i))
            # print(D_i)
            if len(maxC) == 0:
                maxC.append(list(i))
                best_fairness_score = FS_i

            else:
                if FS_i < best_fairness_score:
                    maxC.clear()
                    maxC.append(list(i))
                    best_fairness_score = FS_i


    return D, M_graph, maxC, best_fairness_score



def add_attributes_to_vertices_in_graph(G, vertices):  # add 1:1 in attributes
    for i in vertices:
        nx.set_node_attributes(G, {i: {1: 1}})


def delete_attributes_to_vertices_in_graph(G, vertices):  # add 1:1 in attributes
    for i in vertices:
        del G.nodes[i][1]


def get_vertex_with_target_type_in_q_expect_target_vertex(q, target_vertex_id):
    taget_vertex_label = nx.get_node_attributes(q, "type")[target_vertex_id]
    graph_label = nx.get_node_attributes(q, "type")
    S_with_target_vertex_label = [i for i in q.nodes() if graph_label[i] == taget_vertex_label]

    return set(S_with_target_vertex_label) - set([target_vertex_id])


def generate_M_graph_edges(mapping_dic, vertex_with_target_type_in_q_expect_target_vertex, target_vertex_id):
    edge_list = []
    for i in vertex_with_target_type_in_q_expect_target_vertex:
        edge_list.append( (mapping_dic[target_vertex_id], mapping_dic[i]) )
    return edge_list


def generate_dictionary_of_target_vertex_instance(
        motif: nx.Graph,
        host: nx.Graph,
        target_vertex_id: int,
        target_vertex_instances: list,
        *args,
        count_only: bool = False,
        limit: int = None,
        is_node_attr_match=_is_node_attr_match,
        is_node_structural_match=_is_node_structural_match,
        is_edge_attr_match=_is_edge_attr_match,
        **kwargs,
) -> Union[int, List[dict]]:
    S = set();
    D = {}

    add_attributes_to_vertices_in_graph(motif, [target_vertex_id])
    add_attributes_to_vertices_in_graph(host, target_vertex_instances)
    set_of_vertex_with_target_type = get_vertex_with_target_type_in_q_expect_target_vertex(motif, target_vertex_id)

    for qresult in find_motifs_iter(
            motif,
            host,
            *args,
            is_node_attr_match=is_node_attr_match,
            is_node_structural_match=is_node_structural_match,
            is_edge_attr_match=is_edge_attr_match,
            **kwargs,
    ):
        result = qresult

        edges_in_M = generate_M_graph_edges(result, set_of_vertex_with_target_type, target_vertex_id)

        S.update(set(edges_in_M))
        if result[target_vertex_id] in D.keys():
            D[result[target_vertex_id]] = D[result[target_vertex_id]] + 1
        else:
            D[result[target_vertex_id]] = 1

    delete_attributes_to_vertices_in_graph(motif, [target_vertex_id])
    delete_attributes_to_vertices_in_graph(host, target_vertex_instances)

    return S, D


def adv_generate_dictionary_of_target_vertex_instance(
        motif: nx.Graph,
        host: nx.Graph,
        target_vertex_id: int,
        target_vertex_instances: list,
        *args,
        count_only: bool = False,
        limit: int = None,
        is_node_attr_match=_is_node_attr_match,
        is_node_structural_match=_is_node_structural_match,
        is_edge_attr_match=_is_edge_attr_match,
        **kwargs,
) -> Union[int, List[dict]]:
    S = set();
    D = {}

    add_attributes_to_vertices_in_graph(motif, [target_vertex_id])
    print(motif.nodes(data=True))
    set_of_vertex_with_target_type = get_vertex_with_target_type_in_q_expect_target_vertex(motif, target_vertex_id)

    for id in target_vertex_instances:
        add_attributes_to_vertices_in_graph(host, [id])
        for qresult in find_motifs_iter(
                motif,
                host,
                *args,
                is_node_attr_match=is_node_attr_match,
                is_node_structural_match=is_node_structural_match,
                is_edge_attr_match=is_edge_attr_match,
                **kwargs,
        ):
            result = qresult

            edges_in_M = generate_M_graph_edges(result, set_of_vertex_with_target_type, target_vertex_id)

            S.update(set(edges_in_M))
            if result[target_vertex_id] in D.keys():
                D[result[target_vertex_id]] = D[result[target_vertex_id]] + 1
            else:
                D[result[target_vertex_id]] = 1

        delete_attributes_to_vertices_in_graph(host, [id])

    return S, D



def EFS(G, q, target_vertex_id, quality_limitation):

    connected_graphs = propagation_based_filter(G, q, quality_limitation, target_vertex_id)
    maxC = []; best_fairness_score = 1; best_score = -1

    start = time.time()
    for i in connected_graphs:
        D_, M_graph, maxC_, best_score = Adv_BaseLine(i, q, target_vertex_id, quality_limitation)

        if len(maxC) == 0:
            maxC = maxC_
            best_fairness_score = best_score

        else:
            if best_score < best_fairness_score:
                maxC.clear()
                maxC = maxC_
                best_fairness_score = best_score
    # print("Time of EFS: " + str(time.time() - start) + "s")

    return maxC, best_score, time.time() - start


# def Baseline(G, q, target_vertex_id, quality_limitation, fairness_thresholds): # 不用 M-graph
#
#     D = dict()
#     NF = True
#
#     taget_vertex_label = nx.get_node_attributes(q, "type")[target_vertex_id]
#     graph_label = nx.get_node_attributes(G, "type")
#
#     while NF == True:
#
#         S, D = generate_dictionary(q, G, target_vertex_id)
#         S_ = [i for i in S if graph_label[i] == taget_vertex_label]
#
#         graph_label = nx.get_node_attributes(G, "type")
#         vertices_id_with_target_type_in_graph = [i[0] for i in graph_label.items() if i[1] == taget_vertex_label]
#
#         if len(S_) == len(D.keys()):
#             NF = False
#         else:
#             G.remove_nodes_from(set(vertices_id_with_target_type_in_graph) - set(D.keys()))
#
#     G_temp = G.subgraph(S).copy()
#     maxC = []; best_fairness_score = 1
#
#     for i in nx.weakly_connected_components(G_temp):
#         D_i = {key: value for key, value in D.items() if key in i}
#         if len(D_i) > quality_limitation:
#             FS_i = calculate_fairness_score(D_i)
#             # print("Score is: " + str(FS_i))
#             # print(D_i)
#             if FS_i < fairness_thresholds:
#                 if len(maxC) == 0:
#                     maxC.append(list(D_i.keys()))
#                     best_fairness_score = FS_i
#
#                 else:
#                     if FS_i < best_fairness_score:
#                         maxC.clear()
#                         maxC.append(list(D_i.keys()))
#                         best_fairness_score = FS_i
#
#
#     return S_, D, maxC, best_fairness_score

def calculate_r_degree(M_graph):
    degrees = [i[1] for i in M_graph.degree()]
    result = Counter(degrees)

    # print(degrees)
    # print(result)

    # print(result.keys())
    # print(result.values())

    x = list(result.keys())
    x.sort()
    y = [result[i] for i in x]
    yy = [i/sum(y)*100 for i in y]

    # print(result)
    print("------------")
    print(x)
    print(yy)

    return x, yy



def Find_t_communities_using_baseline_(G, q, target_vertex_id, quality_limitation): # 不用 M-graph

    taget_vertex_label = nx.get_node_attributes(q, "type")[target_vertex_id]
    graph_label = nx.get_node_attributes(G, "type")
    unvisited_vertices_with_target_type = [i for i in G.nodes() if graph_label[i] == taget_vertex_label]

    D = dict()
    M_graph = nx.DiGraph()
    N_R = set()
    while len(unvisited_vertices_with_target_type) > 0:
        N_R_, D_ = generate_dictionary_of_target_vertex_instance(q, G, target_vertex_id, unvisited_vertices_with_target_type)
        D.update(D_)
        N_R.update(N_R_)
        # print(N_R)

        M_graph = nx.DiGraph()
        M_graph.add_edges_from(N_R)
        G.remove_nodes_from((set(unvisited_vertices_with_target_type) - set(D.keys())))

        V_D = set(M_graph.nodes()) - set( D.keys() )

        UV = set()
        for i in V_D:
            UV.update( set(M_graph.pred[i].keys() ))
        unvisited_vertices_with_target_type = UV

        M_graph.remove_nodes_from(V_D)
        N_R = set(M_graph.edges())

        N_R = N_R - set(M_graph.out_edges(unvisited_vertices_with_target_type))
        for i in unvisited_vertices_with_target_type:
            if i in D:
                D.pop(i)

    communities_fairness_score = [];

    print("Number of t-communities")
    count = 0
    for i in nx.weakly_connected_components(M_graph):

        D_i = {key: value for key, value in D.items() if key in i}
        if len(D_i) > quality_limitation:
            count = count + 1
            FS_i = calculate_fairness_score(D_i)
            communities_fairness_score.append(FS_i)
    print(count)

    return list(np.sort(communities_fairness_score))