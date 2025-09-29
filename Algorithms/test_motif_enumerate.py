import networkx as nx
from motif_enumerate.enumerate_motif_utils import CECIMatcher
# from openGraphMatching.utils import convert_graph, check_match_correctness
import time
from utils import generate_dictionary

# q = nx.DiGraph()
# q.add_nodes_from([
#     (0, {'feat': 'A'}),
#     (1, {'feat': 'A'}),
#     (2, {'feat': 'A'}),
#     (3, {'feat': 'A'}),
#     (4, {'feat': 'A'}),
#     (5, {'feat': 'A'}),
#     ])
# q.add_edges_from([
#     (0, 1),
#     (1, 2),
#     (2, 3),
#     (3, 4),
#     (4, 5),
#     (5, 0),
# ])
# G = nx.DiGraph()
# G.add_nodes_from([
#     (0, {'feat': 'A'}),
#     (1, {'feat': 'A'}),
#     (2, {'feat': 'A'}),
#     (3, {'feat': 'A'}),
#     (4, {'feat': 'A'}),
#     (5, {'feat': 'A'}),
#     (6, {'feat': 'A'}),
#     ])
# G.add_edges_from([
#     (0, 1),
#     (1, 2),
#     (2, 3),
#     (3, 4),
#     (4, 5),
#     (5, 0),
#     (1, 6),
#     (4, 6),
#     ])

G = nx.read_gpickle('./IMDB_undirected.gpickle')
# # G = nx.read_gpickle('./IMDB.gpickle')
# # print(G.nodes(data=True))
# # print("333")
#
q = nx.Graph()
#
q.add_node(1, feat="actor")
q.add_node(2, feat="movie")
# q.add_node(3, feat="movie")
# q.add_node(4, feat="actor")
# q.add_node(5, feat="actor")
#
q.add_edge(1, 2)
# q.add_edge(1, 3)
# q.add_edge(4, 2)
# q.add_edge(5, 2)

# The testing example
# target_graph_path = './dataset/hprd/data_graph/hprd.graph'
# query_folder_path = './dataset/hprd/query_graph/'
# query_file_name = 'query_dense_16_1.graph'
# G = convert_graph(target_graph_path)
# q = convert_graph(query_folder_path + query_file_name)


start = time.time()
m = CECIMatcher(G)
l = m.is_subgraph_match(q)
# for i in l:
#     print(i)

# generate_dictionary(q, G, 1)

print(str(time.time() - start) + " s")


print("-------------------------")
print("new enumerate")

q = nx.Graph()
#
q.add_node(1, feat="actor")
q.add_node(2, feat="movie")
q.add_node(3, feat="movie")
q.add_node(4, feat="actor")
q.add_node(5, feat="actor")
#
q.add_edge(1, 2)
q.add_edge(1, 3)
q.add_edge(4, 2)
q.add_edge(5, 2)

start = time.time()
m = CECIMatcher(G)
l = m.is_subgraph_match(q)
# for i in l:
#     print(i)

# generate_dictionary(q, G, 1)

print(str(time.time() - start) + " s")