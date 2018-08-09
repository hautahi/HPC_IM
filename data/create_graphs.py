"""
This program creates the graph csv files used for
the HPC evaluation project
"""

import numpy as np
import pandas as pd
from igraph import *
import random

# ---------------
# Create Erdos-Renyi Networks
# ---------------

def gen_ER_random(nodes, edges, name):

    # Generate Graph
    G = Graph.Erdos_Renyi(n=nodes,m=edges)

    # Transform into dataframe of edges
    source, target = [], []
    for edge in G.es:
        source.append(edge.source)
        target.append(edge.target)
    
    d = pd.DataFrame({'source': source,'target': target})

    d.to_csv('./ER/' + name +'.csv', index=False)

for n in [10,20,30,40,50,60,70,80,90,100,500,1000,5000,10000,50000,100000]:
    
    e = n*3
    
    random.seed(n)

    gen_ER_random(n, e, 'nodes_' + str(n))
