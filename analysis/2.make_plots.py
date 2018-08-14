"""
This program creates plots for the report.
@author: luke
"""

import pandas as pd
from matplotlib import pyplot as plt

#-------------------------
# Multicore: Loop 1 Running Time vs Network Size by Cores
# -------------------------

d_L1 = pd.read_csv("./results/multicore-loop1.csv",index_col=5)
cols = [int(x) for x in d_L1.columns]
cols= sorted(cols)
cols = [str(x) for x in cols]
d_L1=d_L1[cols]

names=list(d_L1.index)
names=[str(x) for x in names]
name_index=range(len(names))
values=d_L1.values

plt.plot(name_index, values)
plt.xticks(name_index, names)
plt.legend(([str(x)+' cores' for x in d_L1.columns]))
plt.xlabel('Nodes')
plt.ylabel('Runtime, seconds')
plt.title('Loop 1 Running Time with Network Size & Cores')
fig = plt.gcf()
fig.set_size_inches(11, 5)
plt.savefig('./graphs/L1.png')
plt.clf()



#-------------------------
# Multicore: Loop 2-RIS Running Time vs Network Size by Cores
# -------------------------

d_RIS = pd.read_csv("./results/multicore-loop2-RIS.csv",index_col=5)
cols = [int(x) for x in d_RIS.columns]
cols= sorted(cols)
cols = [str(x) for x in cols]
d_RIS=d_RIS[cols]

names=list(d_RIS.index)
names=[str(x) for x in names]
name_index=range(len(names))
values=d_RIS.values

plt.plot(name_index, values)
plt.xticks(name_index, names)
plt.legend(([str(x)+' cores' for x in d_RIS.columns]))
plt.xlabel('Nodes')
plt.ylabel('Runtime, seconds')
plt.title('Loop 2-RIS Running Time with Network Size & Cores')
fig = plt.gcf()
fig.set_size_inches(11, 5)
plt.savefig('./graphs/L2_RIS.png')
plt.clf()

#-------------------------
# Multicore: Loop 2-Exact Running Time vs Network Size by Cores
# -------------------------

d_ex = pd.read_csv("./results/multicore-loop2-Exact.csv",index_col=5)
cols = [int(x) for x in d_ex.columns]
cols= sorted(cols)
cols = [str(x) for x in cols]
d_ex=d_ex[cols]

names=list(d_ex.index)
names=[str(x) for x in names]
name_index=range(len(names))
values=d_ex.values

plt.plot(name_index, values)
plt.xticks(name_index, names)
plt.legend(([str(x)+' cores' for x in d_ex.columns]))
plt.xlabel('Nodes')
plt.ylabel('Runtime, seconds')
plt.title('Loop 2-Exact Running Time with Network Size & Cores')
fig = plt.gcf()
fig.set_size_inches(11, 5)
plt.savefig('./graphs/L2_Exact.png')
plt.clf()

#-------------------------
# Multicore: Loop 1- Speed Improvement with Number of Cores
# -------------------------
names=list(d_L1.loc[100000].index)
names=[str(x) for x in names]
name_index=range(len(names))
values=d_L1.loc[100000]

plt.plot(name_index, values)
plt.xticks(name_index, names)
plt.xlabel('Cores')
plt.ylabel('Runtime, seconds')
plt.title('Loop 1- 100,000 nodes')
fig = plt.gcf()
fig.set_size_inches(11, 5)
plt.savefig('./graphs/L1_cores_speedup.png')
plt.clf()

#-------------------------
# Multicore: Loop 2, RIS- Speed Improvement with Number of Cores
# -------------------------
names=list(d_RIS.loc[100000].index)
names=[str(x) for x in names]
name_index=range(len(names))
values=d_RIS.loc[100000]

plt.plot(name_index, values)
plt.xticks(name_index, names)
plt.xlabel('Cores')
plt.ylabel('Runtime, seconds')
plt.title('Loop 2, RIS- 100,000 nodes')
fig = plt.gcf()
fig.set_size_inches(11, 5)
plt.savefig('./graphs/L2_RIS_cores_speedup.png')
plt.clf()

#-------------------------
# Multicore: Loop 2, Exact - Speed Improvement with Number of Cores
# -------------------------
names=list(d_ex.loc[30].index)
names=[str(x) for x in names]
name_index=range(len(names))
values=d_ex.loc[30]

plt.plot(name_index, values)
plt.xticks(name_index, names)
plt.xlabel('Cores')
plt.ylabel('Runtime, seconds')
plt.title('Loop 2, RIS- 30 nodes')
fig = plt.gcf()
fig.set_size_inches(11, 5)
plt.savefig('./graphs/L2_exact_cores_speedup.png')
plt.clf()

#-------------------------
# Multicore: Computation of Exact Solution
# -------------------------
d_ex = pd.read_csv("./results/multicore-loop2-Exact.csv",index_col=5)
d_ex=pd.DataFrame(d_ex['72'])

names=list(d_ex.index)
names=[str(x) for x in names]
name_index=range(len(names))
values=d_ex.values

plt.plot(name_index, values)
plt.xticks(name_index, names)
plt.legend(([str(x)+' cores' for x in d_ex.columns]))
plt.xlabel('Nodes')
plt.ylabel('Runtime, seconds')
plt.title('Loop 2-Exact Running Time with Network Size using 72 Cores')
fig = plt.gcf()
fig.set_size_inches(11, 5)
plt.savefig('./graphs/L2_Exact_72c.png')
plt.clf()
