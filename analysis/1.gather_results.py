"""
This program compiles the results from the various simulation runs
"""

import pandas as pd
import os.path

#-------------------------
# Construct Loop 1: multicore
# -------------------------

def get_results(fname):
    if os.path.isfile(fname): 
        temp = pd.read_csv(fname)
        t = temp['time'][0]
    else:
        t = None
    return(t)

node_list = [10,20,30,40,50,60,70,80,90,100,500,1000,5000,10000,50000,100000]
desk, aws4, aws8, aws36, aws72 = [],[],[],[],[]
folder = "../multicore/output/"
for node in node_list:

    fname = folder + "loop1_ser_n" + str(node)+"_mc70000_p0.2_c1_desk.csv"
    desk.append(get_results(fname))
    
    fname = folder + "loop1_par_n" + str(node)+"_mc70000_p0.2_c4_aws.csv"
    aws4.append(get_results(fname))
        
    fname = folder + "loop1_par_n" + str(node)+"_mc70000_p0.2_c8_aws.csv"
    aws8.append(get_results(fname))
        
    fname = folder + "loop1_par_n" + str(node)+"_mc70000_p0.2_c36_aws.csv"
    aws36.append(get_results(fname))
        
    fname = folder + "loop1_par_n" + str(node)+"_mc70000_p0.2_c72_aws.csv"
    aws72.append(get_results(fname))

d = pd.DataFrame({'nodes':node_list,'1':desk,'4': aws4,'8': aws8,'36': aws36,'72': aws72})
d.to_csv("./results/multicore-loop1.csv", index=False)

#-------------------------
# Construct Loop 2 - RIS: multicore
# -------------------------

desk, aws4, aws8, aws36, aws72 = [],[],[],[],[]
for node in node_list:

    fname = folder + "loop2-RIS_ser_n" + str(node)+"_k4_mc70000_p0.2_c1_desk.csv"
    desk.append(get_results(fname))
    
    fname = folder + "loop2-RIS_par_n" + str(node)+"_k4_mc70000_p0.2_c4_aws.csv"
    aws4.append(get_results(fname))
    
    fname = folder + "loop2-RIS_par_n" + str(node)+"_k4_mc70000_p0.2_c8_aws.csv"
    aws8.append(get_results(fname))
    
    fname = folder + "loop2-RIS_par_n" + str(node)+"_k4_mc70000_p0.2_c36_aws.csv"
    aws36.append(get_results(fname))
    
    fname = folder + "loop2-RIS_par_n" + str(node)+"_k4_mc70000_p0.2_c72_aws.csv"
    aws72.append(get_results(fname))

d = pd.DataFrame({'nodes':node_list,'1':desk,'4': aws4,'8': aws8,'36': aws36,'72': aws72})
d.to_csv("./results/multicore-loop2-RIS.csv", index=False)

#-------------------------
# Construct Loop 2 - Exact: multicore
# -------------------------

node_list = [10,20,30,40,50,60,70,80,90]
desk, aws4, aws8, aws36, aws72 = [],[],[],[],[]
for node in node_list:

    fname = folder + "loop2-Exact_ser_n" + str(node)+"_k4_mc70000_p0.2_c1_desk.csv"
    desk.append(get_results(fname))

    fname = folder + "loop2-Exact_par_n" + str(node)+"_k4_mc70000_p0.2_c4_aws.csv"
    aws4.append(get_results(fname))
    
    fname = folder + "loop2-Exact_par_n" + str(node)+"_k4_mc70000_p0.2_c8_aws.csv"
    aws8.append(get_results(fname))
           
    fname = folder + "loop2-Exact_par_n" + str(node)+"_k4_mc70000_p0.2_c36_aws.csv"
    aws36.append(get_results(fname))
    
    fname = folder + "loop2-Exact_par_n" + str(node)+"_k4_mc70000_p0.2_c72_aws.csv"
    aws72.append(get_results(fname))

d = pd.DataFrame({'nodes':node_list,'1':desk,'4': aws4,'8': aws8,'36': aws36,'72': aws72})
d.to_csv("./results/multicore-loop2-Exact.csv", index=False)

#-------------------------
# Construct Loop 1: GPU
# -------------------------

node_list = [10,20,30,40,50,60,70,80,90,100,500,1000,5000,10000]
aws_p2_64, aws_p2_128, aws_p2_256 = [],[],[]
aws_p8_64, aws_p8_128, aws_p8_256 = [],[],[]
for node in node_list:

    # The results from p2.x AWS instance
    folder = "../GPU/output_p2_1/"
    
    fname = folder + "loop1_gpu_n" + str(node)+"_mc70000_p0.2_th64_aws.csv"
    aws_p2_64.append(get_results(fname))
    
    fname = folder + "loop1_gpu_n" + str(node)+"_mc70000_p0.2_th128_aws.csv"
    aws_p2_128.append(get_results(fname))
        
    fname = folder + "loop1_gpu_n" + str(node)+"_mc70000_p0.2_th256_aws.csv"
    aws_p2_256.append(get_results(fname))
        
    # The results from p2.x8 AWS instance
    folder = "../GPU/output_p2_8/"

    fname = folder + "loop1_gpu_n" + str(node)+"_mc70000_p0.2_th64_aws.csv"
    aws_p8_64.append(get_results(fname))
    
    fname = folder + "loop1_gpu_n" + str(node)+"_mc70000_p0.2_th128_aws.csv"
    aws_p8_128.append(get_results(fname))
        
    fname = folder + "loop1_gpu_n" + str(node)+"_mc70000_p0.2_th256_aws.csv"
    aws_p8_256.append(get_results(fname))

    # The results from p2.x16 AWS instance

