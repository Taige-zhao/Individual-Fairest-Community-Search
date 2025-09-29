import time
import networkx as nx
import numpy as np
import psutil
import os
import random

divided_percent = 0.5

start = time.time()
node_list_with_label = np.load('./Amazon_Product_node_label_list.npy', allow_pickle=True)
edge_tuple = np.load('./Amazon_Product_edge_tuple.npy', allow_pickle=True)
print("Time: " + str(time.time() - start))

print(len(node_list_with_label))
print(node_list_with_label[0:5])
# print(len(edge_tuple))

random.seed(1)
node_number = int(len(node_list_with_label) * divided_percent)
index = random.sample([i for i in range(0, len(node_list_with_label))], node_number)

node_list_with_label = node_list_with_label[index]

node_list = set([i[0] for i in node_list_with_label])

print(len(node_list_with_label))

divided_edge_tuple = []
for i in edge_tuple:
    if i[0] in node_list and i[1] in node_list:
        divided_edge_tuple.append(i)


print("Now loaded memory: " + str(psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024) + " GB")
#
Amazon_Product = nx.DiGraph()
Amazon_Product.add_nodes_from(node_list_with_label)

print("Now loaded memory: " + str(psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024) + " GB")
#
Amazon_Product.add_edges_from(divided_edge_tuple)
#
print("Now loaded memory: " + str(psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024) + " GB")
# #
nx.write_gpickle(Amazon_Product,'./Amazon_Product_divided_0_5.gpickle')