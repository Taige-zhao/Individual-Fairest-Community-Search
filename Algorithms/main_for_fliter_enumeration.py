import networkx as nx
import numpy as np
import time
from fliter_enumeration import Filter_search_algorithm
import sys
sys.setrecursionlimit(int(10e8))

# processed 1000 enumerations. Time: 14.936743974685669
# processed 2000 enumerations. Time: 745.7780938148499
# processed 3000 enumerations. Time: 15470.582703828812

IMDB = nx.read_gpickle('./IMDB.gpickle')

IMDB_motif=nx.DiGraph()

IMDB_motif.add_node(0, type="actor")
IMDB_motif.add_node(1, type="movie")
IMDB_motif.add_node(2, type="movie")

IMDB_motif.add_edge(0, 1)
IMDB_motif.add_edge(0, 2)

Filter_search_algorithm(IMDB, IMDB_motif, 0, 0.2)


