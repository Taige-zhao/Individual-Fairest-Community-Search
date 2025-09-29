import numpy as np
import time

from typing import Dict, Generator, Hashable, List, Optional, Union, Tuple

import networkx as nx
# from grandiso.queues import SimpleQueue
import random

__version__ = "2.1.1"

from SimpleQueue import SimpleQueue

from enumerate_motif import _is_node_attr_match, _is_node_structural_match, _is_edge_attr_match, find_motifs_iter
from navie_enumeration import calculate_fairness_score, generate_dictionary

count = 0; maxC = []; now_existing_target_vertex_number = 0
time_start = time.time()

def get_vertices_with_target_vertex_label_in_graph(G, q, target_vertex_id):
    graph_label = nx.get_node_attributes(G, "type")
    taget_vertex_label = nx.get_node_attributes(q, "type")[target_vertex_id]
    return [i[0] for i in graph_label.items() if i[1] == taget_vertex_label]


def max_Out_and_In_edge_hops(q, target_vertex_id):
    nodes = set([x for t in q.in_edges(target_vertex_id) for x in t]) | set([x for t in q.out_edges(target_vertex_id)
                                                                             for x in t])
    should_break = False
    hops = 0

    while should_break == False:
        hops = hops + 1
        temp_in_edges = set([x for t in q.in_edges(nodes) for x in t])
        temp_out_edges = set([x for t in q.out_edges(nodes) for x in t])

        if (temp_in_edges | temp_out_edges).issubset(nodes):
            should_break = True
        else:
            nodes = temp_in_edges | temp_out_edges
    return hops


def get_nodes_in_hops(G, delete_nodes, hops):
    nodes = set([x for t in G.in_edges(delete_nodes) for x in t]) | set([x for t in G.out_edges(delete_nodes)
                                                                         for x in t])
    next_nodes = nodes
    for _ in range(0, hops - 1):
        temp_in_edges = set([x for t in G.in_edges(next_nodes) for x in t])
        temp_out_edges = set([x for t in G.out_edges(next_nodes) for x in t])
        next_nodes = (temp_in_edges | temp_out_edges) - nodes
        nodes = nodes | temp_in_edges | temp_out_edges
    return nodes


def add_attributes_to_vertices_in_graph(G, vertices):  # add 1:1 in attributes
    for i in vertices:
        nx.set_node_attributes(G, {i: {1: 1}})


def delete_attributes_to_vertices_in_graph(G, vertices):  # add 1:1 in attributes
    for i in vertices:
        del G.nodes[i][1]


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
        S.update(list(result.values()))
        if result[target_vertex_id] in D.keys():
            D[result[target_vertex_id]] = D[result[target_vertex_id]] + 1
        else:
            D[result[target_vertex_id]] = 1

    delete_attributes_to_vertices_in_graph(motif, [target_vertex_id])
    delete_attributes_to_vertices_in_graph(host, target_vertex_instances)

    return S, D


# 输入graph和删除的nodes，把follower更新的dictionary输出，并给出是否还需要refine
# 1. 先获得 motif中 in degree的maximal hop和 out degree的maximal hop，然后拿到周围所有的顶点（这个可以通过AAN得到）。
def get_Follower(G, D, q, target_vertex_id, delete_nodes, motif_hops):

    nodes_delete = get_nodes_in_hops(G, delete_nodes, motif_hops)

    G_small = G.subgraph(list(set(nodes_delete) - set(delete_nodes)))
    G = G.subgraph(set(G.nodes()) - set(delete_nodes))
    followers = set(get_vertices_with_target_vertex_label_in_graph(G_small, q, target_vertex_id))
    S_small, D_small = generate_dictionary_of_target_vertex_instance(q, G, target_vertex_id, followers)
    delete_nodes = followers - set(D_small.keys())

    for i in list(D_small.keys()):
        D[i] = D_small[i]
    for i in delete_nodes:
        D.pop(i)

    nodes_set = (set(G.nodes()) - set(nodes_delete)).union(S_small)
    G = G.subgraph(nodes_set)

    return G, D, delete_nodes


