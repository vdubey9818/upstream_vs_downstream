import numpy as np
from multiprocessing import Pool
import time
import networkx as nx
import os

start_time = time.time()

# Global Parameters
num_agents = 80
k_list = np.array([
    2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,
    22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,
    41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,
    60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79
])

# Network creation
def create_network(N, k, seed=None):

    if k == 2:
        return nx.cycle_graph(N)

    if (N * k) % 2 != 0:
        raise ValueError("N*k must be even")

    while True:
        G = nx.random_regular_graph(d=k, n=N, seed=seed)
        if nx.is_connected(G):
            return G


def build_one(k):
    G = create_network(num_agents, k)
    neighbors = np.zeros((num_agents, k), dtype=np.int32)
    for i in range(num_agents):
        neighbors[i] = list(G.neighbors(i))
    return neighbors


if __name__ == "__main__":

    num_cores = os.cpu_count()
    num_workers = max(1, num_cores - 3)

    print(f"Using {num_workers} cores (leaving 3 free)")

    with Pool(processes=num_workers) as p:
        neighbors_list = p.map(build_one, k_list)

    neighbors_array = np.array(neighbors_list, dtype=np.int32)

    np.save("neighbors.npy", neighbors_array)

    end_time = time.time()
    print(f"Saved neighbors.npy")
    print(f"Runtime: {end_time - start_time:.2f} seconds")