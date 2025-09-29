import networkx as nx
import numpy as np
import time
from utils import generate_dictionary
from utils import generate_dictionary_of_target_vertex_instance
from utils import Baseline, Adv_BaseLine, EFS, select_motif, divide_graph, generate_motif

DBLP = nx.read_gpickle('../../DBLP.gpickle')

number_of_motifs = 1
motifs = []
for _ in range(0, number_of_motifs):
    q, target_vertex_id, target_type = select_motif(DBLP, 5)
    # q = nx.DiGraph()

    # q.add_node(0, type="author")
    # q.add_node(1, type="paper")
    # # q.add_node(2, type="paper")
    # q.add_node(3, type="author")
    # # q.add_node(4, type="author")
    #
    # q.add_edge(0, 1)
    # # q.add_edge(0, 2)
    # q.add_edge(3, 1)
    # target_vertex_id = 0
    motifs.append((q, target_vertex_id))


print("Finish generate motif")


time_list_EFS = []
divide_adv = []

for i in range(0, number_of_motifs):
    print("Doing " + str(i))
    start_itr = time.time()
    q = motifs[i][0]
    target_vertex_id = motifs[i][1]

    start = time.time()
    D_, M_graph, maxC, best_score = Adv_BaseLine(DBLP, q, target_vertex_id, 10, 0.6)

    divide_adv.append(time.time() - start)

    # maxC_, best_score_, time_EFS = EFS(DBLP, q, target_vertex_id, 10, 0.6)
    # time_list_EFS.append(time_EFS)

print("Baseline average time is: " + str(sum(divide_adv)/len(divide_adv)))
# print("EFS average time is: " + str(sum(time_list_EFS)/len(time_list_EFS)))