def Advanced_Refine(G, D, q, target_vertex_id, motif_hops):
    taget_vertex_label = nx.get_node_attributes(q, "type")[target_vertex_id]
    graph_label = nx.get_node_attributes(G, "type")
    S_with_target_vertex_label = [i for i in G.nodes() if graph_label[i] == taget_vertex_label]

    vertex_with_zero_participation = set(S_with_target_vertex_label) - set(D.keys())
    G, D, delete_nodes = get_Follower(G, D, q, target_vertex_id, vertex_with_zero_participation, motif_hops)

    count = 0
    while len(delete_nodes) != 0:
        G, D, delete_nodes = get_Follower(G, D, q, target_vertex_id, delete_nodes, motif_hops)
        count = count + 1
        print("refined times: " + str(count))
    return G, D


def Advanced_enumeration(G, C, D, q, FS, theta, target_vertex_id, motif_hops, target_vertex_label_number_in_G):
    global maxC;
    global now_existing_target_vertex_number;
    global count;
    global time_start

    count = count + 1
    if count % 10 == 0:
        print("processed " + str(count) + " enumerations. Time: " + str(time.time() - time_start))

    if (now_existing_target_vertex_number < target_vertex_label_number_in_G):
        #         print(FS)
        #         print(target_vertex_label_number_in_G)
        #         print(now_existing_target_vertex_number)
        #         print(len(G.nodes()))
        #         print("------------")

        if len(C) != 0:
            v = random.sample(C, 1)
            D_c = D.copy()
            D_c.pop(v[0])
            G_copy, D_copy = Advanced_Refine(G, D_c, q, target_vertex_id, motif_hops)

            for i in nx.weakly_connected_components(G_copy):
                D_i = {key: value for key, value in D_copy.items() if key in i}
                G_copy_i = G_copy.subgraph(i)
                if len(D_i) > 1 and len(D_i) > now_existing_target_vertex_number:
                    FS_i = calculate_fairness_score(D_i)
                    C_i = C - (set(G.nodes()) - set(G_copy_i.nodes()))
                    if FS_i > theta:
                        Advanced_enumeration(G_copy_i, C_i, D_i, q, FS_i, theta, target_vertex_id, motif_hops,
                                             len(D_i))
                    else:
                        if len(maxC) == 0:
                            maxC.append(G_copy_i)
                            now_existing_target_vertex_number = len(D_i)
                        else:
                            if now_existing_target_vertex_number < len(D_i):
                                maxC.clear()
                                maxC.append(G)
                                now_existing_target_vertex_number = len(D_i)
            Advanced_enumeration(G, C - set(v), D, q, FS, theta, target_vertex_id, motif_hops,
                                 target_vertex_label_number_in_G)


def Advanced_algorithm(G, q, target_vertex_id, theta):
    random.seed(1)
    S, D = generate_dictionary(q, G, target_vertex_id)
    G_small = G.subgraph(S)
    motif_hops = max_Out_and_In_edge_hops(q, target_vertex_id)
    G_small, D_small = Advanced_Refine(G_small, D, q, target_vertex_id, motif_hops)

    global maxC;
    global now_existing_target_vertex_number;
    global count;
    global time_start

    for i in nx.weakly_connected_components(G_small):
        G_small_i = G.subgraph(i)
        D_i = {key: value for key, value in D.items() if key in i}
        FS_small = calculate_fairness_score(D_i)
        if FS_small > theta:
            C_small = set(D_i.keys())
            Advanced_enumeration(G_small_i, C_small, D_i, q, FS_small, theta, target_vertex_id, motif_hops,
                                 len(C_small))
        else:
            if len(maxC) == 0:
                maxC.append(G_small_i)
                now_existing_target_vertex_number = len(D_i)
            else:
                if now_existing_target_vertex_number < len(D_i):
                    maxC.clear()
                    maxC.append(G_small_i)
                    now_existing_target_vertex_number = len(D_i)

    print(maxC[0].nodes())
