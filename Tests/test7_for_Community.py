import numpy as np
import time

from typing import Dict, Generator, Hashable, List, Optional, Union, Tuple

import networkx as nx
# from grandiso.queues import SimpleQueue
import random

__version__ = "2.1.1"

from SimpleQueue import SimpleQueue
from networkx.exception import NetworkXError

from enumerate_motif import _is_node_attr_match, _is_node_structural_match, _is_edge_attr_match, find_motifs_iter
from navie_enumeration import calculate_fairness_score, generate_dictionary
import os
from navie_enumeration import gini_coefficient


def vertex_id_with_the_same_type_of_target_vertex_except_target_vertex_in_motif(motif, target_vertex_id):
    graph_label = nx.get_node_attributes(motif, "type")
    taget_vertex_label = nx.get_node_attributes(motif, "type")[target_vertex_id]
    target_label_except_target_vertex_in_motif = [i[0] for i in graph_label.items() if i[1] == taget_vertex_label]
    # print(target_label_except_target_vertex_in_motif)
    target_label_except_target_vertex_in_motif.remove(target_vertex_id)

    return target_label_except_target_vertex_in_motif

def generate_AAN_and_refined_graphs(
        motif: nx.Graph,
        host: nx.Graph,
        # target_vertex_id: int,
        # file_name: str,
        *args,
        count_only: bool = False,
        limit: int = None,
        is_node_attr_match=_is_node_attr_match,
        is_node_structural_match=_is_node_structural_match,
        is_edge_attr_match=_is_edge_attr_match,
        **kwargs,
) -> Union[int, List[dict]]:

    # path = "./"+file_name+".gpickle"
    #
    # if not os.path.exists(path):

    # print("Not exist stored graph, generating...")

    # target_label_except_target_vertex_in_motif = vertex_id_with_the_same_type_of_target_vertex_except_target_vertex_in_motif(motif, target_vertex_id)

    edge_set = set()

    # AAN_node_dic = {}
    # AAN_edge_dic = {}

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

        # if result[target_vertex_id] in node_dic:
        #     node_dic[result[target_vertex_id]] = node_dic[result[target_vertex_id]] + 1
        # else:
        #     node_dic[result[target_vertex_id]] = 1

        # for i in target_label_except_target_vertex_in_motif:
        #     if (result[i], result[target_vertex_id]) in edge_dic:
        #         edge_dic[(result[i], result[target_vertex_id])] = edge_dic[
        #                                                               (result[i], result[target_vertex_id])] + 1
        #     else:
        #         edge_dic[(result[i], result[target_vertex_id])] = 1

        for edges in motif.edges():
            edge_set.add((result[edges[0]], result[edges[1]]))

    # graph = nx.DiGraph()
    # graph.add_nodes_from(node_dic.keys())
    # nx.set_node_attributes(graph, node_dic, "weight")

    # weighted_edges_list = [(k[0], k[1], v) for k, v in edge_dic.items()]
    #
    # graph.add_weighted_edges_from(weighted_edges_list)

    #     nx.write_gpickle(graph, path)
    #
    #     print("Finish Generate AAN")
    # else:
    #     print("Exist a stored graph")
    #     graph = nx.read_gpickle(path)

    subgraph = host.edge_subgraph(edge_set)

    return subgraph