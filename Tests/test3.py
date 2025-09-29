import networkx as nx
import numpy as np
import time
from AAN_search import generate_AAN
test=nx.DiGraph()

test.add_node(1, type="author")
test.add_node(2, type="author")
test.add_node(3, type="author")
test.add_node(4, type="author")
test.add_node(5, type="paper")
test.add_node(6, type="paper")
test.add_node(7, type="paper")
test.add_node(8, type="paper")
test.add_node(9, type="paper")
test.add_node(10, type="paper")
test.add_node(11, type="paper")

test.add_edge(1, 5)
test.add_edge(2, 5)
test.add_edge(2, 6)
test.add_edge(3, 6)
test.add_edge(3, 7)
test.add_edge(4, 7)
test.add_edge(4, 8)
test.add_edge(4, 9)
test.add_edge(4, 10)
test.add_edge(4, 11)

a = nx.get_node_attributes(test, "type")
# print(a)

test_motif=nx.DiGraph()

test_motif.add_node(1, type="author")
test_motif.add_node(2, type="paper")
test_motif.add_node(3, type="paper")

test_motif.add_edge(1, 2)
test_motif.add_edge(1, 3)

time_start = time.time()
maxC = []; now_existing_target_vertex_number = 0; count = 0

generate_AAN(test_motif, test, 1)

time_end = time.time()
# print(maxC[0].nodes())


print("time cost: ", time_end - time_start, "s")