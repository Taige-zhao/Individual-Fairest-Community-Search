from utils import generate_candidate_set
import networkx as nx
from utils import count_target_vertex_instance_number_in_community, EFS, BaseLine, generate_dictionary, propagation_based_filter

test=nx.DiGraph()

test.add_node(1, type="author")
test.add_node(2, type="author")
test.add_node(10, type="paper")
test.add_node(11, type="paper")
# test.add_node(12, type="author")

test.add_edge(1, 10)
test.add_edge(1, 11)
test.add_edge(2, 11)
# test.add_edge(12, 11)


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

IMDB.add_node(17, type="paper")
IMDB.add_node(18, type="paper")
IMDB.add_node(8, type="author")
IMDB.add_node(9, type="author")


IMDB.add_edge(8, 17)
IMDB.add_edge(8, 18)
IMDB.add_edge(9, 17)
IMDB.add_edge(9, 18)

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

connected_graphs = propagation_based_filter(IMDB, test, 4, 1)

for i in connected_graphs:
    print(i)

