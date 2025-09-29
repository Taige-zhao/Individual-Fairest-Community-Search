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
from typing import Dict, Generator, Hashable, List, Optional, Union, Tuple

# q_1 = SimpleQueue() if isclass(SimpleQueue) else SimpleQueue  # 先进先出, 只是所有target vertex的集合
# q_1.put({})
# q_1.put({})
# print(q_1.qsize())

import networkx as nx
from utils import generate_motif, count_target_vertex_instance_number_in_community

IMDB=nx.DiGraph()

IMDB.add_node(10, type="paper")
IMDB.add_node(11, type="paper")
IMDB.add_node(12, type="paper")
IMDB.add_node(13, type="paper")
IMDB.add_node(14, type="paper")
IMDB.add_node(15, type="paper")
IMDB.add_node(16, type="paper")
IMDB.add_node(3, type="author")
IMDB.add_node(6, type="author")
IMDB.add_node(5, type="author")
IMDB.add_node(1, type="author")
IMDB.add_node(2, type="author")
IMDB.add_node(4, type="author")
IMDB.add_node(7, type="author")


IMDB.add_edge(1, 10)
IMDB.add_edge(2, 10)
IMDB.add_edge(2, 11)
IMDB.add_edge(3, 11)
IMDB.add_edge(3, 12)
IMDB.add_edge(4, 11)
IMDB.add_edge(4, 12)
IMDB.add_edge(5, 13)
IMDB.add_edge(5, 14)
IMDB.add_edge(6, 13)
IMDB.add_edge(6, 14)
IMDB.add_edge(6, 15)
IMDB.add_edge(6, 16)
IMDB.add_edge(7, 15)
IMDB.add_edge(7, 16)

test_motif=nx.DiGraph()

test_motif.add_node(1, type="author")
test_motif.add_node(2, type="paper")
test_motif.add_node(3, type="author")

test_motif.add_edge(1, 2)
test_motif.add_edge(3, 2)

# count_target_vertex_instance_number_in_community(IMDB, test_motif, 1)
# motifs = generate_motif(IMDB, 4, 1)
#
# print(motifs[0].nodes())
# print(motifs[0].edges())

# nx.k_core()

Freebase = nx.read_gpickle('./Freebase.gpickle')

print(len(Freebase.edges()))