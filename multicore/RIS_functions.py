"""
Define all functions used for experimental evaluation of IM algorithms
on multicore resources such as AWS

# Table of Contents
   1. Create R, a large set of RRRSs. This is Loop 1 in Technical Report
      Can be performed in series or parallel (MP and joblib)
   2. Run RIS approximate algorithm. This is Loop 2 in Technical Report
      Performed in series because computation cost is trivial
   3. Run RIS exact algorithm. This is Loop 2-Exact in Technical Report
      Can be performed in series or parallel (MP and joblib)
"""

# ---------------------------
# Dependencies
# ---------------------------

from random import uniform, seed
import numpy as np
import pandas as pd
import time
import random
from collections import Counter
import itertools as it
import multiprocessing
from multiprocessing import Pool
from joblib import Parallel, delayed
import warnings
import os

# ---------------------------
# Section 1. Create R
# ---------------------------

# 1a. Create One Random Reverse Reachable Set (RRRS)
def make_RRS(g,p):
    """
    Inputs: g:  Vx2 dataframe of directed edges and weights.
                Columns are ['source','target']. Each row is an edge.
            p:  Disease propagation probability
    Return: One RRRS
    """

    # Step 1. Select random source node
    source = random.choice(list(set(g['source'].tolist())))

    # Step 2. Get an instance from g by sampling edges
    g['success'] = np.random.uniform(0,1,len(g['source'])) < p
    g = g.loc[g['success'] == True]

    # Step 3. Construct reverse reachable set of the random source node
    new_nodes, RRS0, diff = [source], [source], 1

    while diff > 0:

        # Limit to edges that flow into the source node
        temp = g.loc[g['target'].isin(new_nodes)]

        # Extract the nodes flowing into the source node
        temp = temp['source'].tolist()

        # Add new set of in-neighbors to the RRS
        RRS = list(set(RRS0 + temp))

        # Find what new nodes were added
        new_nodes = list(set(RRS) - set(RRS0))

        # Reset loop variables
        RRS0, diff = RRS[:], len(new_nodes)

    return(RRS)

# 1b. Series implementation of constructing R
def get_R(G,p,mc):
    """
    Inputs: G:  Vx2 dataframe of directed edges and weights.
                Columns are ['source','target']. Each row is an edge
            p:  Disease propagation probability
            mc: number of RRRS sets created
    Return: A collection of mc random reverse reachable sets
    """
    
    R = [make_RRS(G,p) for i in range(mc)]

    return(R)

# 1c. Parallel implementation of constructing R
def get_R_parallel(G,p,mc,p_type='mp'):
    """
    Inputs: G:  Vx2 dataframe of directed edges and weights.
                Columns are ['source','target']. Each row is an edge
            p:  Disease propagation probability
            mc: number of RRS sets created
            p_type: type of parallelization method (mp or joblib)
    Return: A collection of mc random reverse reachable sets (also # of cores just for information)
    """
    
    num_cores = multiprocessing.cpu_count()

    # Option 1: Joblib method
    if p_type=='joblib':
        R = Parallel(n_jobs=num_cores,verbose=0)(delayed(make_RRS)(G,p)for i in range(mc))

    # Option 2: Multiprocessing method
    else:
        with Pool(num_cores) as pl:
            R = pl.starmap(make_RRS,[(g,p) for i in range(mc)])

    return(R,num_cores)

# ---------------------------
# Section 2. RIS algorithm - series
# ---------------------------

def ris(R,k):
    """
    Inputs: R: set of RRRS expressed as a list of list of nodes
            k: size of seed set
    Return: A seed set of nodes as an approximate solution to the IM problem
    """

    # Choose nodes that appear most often (maximum coverage greedy algorithm)
    SEED = []
    for i in range(k):

        # Find node that occurs most often in R
        flat_list = [item for sublist in R for item in sublist]
        seed = Counter(flat_list).most_common()[0][0]

        # Remove RRSs containing last chosen seed
        R = [item for item in R if seed not in item]

        # Add to outputs
        SEED.append(seed)

    return(SEED)

# ---------------------------
# Section 3. RIS-Exact algorithm
# ---------------------------

# 3a. Series Implementation
def ris_exact(G,R,k):
    """
    Inputs: G: Vx2 dataframe of directed edges and weights.
               Columns are ['source','target']. Each row is an edge
            R: set of RRRS expressed as a list of list of nodes
            k: size of seed set
    Return: A seed set of nodes that is the exact solution to the IM problem
    """

    # Generate all possible seed sets
    n = len(set(G['source'].tolist()))
    seed_sets = list(it.combinations(range(n),k))
    
    # Select seed set that appears in most RRS sets
    max_val = 0
    for ss in seed_sets:
        count = 0
        for rrrs in R:
            count += any([x in rrrs for x in ss])

        if count > max_val:
            max_val, max_set = count, ss

    return(max_set)

# 3b. Parallel Implementation (requires the split into 2 functions)
def ris_complete_loop(ss,R):
    ss_eval = []
    for rs in R:
        ss_eval.append(any([i in rs for i in ss]))
    return([ss,Counter(ss_eval)[True]])

def ris_exact_parallel(G,R,k,p_type='mp'):
    """
    Inputs: G: Vx2 dataframe of directed edges and weights.
               Columns are ['source','target']. Each row is an edge
            R: set of RRRS expressed as a list of list of nodes
            k: size of seed set
            p_type: type of parallelization method (mp or joblib)
    Return: A seed set of nodes that is the exact solution to the IM problem (also # of cores just for information)
    """

    # Generate all possible seed sets
    n = len(set(G['source'].tolist()))
    seed_sets = list(it.combinations(range(n),k))

    # Check number of cores in system
    num_cores = multiprocessing.cpu_count()

    # Option 1: Joblib method
    if p_type=='joblib':
        ss_in_rs = Parallel(n_jobs = num_cores,verbose = 0)(delayed(ris_complete_loop)(ss,R) for ss in seed_sets)

    # Option 2: Multiprocessing method
    else:
        with Pool(num_cores) as pl:
            ss_in_rs = pl.starmap(ris_complete_loop,[(ss,R) for ss in seed_sets])
    
    # Find seed set that appears in most RRSs
    max_val = 0
    for i in ss_in_rs:
        if i[1] > max_val:
            max_set, max_val = i[0], i[1]

    return(max_set,num_cores)
