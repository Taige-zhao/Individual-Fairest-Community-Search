import time

import networkx as nx
# from grandiso.queues import SimpleQueue
import random

__version__ = "2.1.1"

from navie_enumeration import calculate_fairness_score, generate_dictionary
from Advance_enumeration import max_Out_and_In_edge_hops, Advanced_Refine
import numpy as np

count = 0;
maxC = [];
now_existing_target_vertex_number = 0
time_start = time.time()

def lower_bound(x, n):  # x=array, size,
    x.sort()
    m = len(x)
    D = n - m
    C = np.sum([(i + 1) * n for i, n in enumerate(x)])
    sum_x = sum(x)

    return (2 * (D * (1 + D) * np.min(x) / 2 + D * sum_x + C)) / (n * (sum_x + D * np.max(x))) - ((n + 1) / n)


def divide_graph(G, percent):
    random.seed(1)
    G_nodes = G.nodes()
    node_number = int(len(G_nodes) * percent)

    return G.subgraph(random.sample(G_nodes, node_number)).copy()


def Filter_search(G, C, D, q, FS, theta, target_vertex_id, motif_hops, target_vertex_label_number_in_G):
    global maxC;
    global now_existing_target_vertex_number;
    global count;
    global time_start

    count = count + 1
    # if count %  == 0 and count > 2000:
    if count % 1000 == 0:
        print("processed " + str(count) + " enumerations. Time: " + str(time.time() - time_start))

    if (now_existing_target_vertex_number < target_vertex_label_number_in_G):
        #         print(FS)
        #         print(target_vertex_label_number_in_G)
        #         print(now_existing_target_vertex_number)
        # #         print(len(G.nodes()))
        #         print("------------")

        if len(C) != 0:
            v = random.sample(C, 1)
            D_c = D.copy()
            delete = D_c.pop(v[0])

            s = time.time()
            lb = lower_bound(list(D_c.values()), len(D))
            e = time.time()

            # count = count + 1
            # # if count %  == 0 and count > 2000:
            # if count % 100 == 0:
            #     print("processed " + str(count) + " enumerations. Time: " + str(time.time() - time_start))
                # print(lb)
                # print(FS)
                # print(target_vertex_label_number_in_G)
                # print(now_existing_target_vertex_number)
                # # print("lower bound calculate time: " + str(e-s))
                # print(D.values())
                # print(delete)

            if lb < theta:
                G_copy, D_copy = Advanced_Refine(G, D_c, q, target_vertex_id, motif_hops)
                for i in nx.weakly_connected_components(G_copy):
                    D_i = {key: value for key, value in D_copy.items() if key in i}
                    G_copy_i = G_copy.subgraph(i)

                    if len(D_i) > 1 and len(D_i) > now_existing_target_vertex_number:
                        FS_i = calculate_fairness_score(D_i)
                        C_i = C - (set(G.nodes()) - set(G_copy_i.nodes()))
                        if FS_i > theta:
                            Filter_search(G_copy_i, C_i, D_i, q, FS_i, theta, target_vertex_id, motif_hops,
                                          len(D_i))
                        else:
                            if len(maxC) == 0:
                                maxC.append(G_copy)
                                now_existing_target_vertex_number = len(D_copy)
                            else:
                                if now_existing_target_vertex_number < len(D_copy):
                                    maxC.clear()
                                    maxC.append(G_copy)
                                    now_existing_target_vertex_number = len(D_copy)
            else:
                Filter_search(G.subgraph(list(G.nodes()).remove(v[0])), C - set(v), D_c, q, FS, theta, target_vertex_id,
                              motif_hops, len(D_c))
            Filter_search(G, C - set(v), D, q, FS, theta, target_vertex_id, motif_hops,
                          target_vertex_label_number_in_G)


def Filter_search_algorithm(G, q, target_vertex_id, theta):

    random.seed(1)
    S, D = generate_dictionary(q, G, target_vertex_id)
    G_small = G.subgraph(S)
    motif_hops = max_Out_and_In_edge_hops(q, target_vertex_id)
    G_small, D_small = Advanced_Refine(G_small, D, q, target_vertex_id, motif_hops)

    global maxC;
    global now_existing_target_vertex_number

    for i in nx.weakly_connected_components(G_small):
        G_small = G.subgraph(i)
        D_i = {key: value for key, value in D.items() if key in i}
        if now_existing_target_vertex_number < len(D_i) and len(D_i) > 1:
            FS_small = calculate_fairness_score(D_i)
            if FS_small > theta:
                C_small = set(D_i.keys())
                Filter_search(G_small, C_small, D_i, q, FS_small, theta, target_vertex_id, motif_hops, len(C_small))
            else:
                if len(maxC) == 0:
                    maxC.append(G_small)
                    now_existing_target_vertex_number = len(D_i)
                else:
                    if now_existing_target_vertex_number < len(D_i):
                        maxC.clear()
                        maxC.append(G_small)
                        now_existing_target_vertex_number = len(D_i)

    time_end = time.time()
    if len(maxC) != 0:
        print(maxC[0].nodes())
    else:
        print("There is no community founded")
    print("time cost: ", time_end - time_start, "s")



# processed 1000 enumerations. Time: 11.476636409759521
# processed 2000 enumerations. Time: 25.39538812637329
# processed 3000 enumerations. Time: 50.185911893844604
# processed 4000 enumerations. Time: 71.06921911239624
# processed 5000 enumerations. Time: 79.47395777702332
# processed 6000 enumerations. Time: 99.53101944923401
# processed 7000 enumerations. Time: 111.81000351905823
# processed 8000 enumerations. Time: 116.11179757118225
# processed 9000 enumerations. Time: 123.01148128509521
# processed 10000 enumerations. Time: 145.30136966705322
# processed 11000 enumerations. Time: 160.1974000930786
# processed 12000 enumerations. Time: 164.7069857120514
# processed 13000 enumerations. Time: 183.48052310943604
# processed 14000 enumerations. Time: 204.41306471824646
# processed 15000 enumerations. Time: 219.42077589035034
# processed 16000 enumerations. Time: 243.82589745521545
# processed 17000 enumerations. Time: 256.75899171829224
# processed 18000 enumerations. Time: 283.1043598651886
# processed 19000 enumerations. Time: 287.4744505882263
# processed 20000 enumerations. Time: 291.8507614135742
# processed 21000 enumerations. Time: 296.22646713256836
# processed 22000 enumerations. Time: 302.37818670272827
# processed 23000 enumerations. Time: 306.7663507461548
# processed 24000 enumerations. Time: 317.00023221969604
# processed 25000 enumerations. Time: 324.7651138305664
# processed 26000 enumerations. Time: 329.07760190963745
# processed 27000 enumerations. Time: 333.8134694099426
# processed 28000 enumerations. Time: 338.1169810295105
# processed 29000 enumerations. Time: 356.50399255752563
# processed 30000 enumerations. Time: 379.93986201286316