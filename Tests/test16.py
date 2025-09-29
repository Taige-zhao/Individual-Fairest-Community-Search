
# a = [1,2,3,4,5]
#
# s_m = 3
#
# def dev(a):
#     return ( 2 * (a.index(s_m) + 1) - 1 ) * sum(a) - sum([(2*(a.index(i)+1)-1)*i for i in a])
#
#
# # print(dev(a))
#
# b = [1,3,4,5,6] # p > * 时
#
# print(dev(b)-dev(a))
#
# c = [1,2,3,5,6] # p < * 时
#
# print(dev(c)-dev(a))
#
# print(dev(a))

# 想证明 b-a > 0

# print([i for i in range(3,7)])

import networkx as nx
DBLP = nx.read_gpickle('./Freebase.gpickle')

print(len(DBLP.nodes()))