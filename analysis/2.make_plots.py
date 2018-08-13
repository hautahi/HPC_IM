"""
This program creates plots for the report.
"""

import pandas as pd
from matplotlib import pyplot as plt

#-------------------------
# Multicore: Loop 1 Running Time vs Network Size by Cores
# -------------------------

d = pd.read_csv("./results/multicore-loop1.csv")

#-------------------------
# Multicore: Loop 2-RIS Running Time vs Network Size by Cores
# -------------------------

d = pd.read_csv("./results/multicore-loop2-Exact.csv")

#-------------------------
# Multicore: Loop 2-Exact Running Time vs Network Size by Cores
# -------------------------

d = pd.read_csv("./results/multicore-loop2-RIS.csv")
