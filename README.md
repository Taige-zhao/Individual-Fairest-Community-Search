# Implementation for Individual-Fairest-Community-Search

This repository is a reference implementation of the querying algorithms proposed in "Effective Fairest Community Search over Heterogeneous Information Networks".

# Data Source
All the Graph Data are Available at: https://pytorch-geometric.readthedocs.io/en/latest/modules/datasets.html

# Requirements
Python 3
numpy 1.19.4
networkx 2.5
torch_geometric 2.1.0
gnuplotlib 0.38

# Run the Code
Download the datasets and run the test files in the Algorithm folder. 

Notes that the running time varies because of the motif algorithm you used. In this example, we use DotMotif in the paper "DotMotif: an open-source tool for connectome subgraph isomorphism search and graph queries", which can be used directly in Python. But this is not the fastest algorithm currently. You can try the state-of-art algorithms like VF3 or methods in the paper: "Subgraph Matching with Effective Matching Order and Indexing".
