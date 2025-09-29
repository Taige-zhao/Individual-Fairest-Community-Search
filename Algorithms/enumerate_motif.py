from typing import Dict, Generator, Hashable, List, Optional, Union, Tuple
from inspect import isclass
import itertools
from functools import lru_cache

import networkx as nx
# import psutil
import os
# from grandiso.queues import SimpleQueue
import random

__version__ = "2.1.1"

from SimpleQueue import SimpleQueue

@lru_cache()
def _is_node_attr_match(
        motif_node_id: str, host_node_id: str, motif: nx.Graph, host: nx.Graph
) -> bool:
    motif_node = motif.nodes[motif_node_id]
    host_node = host.nodes[host_node_id]

    for attr, val in motif_node.items():
        if attr not in host_node:
            return False
        if host_node[attr] != val:
            return False

    return True


@lru_cache()
def _is_node_structural_match(
        motif_node_id: str, host_node_id: str, motif: nx.Graph, host: nx.Graph
) -> bool:
    return host.degree(host_node_id) >= motif.degree(motif_node_id)


@lru_cache()
def _is_edge_attr_match(
        motif_edge_id: Tuple[str, str],
        host_edge_id: Tuple[str, str],
        motif: nx.Graph,
        host: nx.Graph,
) -> bool:
    motif_edge = motif.edges[motif_edge_id]
    host_edge = host.edges[host_edge_id]

    for attr, val in motif_edge.items():
        if attr not in host_edge:
            return False
        if host_edge[attr] != val:
            return False

    return True


def get_next_backbone_candidates(
        backbone: dict,
        motif: nx.Graph,
        host: nx.Graph,
        interestingness: dict,
        next_node: str = None,
        directed: bool = True,
        is_node_structural_match=_is_node_structural_match,
        is_node_attr_match=_is_node_attr_match,
        is_edge_attr_match=_is_edge_attr_match,
        isomorphisms_only: bool = False,
) -> List[dict]:
    if next_node is None and len(backbone) == 0:
        next_node = max(
            interestingness.keys(), key=lambda node: interestingness.get(node, 0.0)
        )
        return [
            {next_node: n}
            for n in host.nodes
            if is_node_attr_match(next_node, n, motif, host)
               and is_node_structural_match(next_node, n, motif, host)
        ]

    else:
        _nodes_with_greatest_backbone_count: List[str] = []
        _greatest_backbone_count = 0
        for motif_node_id in motif.nodes:
            if motif_node_id in backbone:
                continue
            if directed:
                motif_backbone_connections_count = sum(
                    [
                        1
                        for v in list(
                        set(motif.adj[motif_node_id]).union(
                            set(motif.pred[motif_node_id])
                        )
                    )
                        if v in backbone
                    ]
                )
            else:
                motif_backbone_connections_count = sum(
                    [1 for v in motif.adj[motif_node_id] if v in backbone]
                )
            if motif_backbone_connections_count > _greatest_backbone_count:
                _nodes_with_greatest_backbone_count.append(motif_node_id)
        next_node = max(
            _nodes_with_greatest_backbone_count,
            key=lambda node: interestingness.get(node, 0.0),
        )

    required_edges = []
    for other in list(motif.adj[next_node]):
        if other in backbone:
            # edge is (next_node, other)
            required_edges.append((None, next_node, other))
    if directed:
        for other in list(motif.pred[next_node]):
            if other in backbone:
                # edge is (other, next_node)
                required_edges.append((other, next_node, None))

    candidate_nodes = []
    if len(required_edges) == 1:
        # :(
        (source, _, target) = required_edges[0]
        if directed:
            if source is not None:
                # this is a "from" edge:
                candidate_nodes = list(host.adj[backbone[source]])
            elif target is not None:
                # this is a "from" edge:
                candidate_nodes = list(host.pred[backbone[target]])
        else:
            candidate_nodes = list(host.adj[backbone[target]])

    elif len(required_edges) > 1:
        candidate_nodes_set = set()
        for (source, _, target) in required_edges:
            if directed:
                if source is not None:
                    candidate_nodes_from_this_edge = host.adj[backbone[source]]
                else:
                    candidate_nodes_from_this_edge = host.pred[backbone[target]]
            else:
                candidate_nodes_from_this_edge = host.adj[backbone[target]]
            if len(candidate_nodes_set) == 0:
                candidate_nodes_set.update(candidate_nodes_from_this_edge)
            else:
                candidate_nodes_set = candidate_nodes_set.intersection(
                    candidate_nodes_from_this_edge
                )
        candidate_nodes = list(candidate_nodes_set)

    elif len(required_edges) == 0:
        raise ValueError(
            f"Somehow you found a motif node {next_node} that doesn't have "
            + "any motif-graph edges. This is bad. (Did you maybe pass an "
            + "empty backbone to this function?)"
        )

    tentative_results = [
        {**backbone, next_node: c}
        for c in candidate_nodes
        if c not in backbone.values()
           and is_node_attr_match(next_node, c, motif, host)
           and is_node_structural_match(next_node, c, motif, host)
    ]

    monomorphism_candidates = []

    for mapping in tentative_results:
        if len(mapping) == len(motif):
            if all(
                    [
                        host.has_edge(mapping[motif_u], mapping[motif_v])
                        and is_edge_attr_match(
                            (motif_u, motif_v),
                            (mapping[motif_u], mapping[motif_v]),
                            motif,
                            host,
                        )
                        for motif_u, motif_v in motif.edges
                    ]
            ):
                monomorphism_candidates.append(mapping)
        else:
            monomorphism_candidates.append(mapping)

    if not isomorphisms_only:
        return monomorphism_candidates

    isomorphism_candidates = []
    for result in monomorphism_candidates:
        for (motif_u, motif_v) in itertools.product(result.keys(), result.keys()):
            if not motif.has_edge(motif_u, motif_v) and host.has_edge(
                    result[motif_u], result[motif_v]
            ):
                break
        else:
            isomorphism_candidates.append(result)
    return isomorphism_candidates

