import os
import copy
import glob
import shutil

import numpy as np
from utils import get_BFS_order, generate_candidate_set, generate_motif, select_motif, Adv_BaseLine
import time
import random

# from  navie_enumeration import generate_dictionary, calculate_fairness_score
from utils import count_target_vertex_instance_number_in_community, EFS, generate_dictionary, propagation_based_filter
from Advance_enumeration import max_Out_and_In_edge_hops, Advanced_Refine
import psutil
# import ssl
# ssl.match_hostname = lambda cert, hostname: True

import networkx as nx
from collections import Counter

start = time.time()
Amazon = nx.read_gpickle('../Amazon_Product_divided.gpickle')
# Amazon = nx.read_gpickle('../IMDB.gpickle')

q, target_vertex_id, target_type = select_motif(Amazon, 7)

quality_limitation = 10

print("loading graph: time " + str(time.time() - start) + "s")

print("Now loaded memory: " + str(psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024) + " GB")

# print(target_vertex_id)

nx.write_gpickle(q,'../toy_q_with7nodes_Amazon.gpickle') # 1659s; 353s, 172s
# q = nx.read_gpickle('../toy_q_Amazon.gpickle') # target_vertex_id = 974433

start = time.time()
Adv_BaseLine(Amazon, q, target_vertex_id, 10, 0.6)
print("Enumeration Time: " + str(time.time() - start) + "s")


start = time.time()
EFS(Amazon, q, target_vertex_id, 10, 0.6)
print("EFS Time: " + str(time.time() - start) + "s")