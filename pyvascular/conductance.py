
import numpy as np
import scipy.sparse as ss

def assemble_matrix(network):
    vessels = network.vessels
    numNodes = network.get_num_nodes()
    numVessels = network.get_num_vessels()
    
    output = np.zeros((numNodes, numNodes))
    output[0][0] = 1
    output[-1][-1] = - (vessels[numVessels-1].get_conductance())
    output[-1][-2] = vessels[numVessels-1].get_conductance()
    
    for i in range(0, numVessels):
        start_node = vessels[i].nodes[0]
        end_node = vessels[i].nodes[1]
        
        if i > 0 and i < numVessels-1:
            output[start_node][start_node] = output[start_node][start_node] - vessels[i].get_conductance()
            output[start_node][end_node] = vessels[i].get_conductance()
            output[end_node][end_node] = output[end_node][end_node] - vessels[i].get_conductance()
            output[end_node][start_node] = vessels[i].get_conductance()
        elif i == 0:
            output[end_node][end_node] = output[end_node][end_node] - vessels[i].get_conductance()
            output[end_node][start_node] = vessels[i].get_conductance()
        elif i == numVessels-1:
            output[start_node][start_node] = output[start_node][start_node] - vessels[i].get_conductance()
            output[start_node][end_node] = vessels[i].get_conductance()
    output = ss.csr_matrix(output)
    return output


def assemble_rhs_vector(network):
    numNodes = network.get_num_nodes()
    rhs_vector = np.zeros(numNodes)
    Q_f = network.get_output_flow_rate()
    rhs_vector[0] = 1
    rhs_vector[-1] = Q_f
    return rhs_vector


def solve_flows(network, pressureSolutionVector):
    numVessels = network.get_num_vessels()
    numNodes = network.get_num_nodes()
    arr = np.zeros((numVessels,numNodes))
    for i in range(numVessels):
        start_node = network.vessels[i].nodes[0]
        end_node = network.vessels[i].nodes[1]
        arr[i][start_node] = network.vessels[i].get_conductance()
        arr[i][end_node] = - network.vessels[i].get_conductance()
        
    csr_conductance = ss.csr_matrix(arr)
    flow_array = csr_conductance.dot(pressureSolutionVector)
    return flow_array


def check_flows_are_correct(flows):
    for i in range(0, len(flows)):
        power = 1 / flows[i]
        if (abs(power - int(round(power))) / int(round(power)) > 0.0001):
            return False
    return True