from utils import get_q_neighbor_count, get_BFS_order, NLF, get_neighbor_of_query_vertex_with_small_index, generate_candidate_set, quality_filter, adv_generate_dictionary_of_target_vertex_instance
import networkx as nx
from utils import *
import time
import psutil
import sys


# G = nx.read_gpickle('../DBLP.gpickle')
#
#
# q=nx.DiGraph()
#
# q.add_node(0, type="author")
# q.add_node(1, type="paper")
# # q.add_node(2, type="paper")
# q.add_node(3, type="author")
# # q.add_node(4, type="author")
#
# q.add_edge(0, 1)
# q.add_edge(3, 1)
#
# quality_limitation = 10
#
# target_vertex_id = 0;
#
# taget_vertex_label = nx.get_node_attributes(q, "type")[target_vertex_id]
# graph_label = nx.get_node_attributes(G, "type")
# unvisited_vertices_with_target_type = [i for i in G.nodes() if graph_label[i] == taget_vertex_label]
#
# start = time.time()
# S, D = generate_dictionary_of_target_vertex_instance(q, G, target_vertex_id, unvisited_vertices_with_target_type)
# print("Normal enumerate is: " + str( time.time() - start))
#
# start = time.time()
# S_, D_ = adv_generate_dictionary_of_target_vertex_instance(q, G, target_vertex_id, unvisited_vertices_with_target_type)
# print("adv enumerate is: " + str( time.time() - start))
#
# print(S == S_)
# print(D == D_)

def Adv_BaseLine_test_memory(G, q, target_vertex_id, quality_limitation):

    taget_vertex_label = nx.get_node_attributes(q, "type")[target_vertex_id]
    graph_label = nx.get_node_attributes(G, "type")
    unvisited_vertices_with_target_type = [i for i in G.nodes() if graph_label[i] == taget_vertex_label]

    D = dict()
    M_graph = nx.DiGraph()
    N_R = set()

    while len(unvisited_vertices_with_target_type) > 0:
        N_R_, D_ = generate_dictionary_of_target_vertex_instance(q, G, target_vertex_id,
                                                                 unvisited_vertices_with_target_type)
        D.update(D_)
        N_R.update(N_R_)

        M_graph = nx.DiGraph()
        M_graph.add_edges_from(N_R)
        G.remove_nodes_from((set(unvisited_vertices_with_target_type) - set(D.keys())))

        V_D = set(M_graph.nodes()) - set( D.keys() )

        UV = set()
        for i in V_D:
            UV.update( set(M_graph.pred[i].keys() ))
        unvisited_vertices_with_target_type = UV

        M_graph.remove_nodes_from(V_D)
        N_R = set(M_graph.edges())

        N_R = N_R - set(M_graph.out_edges(unvisited_vertices_with_target_type))
        for i in unvisited_vertices_with_target_type:
            if i in D:
                D.pop(i)

    maxC = []; best_fairness_score = 1

    total_var_memory = ( sys.getsizeof(N_R) + sys.getsizeof(M_graph) + \
                       sys.getsizeof(unvisited_vertices_with_target_type) + \
                       sys.getsizeof(UV) + sys.getsizeof(V_D) + sys.getsizeof(D) \
                       + sys.getsizeof(D_) + sys.getsizeof(N_R_)) / 1024 / 1024
    a = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
    for i in nx.weakly_connected_components(M_graph):
        D_i = {key: value for key, value in D.items() if key in i}
        if len(D_i) > quality_limitation:
            FS_i = calculate_fairness_score(D_i)
            # print("Score is: " + str(FS_i))
            # print(D_i)
            if len(maxC) == 0:
                maxC.append(list(i))
                best_fairness_score = FS_i

            else:
                if FS_i < best_fairness_score:
                    maxC.clear()
                    maxC.append(list(i))
                    best_fairness_score = FS_i
    memory = (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024) - a + total_var_memory
    print("Total Memory used: " + str( memory ))


    return D, M_graph, maxC, best_fairness_score, memory




def EFS_test_memory(G, q, target_vertex_id, quality_limitation):

    a = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
    connected_graphs = propagation_based_filter(G, q, quality_limitation, target_vertex_id)
    memory_temp = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 - a
    maxC = []; best_fairness_score = 1; best_score = -1

    print("333333")
    print(memory_temp)

    start = time.time()

    D_ = None; M_graph = None; maxC_ = None
    for i in connected_graphs:
        D_, M_graph, maxC_, best_score = Adv_BaseLine(i, q, target_vertex_id, quality_limitation)

        if len(maxC) == 0:
            maxC = maxC_
            best_fairness_score = best_score

        else:
            if best_score < best_fairness_score:
                maxC.clear()
                maxC = maxC_
                best_fairness_score = best_score

    total_var_memory = (( sys.getsizeof(D_) + sys.getsizeof(M_graph) + \
                        sys.getsizeof(maxC_) ) / 1024 / 1024 ) + memory_temp

    print("Total Memory used: " + str( total_var_memory ))

    return maxC, best_score, time.time() - start, total_var_memory