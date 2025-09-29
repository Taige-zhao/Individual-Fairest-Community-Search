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
def get_Follower(G, D, q, target_vertex_id, delete_nodes, motif_hops):
    nodes_delete = get_nodes_in_hops(G, delete_nodes, motif_hops) # 得到删除点周围motif的nodes，因为这些点可能会被删除
    G_small = G.subgraph(list(set(nodes_delete) - set(delete_nodes))) # 得到删除点周围motif的和target vertex 一样的nodes，因为这些点可能会被删除
    G_temp = G.subgraph(set(G.nodes()) - set(delete_nodes)) # 除去delete的子图
    followers = set(get_vertices_with_target_vertex_label_in_graph(G_small, q, target_vertex_id)) # 得到删除点周围motif的和target vertex 一样的nodes，因为这些点可能会被删除
    S_small, D_small = generate_dictionary_of_target_vertex_instance(q, G_temp, target_vertex_id, followers)

    delete_nodes = followers - set(D_small.keys())

    D_temp = D.copy()
    for i in list(D_small.keys()):
        D_temp[i] = D_small[i]
    for i in delete_nodes:
        D_temp.pop(i)

    nodes_set = (set(G_temp.nodes()) - set(nodes_delete)).union(S_small)
    G_temp = G_temp.subgraph(nodes_set)

    return G_temp, D_temp, delete_nodes


def Advanced_Refine(G, D, q, target_vertex_id, motif_hops):
    taget_vertex_label = nx.get_node_attributes(q, "type")[target_vertex_id]
    graph_label = nx.get_node_attributes(G, "type")
    S_with_target_vertex_label = [i for i in G.nodes() if graph_label[i] == taget_vertex_label]

    vertex_with_zero_participation = set(S_with_target_vertex_label) - set(D.keys())
    G, D, delete_nodes = get_Follower(G, D, q, target_vertex_id, vertex_with_zero_participation, motif_hops)

    while len(delete_nodes) != 0:
        G, D, delete_nodes = get_Follower(G, D, q, target_vertex_id, delete_nodes, motif_hops)

    return G, D



def greedy_algorithm(G, q, target_vertex_id, theta):
    random.seed(1)
    S, D = generate_dictionary(q, G, target_vertex_id)
    G_small = G.subgraph(S)
    motif_hops = max_Out_and_In_edge_hops(q, target_vertex_id)
    G_small, D_small = Advanced_Refine(G_small, D, q, target_vertex_id, motif_hops)

    maxC = [];
    now_existing_target_vertex_number = 0;
    enumerate_count = 0;
    time_start = time.time()

    for i in nx.weakly_connected_components(G_small):
        G_small_i = G.subgraph(i)   #存储目前找到的最好的community
        D_i = {key: value for key, value in D.items() if key in i}  #存储目前最好community的 D
        FS_small = calculate_fairness_score(D_i)    #存储目前最好的community的 fairness score

        if (now_existing_target_vertex_number < len(D_i)):
            if FS_small > theta:
                candidate_vertices = list(D_i.keys())

                while len(candidate_vertices) > 1 and len(candidate_vertices) > now_existing_target_vertex_number: # greedy，直到community只剩两个或者已经找到最好的 后，停止
                    maxC_temp_max = None    #存储本次迭代中最好的community
                    D_temp_max = None   #存储本次迭代中最好community的 D
                    FS_small_temp_max = 1

                    for v in candidate_vertices:

                        enumerate_count = enumerate_count + 1
                        if enumerate_count % 200 == 0:
                            print("processed " + str(enumerate_count) + " enumerations. Time: " + str(
                                time.time() - time_start))

                        D_i_temp = D_i.copy()
                        D_i_temp.pop(v)
                        G_temp, D_temp, delete_nodes = get_Follower(G_small_i, D_i_temp, q, target_vertex_id, [v], motif_hops)

                        while len(delete_nodes) != 0: #这里有问题 这里已经refine 完 delete一个节点后会变成什么样子
                            G_temp, D_temp, delete_nodes = get_Follower(G_temp, D_temp, q, target_vertex_id, delete_nodes, motif_hops)

                        if sum([1 for _ in nx.weakly_connected_components(G_temp)]) == 1 and len(D_temp) > now_existing_target_vertex_number and len(D_temp) > 1:
                            FS_temp = calculate_fairness_score(D_temp)

                            if FS_temp < theta:
                                if len(maxC) == 0:
                                    maxC.append(G_temp)
                                    now_existing_target_vertex_number = len(D_temp)
                                else:
                                    if now_existing_target_vertex_number < len(D_temp):
                                        maxC.clear()
                                        maxC.append(G_temp)
                                        now_existing_target_vertex_number = len(D_temp)
                                maxC_temp_max = G_temp
                                D_temp_max = D_temp
                                FS_small_temp_max = FS_temp
                            else:
                                if FS_temp < FS_small_temp_max:
                                    maxC_temp_max = G_temp
                                    D_temp_max = D_temp
                                    FS_small_temp_max = FS_temp

                    if D_temp_max != None:
                        candidate_vertices = list(D_temp_max.keys())
                        G_small_i = maxC_temp_max
                        D_i = D_temp_max
                    else:
                        candidate_vertices = []
                    # print(len(D_temp))
                    print(FS_small_temp_max)

    if len(maxC) > 0:
        print(len(maxC[0].nodes))
        print("Existing target vertex number: " + str(now_existing_target_vertex_number))
    else:
        print("No community found!")