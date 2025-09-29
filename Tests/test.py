import time
import networkx as nx
import numpy as np
import psutil
import os
import random

start = time.time()
node_label_list = np.load('./Amazon_Product_node_label_list.npy', allow_pickle=True)
edge_tuple = np.load('./Amazon_Product_edge_tuple.npy', allow_pickle=True)
print("Time: " + str(time.time() - start))

print(len(node_label_list))
print(len(edge_tuple))

# edge_tuple_list = []
#
# for i in edge_tuple:
#     edge_tuple_list.append(tuple(i))
# a = np.random.randint(0, len(edge_tuple), int(len(edge_tuple)/2))
# edge_tuple = edge_tuple[a]
# print(len(edge_tuple))
#
print("Now loaded memory: " + str(psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024) + " GB")
#
Amazon_Product = nx.DiGraph()
Amazon_Product.add_nodes_from(node_label_list)

print("Now loaded memory: " + str(psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024) + " GB")
#
Amazon_Product.add_edges_from(edge_tuple)
# #
print("Now loaded memory: " + str(psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024) + " GB")
# #
nx.write_gpickle(Amazon_Product,'./Amazon_Product.gpickle')