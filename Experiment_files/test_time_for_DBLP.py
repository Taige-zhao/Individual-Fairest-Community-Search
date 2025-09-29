import networkx as nx
import numpy as np
import time
from utils import generate_dictionary
from utils import generate_dictionary_of_target_vertex_instance
from utils import Baseline, Adv_BaseLine, EFS, select_motif

DBLP = nx.read_gpickle('../DBLP.gpickle')

motifs = []
q=nx.DiGraph()

q.add_node(0, type="author")
q.add_node(1, type="paper")
q.add_node(2, type="paper")
q.add_node(3, type="author")
q.add_node(4, type="author")

q.add_edge(0, 1)
q.add_edge(0, 2)
q.add_edge(3, 2)
q.add_edge(4, 2)

motifs.append(q)


q=nx.DiGraph()

q.add_node(0, type="author")
q.add_node(1, type="paper")
q.add_node(2, type="paper")
q.add_node(3, type="author")
q.add_node(4, type="author")

q.add_edge(0, 1)
q.add_edge(0, 2)
q.add_edge(3, 2)
q.add_edge(4, 1)

motifs.append(q)


q=nx.DiGraph()

q.add_node(0, type="author")
q.add_node(1, type="paper")
q.add_node(2, type="author")
q.add_node(3, type="author")
q.add_node(4, type="author")

q.add_edge(0, 1)
q.add_edge(2, 1)
q.add_edge(3, 1)
q.add_edge(4, 1)

motifs.append(q)


q=nx.DiGraph()

q.add_node(0, type="author")
q.add_node(1, type="paper")
q.add_node(2, type="paper")
q.add_node(3, type="paper")
q.add_node(4, type="author")

q.add_edge(0, 1)
q.add_edge(0, 2)
q.add_edge(0, 3)
q.add_edge(4, 1)

motifs.append(q)


q=nx.DiGraph()

q.add_node(0, type="author")
q.add_node(1, type="paper")
q.add_node(2, type="paper")
q.add_node(3, type="author")
q.add_node(4, type="author")

q.add_edge(0, 1)
q.add_edge(0, 2)
q.add_edge(3, 1)
q.add_edge(3, 2)
q.add_edge(4, 1)
q.add_edge(4, 2)

motifs.append(q)


number_of_motifs = 5
time_list_baseline = []
time_list_EFS = []
for i in range(0, number_of_motifs):
    print("Doing " + str(i))
    start_itr = time.time()
    q = motifs[i]
    target_vertex_id = 0

    start = time.time()
    D_, M_graph, maxC, best_score = Adv_BaseLine(DBLP, q, target_vertex_id, 10, 0.6)
    time_list_baseline.append(time.time() - start)

    maxC_, best_score_, time_EFS = EFS(DBLP, q, target_vertex_id, 10, 0.6)
    time_list_EFS.append(time_EFS)

    print("Cost " + str(time.time() - start_itr))

print("Baseline average time is: " + str(sum(time_list_baseline)/len(time_list_baseline)))

print("EFS average time is: " + str(sum(time_list_EFS)/len(time_list_EFS)))




