import networkx as nx

from collections import Counter
from utils import count_target_vertex_instance_number_in_community, EFS, BaseLine, propagation_based_filter
# Test q
q=nx.DiGraph()
q.add_node(0, type="A")
q.add_node(1, type="B")
q.add_node(2, type="C")
# q.add_node(3, type="C")


q.add_edge(0, 1)
q.add_edge(2, 1)
# q.add_edge(1, 2)
# q.add_edge(3, 1)
# q.add_edge(3, 2)



# Test data graph

IMDB = nx.DiGraph()
IMDB.add_node(1, type="A")
IMDB.add_node(2, type="A")
IMDB.add_node(3, type="A")
IMDB.add_node(4, type="C")
IMDB.add_node(5, type="B")
IMDB.add_node(6, type="B")
IMDB.add_node(7, type="C")
IMDB.add_node(8, type="B")
IMDB.add_node(9, type="C")
IMDB.add_node(10, type="B")
IMDB.add_node(11, type="C")
IMDB.add_node(12, type="C")
IMDB.add_node(13, type="C")
IMDB.add_node(14, type="C")
IMDB.add_node(15, type="C")

IMDB.add_edge(1, 4)
IMDB.add_edge(1, 5)
IMDB.add_edge(1, 6)
IMDB.add_edge(1, 7)
IMDB.add_edge(1, 8)
IMDB.add_edge(2, 8)
IMDB.add_edge(2, 9)
IMDB.add_edge(10, 2)
IMDB.add_edge(3, 10)
IMDB.add_edge(3, 11)
IMDB.add_edge(4, 5)
IMDB.add_edge(6, 7)
IMDB.add_edge(8, 7)
IMDB.add_edge(8, 9)
IMDB.add_edge(10, 11)

IMDB.add_edge(12, 4)
IMDB.add_edge(12, 5)
IMDB.add_edge(12, 6)
IMDB.add_edge(13, 7)
IMDB.add_edge(13, 8)
IMDB.add_edge(6, 13)
IMDB.add_edge(14, 8)
IMDB.add_edge(14, 9)
IMDB.add_edge(14, 10)
IMDB.add_edge(15, 9)
IMDB.add_edge(15, 11)

v_t=0; quality_limitation=1; theta=1

# maxC = BaseLine(IMDB, q, v_t, quality_limitation, theta)
# maxC = EFS(IMDB, q, v_t, quality_limitation, theta)
graph = propagation_based_filter(IMDB, q, 1, v_t)
# print(maxC)
print(graph)