# 对motif中每个节点的id都赋予一个 1，其中每个id是key，value是1
def uniform_node_interestingness(motif: nx.Graph) -> dict:
    return {n: 1 for n in motif.nodes}


def find_motifs_iter(
        motif: nx.Graph,
        host: nx.Graph,
        directed: bool = True,
        queue_=SimpleQueue,
        isomorphisms_only: bool = False,
        is_node_structural_match=_is_node_structural_match, # 作为一个函数传入，找如何match nodes
        is_node_attr_match=_is_node_attr_match, # 作为一个函数传入，函数就是找这个node attr是不是match的
        is_edge_attr_match=_is_edge_attr_match, # 作为一个函数传入，找如何match edges attributes
) -> Generator[dict, None, None]:
    interestingness = uniform_node_interestingness(motif) # # 对motif中每个节点的id都赋予一个 1，其中每个id是key，value是1

    q = queue_() if isclass(queue_) else queue_ # 先进先出
    q_1 = queue_() if isclass(queue_) else queue_  # 先进先出, 只是所有target vertex的集合

    next_candidate_backbones = get_next_backbone_candidates(
        {},
        motif,
        host,
        interestingness,
        directed=directed,
        isomorphisms_only=isomorphisms_only,
        is_node_structural_match=is_node_structural_match,
        is_node_attr_match=is_node_attr_match,
        is_edge_attr_match=is_edge_attr_match,
    )

    for candidate in next_candidate_backbones:
        if len(candidate) == len(motif):
            yield candidate
        else:
            q_1.put(candidate)

    # size = q_1.qsize()

    while not q.empty() or not q_1.empty():

        if q.empty():
            new_backbone = q_1.get()
        else:
            new_backbone = q.get()

        # if (size - q_1.qsize()) % int(size / 100) == 0:
        #     print("Have enumerate " + str((size - q_1.qsize()) / q_1.qsize()) + "% target nodes.")
        # print(new_backbone)
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
        # print(next_candidate_backbones)
        for candidate in next_candidate_backbones:
            if len(candidate) == len(motif):
                yield candidate
            else:
                q.put(candidate)
