import numpy as np
from navie_enumeration import gini_coefficient
import time
from collections import Counter

import networkx as nx

q=nx.DiGraph()
q.add_node(0, type="A")
q.add_node(1, type="B")
q.add_node(2, type="C")
q.add_node(3, type="C")


q.add_edge(0, 1)
q.add_edge(0, 2)
q.add_edge(1, 2)
q.add_edge(3, 1)
q.add_edge(3, 2)

# print( [g[0] for g in Counter([i[1]["type"] for i in q.nodes(data=True)] ).items() if g[1]>1] )

for i in q.nodes(data=True):
    print(i)