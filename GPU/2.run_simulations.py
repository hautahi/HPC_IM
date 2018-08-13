"""
- This program runs the 1.run_gpu.py script a number of times with different parameter settings (relating to the size of the network).
"""

import subprocess

# Run both approximation and exact solutions
for node in [10,20,30,40,50,60,70,80,90,100]:

    subprocess.call(["python3","1.run_gpu.py",str(node),"4","0.2","70000","both"], shell=False)

# Run just approximate solutions
for node in [500,1000,5000,10000,50000,100000]:

    subprocess.call(["python3","1.run_gpu.py",str(node),"4","0.2","70000","approx"], shell=False)