d = pd.DataFrame({'nodes':node_list,
                  '1gpu-64thread': aws_p2_64,'1gpu-128thread': aws_p2_128,'1gpu-256thread': aws_p2_256,
                  '8gpu-64thread': aws_p8_64,'8gpu-128thread': aws_p8_128,'8gpu-256thread': aws_p8_256})
d.to_csv("./results/gpu-loop1.csv", index=False)

#-------------------------
# Construct Loop 2-RIS: GPU
# -------------------------

node_list = [10,20,30,40,50,60,70,80,90,100,500,1000,5000,10000]
aws_p2_64, aws_p2_128, aws_p2_256 = [],[],[]
aws_p8_64, aws_p8_128, aws_p8_256 = [],[],[]
for node in node_list:

    # The results from p2.x AWS instance
    folder = "../GPU/output_p2_1/"
    
    fname = folder + "loop2-RIS_gpu_n" + str(node)+"_k4_mc70000_p0.2_th64_aws.csv"
    aws_p2_64.append(get_results(fname))
    
    fname = folder + "loop2-RIS_gpu_n" + str(node)+"_k4_mc70000_p0.2_th128_aws.csv"
    aws_p2_128.append(get_results(fname))
        
    fname = folder + "loop2-RIS_gpu_n" + str(node)+"_k4_mc70000_p0.2_th256_aws.csv"
    aws_p2_256.append(get_results(fname))
        
    # The results from p2.x8 AWS instance
    folder = "../GPU/output_p2_8/"

    fname = folder + "loop2-RIS_gpu_n" + str(node)+"_k4_mc70000_p0.2_th64_aws.csv"
    aws_p8_64.append(get_results(fname))
    
    fname = folder + "loop2-RIS_gpu_n" + str(node)+"_k4_mc70000_p0.2_th128_aws.csv"
    aws_p8_128.append(get_results(fname))
        
    fname = folder + "loop2-RIS_gpu_n" + str(node)+"_k4_mc70000_p0.2_th256_aws.csv"
    aws_p8_256.append(get_results(fname))

    # The results from p2.x16 AWS instance

d = pd.DataFrame({'nodes':node_list,
                  '1gpu-64thread': aws_p2_64,'1gpu-128thread': aws_p2_128,'1gpu-256thread': aws_p2_256,
                  '8gpu-64thread': aws_p8_64,'8gpu-128thread': aws_p8_128,'8gpu-256thread': aws_p8_256})
d.to_csv("./results/gpu-loop2-RIS.csv", index=False)

#-------------------------
# Construct Loop 2-Exact: GPU
# -------------------------

node_list = [10,20,30,40,50,60,70,80,90,100]
aws_p2_64, aws_p2_128, aws_p2_256 = [],[],[]
aws_p8_64, aws_p8_128, aws_p8_256 = [],[],[]
for node in node_list:

    # The results from p2.x AWS instance
    folder = "../GPU/output_p2_1/"
    
    fname = folder + "loop2-Exact_gpu_n" + str(node)+"_k4_mc70000_p0.2_th64_aws.csv"
    aws_p2_64.append(get_results(fname))
    
    fname = folder + "loop2-Exact_gpu_n" + str(node)+"_k4_mc70000_p0.2_th128_aws.csv"
    aws_p2_128.append(get_results(fname))
        
    fname = folder + "loop2-Exact_gpu_n" + str(node)+"_k4_mc70000_p0.2_th256_aws.csv"
    aws_p2_256.append(get_results(fname))
        
    # The results from p2.x8 AWS instance
    folder = "../GPU/output_p2_8/"

    fname = folder + "loop2-Exact_gpu_n" + str(node)+"_k4_mc70000_p0.2_th64_aws.csv"
    aws_p8_64.append(get_results(fname))
    
    fname = folder + "loop2-Exact_gpu_n" + str(node)+"_k4_mc70000_p0.2_th128_aws.csv"
    aws_p8_128.append(get_results(fname))
        
    fname = folder + "loop2-Exact_gpu_n" + str(node)+"_k4_mc70000_p0.2_th256_aws.csv"
    aws_p8_256.append(get_results(fname))

    # The results from p2.x16 AWS instance

d = pd.DataFrame({'nodes':node_list,
                  '1gpu-64thread': aws_p2_64,'1gpu-128thread': aws_p2_128,'1gpu-256thread': aws_p2_256,
                  '8gpu-64thread': aws_p8_64,'8gpu-128thread': aws_p8_128,'8gpu-256thread': aws_p8_256})
d.to_csv("./results/gpu-loop2-Exact.csv", index=False)
