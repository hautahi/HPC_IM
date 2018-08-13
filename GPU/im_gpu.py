"""
This program defines a number of IM-RIS functions that exploit GPU resources to run in parallel.
@author: mike
"""
from numba import cuda
from numba.cuda.random import create_xoroshiro128p_states, xoroshiro128p_uniform_float32
import numpy as np
import pandas as pd
import math
from numpy import float32
import time
import itertools

@cuda.jit
def get_node_flow_gpu(sources, probs, success, new_nodes, rrs, mc, rng_states):
    thread_id = cuda.grid(1)

    if thread_id >= mc:
        return
    
    source = sources[thread_id]
    rrs[thread_id][source] = True
    new_nodes[thread_id][source] = True
    
    done = False
    while not done:
        done = True
        for i in range(new_nodes.shape[1]):
            if new_nodes[thread_id][i]:
                for j in range(probs.shape[0]):
                    if not rrs[thread_id][j] and probs[j][i] > xoroshiro128p_uniform_float32(rng_states, thread_id):
                        new_nodes[thread_id][j] = True
                        rrs[thread_id][j] = True
                        done = False
            new_nodes[thread_id][i] = False

def get_rrs_gpu(graph, p, mc):
    
    sources = np.random.choice(graph.shape[0], size=mc)
    probs = (p ** graph).astype(float32)
    success = np.full((mc, graph.shape[0]), False, dtype=bool)
    new_nodes = np.full((mc, graph.shape[0]), False, dtype=bool)
    rrs = np.full((mc, graph.shape[0]), False, dtype=bool)
    
    threads_per_block = 128
    blocks = math.ceil(mc / threads_per_block)
    rng_states = create_xoroshiro128p_states(mc, seed=mc)
    
    get_node_flow_gpu[blocks, threads_per_block](sources, probs, success, new_nodes, rrs, mc, rng_states)
    
    return rrs

@cuda.jit
def get_max_val_gpu(rrs, seed_sets, max_val):
    thread_id = cuda.grid(1)

    if thread_id >= seed_sets.shape[0]:
        return
    
    for i in range(rrs.shape[0]):
        increment = False
        for j in range(seed_sets.shape[1]):
            seed = seed_sets[thread_id][j]
            if rrs[i][seed]:
                increment = True
                break
        if increment:
            max_val[thread_id] += 1

def ris_complete_gpu(rrs, k):
    seed_sets = np.array(list(itertools.combinations(range(rrs.shape[1]),k)))
    max_val = np.zeros(seed_sets.shape[0])
    
    threads_per_block = 128
    blocks = math.ceil(seed_sets.shape[0] / threads_per_block)
    get_max_val_gpu[blocks, threads_per_block](rrs, seed_sets, max_val)
    
    return seed_sets[np.argmax(max_val)]
	
def ris(rrs, k):
    # Choose nodes that appear most often (maximum coverage greedy algorithm)
    seeds = []
    rrs_copy = rrs.tolist()
    
    for i in range(k):
        
        # Find node that occurs most often in R
        source_nodes = np.argwhere(rrs_copy)[:, 1]
        seed = np.bincount(source_nodes).argmax()
        
        # Remove RRSs containing last chosen seed 
        rrs_copy = [item for item in rrs_copy if not item[seed]]
        
        # Add to outputs
        seeds.append(seed)
    
    return(seeds)
	
def load_graph(file_name, size):
    df = pd.read_csv(file_name)
    graph = np.zeros((size, size))
    
    for index, row in df.iterrows():
        graph[row['source']][row['target']] = 1
        
    return graph
