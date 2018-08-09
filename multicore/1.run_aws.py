"""
- This program calls functions to run RIS algorithms on AWS multicore instances in parallel.
- It is designed to be called from the command line.
- The command line keyword arguments are described below
- Output is one csv file for each loop with just one entry stating the time taken to run the given loop.
"""

# Import functions & modules
from RIS_functions import *
import pandas as pd
import sys

# Define Function
def main():
    """
    Function expects arguments via terminal entry:
    nodes: integer size of network
    k:     size of seed set
    p:     Disease propagation probability
    mc:    Number of RRRS sets to generate (size of R)
    opt:   option of ('approx','exact','both') which determines the loop that is run. (Loop 1 must be run)
    """

    # Read in keyword arguments 
    args = sys.argv[1:]
    if not args or len(args) < 5:
        print('usage: node_number k p mc opt')
        sys.exit(1)
    
    nodes, k, p = int(args[0]), int(args[1]), float(args[2])
    mc, opt = int(args[3]), args[4]

    # Read Graph
    G = pd.read_csv("../data/ER/nodes_" + str(nodes) + ".csv")

    # Run Loop 1: Get R
    start = time.time()
    R, cores = get_R_parallel(G,p,mc,p_type='joblib')
    t = time.time() - start
    name = ['./output/','loop1','_par','_n',nodes,'_mc',mc,'_p',p,'_c',cores,'_aws','.csv']
    name = ''.join(map(str, name))
    pd.DataFrame({'time': [t]}).to_csv(name, index=False)
        
    # Run Loop 2: RIS-Approximate
    if (opt == 'approx') | (opt == 'both'):
        start = time.time()
        _ = ris(R,k)
        t = time.time() - start
        name = ['./output/','loop2-RIS','_par','_n',nodes,'_k',k,'_mc',mc,'_p',p,'_c',cores,'_aws','.csv']
        name = ''.join(map(str, name))
        pd.DataFrame({'time': [t]}).to_csv(name, index=False)

    # Run Loop 2: RIS-Exact
    if (opt == 'exact') | (opt == 'both'):
        start = time.time()
        _,_ = ris_exact_parallel(G,R,k,p_type='mp')
        t = time.time() - start
        name = ['./output/','loop2-Exact','_par','_n',nodes,'_k',k,'_mc',mc,'_p',p,'_c',cores,'_aws','.csv']
        name = ''.join(map(str, name))
        pd.DataFrame({'time': [t]}).to_csv(name, index=False)

if __name__ == '__main__':
    main()
