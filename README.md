# High Performance Computing Implementations of RIS Influence Maximization Algorithms
Python code to implement approximate and exact Influence Maximization solutions using RIS-type algorithms

## Graph Inputs

The `create_graphs.py` program within the `data` folder creates a number of csv file representations of Erdos-Renyi networks. These are saved in the `ER` folder and labelled according to the number of nodes.

## Multicore Implementation

The code to run the multicore parallel implementations is contained within the `multicore` folder.

- `RIS_functions.py` defines all the necessary functions to run the algorithms. The file is split into 3 sections, which more or less correspond to the 3 loops described in the Technical Report - the RRRS generators, the RIS Approximate Solver and the RIS Exact Solver.
- `1.run_aws.py` calls the functions defined above to solve the RIS algorithms in parallel. This should be run from the command line as follows: 

  `python3 1.run_aws.py node_size k p mc option`

  where the keyword arguments define the network size (which is read from the `data/ER/` folder) and various IM algorithm parameters. This can be implemented on both a desktop and a cloud server, and makes use of whatever CPU cores are available on the machine/instance it is run on. To use on AWS, see instructions below. The output from this is one csv file for each loop with just one entry stating the time taken to run the given loop. These are stored in the `output` folder.
- `2.run_desktop.py` is very similar to the above but rund each algorithm in series.
- As mentioned, the time to perform each loop is stored as its own csv file in the `output` folder.

## Distributed Implementation

## GPU Implementation

The code to run the GPU parallel implementations is contained within the `GPU` folder.

- `im_gpu.py` defines all the necessary functions to run the algorithms.
- `1.run_gpu.py` calls the functions defined above to solve the RIS algorithms on GPU resources. It can be run from the command line by 

  `python3 1.run_gpu.py node_size k p mc option`

   where the keyword arguments define the network size (which is read from the `data/ER/` folder) and various IM algorithm parameters. The output from this is one csv file for each loop with just one entry stating the time taken to run the given loop. These are stored in the `output` folder.
- `2.run_simulations.py` loops over the `1.run_gpu.py` a number of times with different parameter values to generate the output necessary for the technical report.


## AWS Multicore Instructions
1. Setup instance on the AWS website
2. Login to AWS instance via: `ssh -i path/to/amazonkey.pem ec2-user@instance-address.amazonaws.com`
3. Setup AWS instance with: `sudo yum install python3` and `sudo pip3 install numpy pandas joblib`
4. Transfer file to instance: `scp -i amazonkey.pem file_name ec2-user@instance-address.amazonaws.com:`
5. Transfer folder to instance: `scp -i amazonkey.pem -r folder_name ec2-user@instance-address.amazonaws.com:`
6. Transfer files back to local machine: `scp -i amazonkey.pem -r ec2-user@instance-address.amazonaws.com: .`
