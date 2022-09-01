
# file to store functions for parallel project calculations

import numpy as np



def determine_workloads(network, size, rank):
    workloads = [ network.get_num_vessels() // size for i in range(size) ]
    for i in range( network.get_num_vessels() % size ):
        workloads[i] += 1
    my_start = 0
    for i in range( rank ):
        my_start += workloads[i]
    my_end = my_start + workloads[rank]
    return my_start, my_end



def assemble_triplet_parallel(network, start, end):
    
    triplet = np.empty([1, 3])
    for i in range(start, end):
        start_node = network.vessels[i].nodes[0]
        end_node = network.vessels[i].nodes[1]
        triplet = np.append(triplet, [i, start_node, network.vessels[i].get_conductance()])
        triplet = np.append(triplet, [i, end_node, - network.vessels[i].get_conductance()])
        
    triplet.resize(2*(end-start)+1, 3)  
    triplet = np.delete(triplet, 0, 0)
    return triplet