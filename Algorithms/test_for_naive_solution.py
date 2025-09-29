import numpy as np
import time

from typing import Dict, Generator, Hashable, List, Optional, Union, Tuple

import networkx as nx
import random
from navie_enumeration import Refine
__version__ = "2.1.1"

from enumerate_motif import _is_node_attr_match, _is_node_structural_match, _is_edge_attr_match, find_motifs_iter

def gini_coefficient(x):
    diffsum = 0
    x = np.array(x)
    for i, xi in enumerate(x[:-1], 1):
        diffsum += np.sum(np.abs(xi - x[i:]))
    return diffsum / (len(x) ** 2 * np.mean(x))


def calculate_fairness_score(D):
    return gini_coefficient(list(D.values()))


def navie_enumeration(G, C, q, FS, theta, target_vertex_id,
                      target_vertex_label_number_in_G):  # C是一个存了target vertex instance的set
    global maxC;
    global now_existing_target_vertex_number;
    global count;
    global time_start

    count = count + 1
    if count % 10 == 0:
        print("processed " + str(count) + " enumerations.")

    if (now_existing_target_vertex_number < target_vertex_label_number_in_G):

        print(FS)
        print(target_vertex_label_number_in_G)
        print(now_existing_target_vertex_number)
        print(len(G.nodes()))
        print("------------")

        if len(C) != 0:
            v = random.sample(C, 1)

            G_copy = G.subgraph(set(G.nodes()) - set(v))
            G_copy, D_copy = Refine(G_copy, q, target_vertex_id)

            for i in nx.weakly_connected_components(G_copy):
                D_i = {key: value for key, value in D_copy.items() if key in i}
                G_copy_i = G_copy.subgraph(i)
                if len(D_i) > now_existing_target_vertex_number and len(D_i) > 1:
                    FS_i = calculate_fairness_score(D_i)
                    C_i = C - (set(G.nodes()) - set(G_copy_i.nodes()))
                    if FS_i > theta:
                        navie_enumeration(G_copy_i, C_i, q, FS_i, theta, target_vertex_id, len(D_i))
                    else:
                        if len(maxC) == 0:
                            maxC.append(G_copy_i)
                            now_existing_target_vertex_number = len(D_i)
                        else:
                            if now_existing_target_vertex_number < len(D_i):
                                maxC.clear()
                                maxC.append(G_copy_i)
                                now_existing_target_vertex_number = len(D_i)
            navie_enumeration(G, C - set(v), q, FS, theta, target_vertex_id, target_vertex_label_number_in_G)


def baseline(G, q, target_vertex_id, theta):
    random.seed(1)
    G, D = Refine(G, q, target_vertex_id)
    global maxC;
    global now_existing_target_vertex_number;
    global count;
    global time_start
    for i in nx.weakly_connected_components(G):
        D_i = {key: value for key, value in D.items() if key in i}
        if now_existing_target_vertex_number < len(D_i) and len(D_i) > 1:
            FS = calculate_fairness_score(D_i)
            if FS > theta:
                G_i = G.subgraph(i)
                C_i = set(D_i.keys())
                navie_enumeration(G_i, C_i, q, FS, theta, target_vertex_id, len(C_i))
            else:
                if len(maxC) == 0:
                    maxC.append(G_i)
                    now_existing_target_vertex_number = len(D_i)
                else:
                    if now_existing_target_vertex_number < len(D_i):
                        maxC.clear()
                        maxC.append(G_i)
                        now_existing_target_vertex_number = len(D_i)