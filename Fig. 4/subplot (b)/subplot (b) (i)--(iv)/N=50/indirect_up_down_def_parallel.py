import numpy as np
import random
import matplotlib.pyplot as plt
from collections import Counter
import time
import networkx as nx
# from tqdm import tqdm
start_time = time.time()
import os
from numba import njit, prange, set_num_threads


# Global Parameters
num_agents = 50  # Number of agents
k_list = np.array([2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,
    22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,
    45,46,47,48,49])

#define network
def create_network(N, k, seed=None):

    if k == 2:
        return nx.cycle_graph(N)

    if (N * k) % 2 != 0:
        raise ValueError("N*k must be even")

    while True:
        G = nx.random_regular_graph(d=k, n=N, seed=seed)
        if nx.is_connected(G):
            return G



neighbors_array = np.zeros((len(k_list), num_agents, max(k_list)), dtype=np.int32)

for idx, k in enumerate(k_list):
    G = create_network(num_agents, k)
    for i in range(num_agents):
        nbrs = list(G.neighbors(i))
        neighbors_array[idx, i, :k] = nbrs

@njit
def play_games(kappa, ownimage, payoff, imagescore_others, neighbors,k, max_games, b, c):
    
    N = len(kappa)
    coop_total = 0
    total_interactions = 0

    for i in range(N):
        payoff[i] = 0

    for g in range(max_games):

        donor = np.random.randint(0, N)
        nbrs = neighbors[donor][:k]
        receiver = nbrs[np.random.randint(0, k)]
        total_interactions += 1
        #donor is upstream
        if kappa[donor] == 0: 
            if ownimage[donor] == 1:#upstream individual is +vely motivated
                payoff[donor] -= c
                payoff[receiver] += b
                coop_total += 1
                ownimage[receiver] = 1
                imagescore_others[donor] = 1
            else: #upstream individual is -vely motivated
                ownimage[receiver] = -1
                imagescore_others[donor] = -1

        #donor is downstream
        elif kappa[donor] == 1:
            if imagescore_others[receiver] == 1:
                payoff[donor] -= c
                payoff[receiver] += b
                coop_total += 1
                ownimage[receiver] = 1
                imagescore_others[donor] = 1
            else:
                ownimage[receiver] = -1
                imagescore_others[donor] = -1
        #donor is allD
        elif kappa[donor]==2:
            ownimage[receiver] = -1
            imagescore_others[donor] = -1
        payoff[donor] +=c
        payoff[receiver] +=c
    C_global = coop_total / total_interactions
    return C_global

    #==================================================================
@njit
def new_generation(kappa, ownimage, payoff, imagescore_others,neighbors,k, mutation_rate):
    N = len(kappa)
    new_kappa = np.zeros(N, dtype=np.int32) # new kappa to store the values before moving it to next generation    agent.oldkappa=agent.kappa

    for i in range(N):
        nbrs = neighbors[i][:k]
        local_size = k + 1
        local_group = np.empty(local_size, dtype=np.int32) # create empty array to fill with local group
        for j in range(len(nbrs)):
            local_group[j] = nbrs[j]
        local_group[-1] = i

    #compute the local payoff sum to make sure reproduction happens according to payoff
        local_payoff = 0.0
        for j in range(local_size):
            local_payoff += payoff[local_group[j]]

        #sampling with payoff
        if local_payoff > 0:
            r = np.random.random() * local_payoff #random number (0, total local payoff)
            s = 0
            for j in range(local_size): #find the index of the parent whose payoff crosess the cum dist
                idx = local_group[j]
                s += payoff[idx]
                if s >= r:
                    parent = idx
                    break   
        else:
            parent = local_group[np.random.randint(0, local_size)]

        # Mutation
        if np.random.random() > mutation_rate:
            new_kappa[i] = kappa[parent]
        else:
            new_kappa[i] = np.random.randint(0, 3)
    for i in range(N):
        kappa[i] = new_kappa[i]
        ownimage[i] = 1
        imagescore_others[i] = 1


@njit
def simulate(num_generations, kappa, ownimage, payoff, imagescore_others,
             neighbors,k, max_games, b, c, mutation_rate):

    C_globalCum = 0.0
    kappa_upCum = 0.0
    kappa_downCum = 0.0
    kappa_defCum = 0.0

    N = len(kappa)

    for gen in range(num_generations):

        Cg = play_games(kappa, ownimage, payoff,
                        imagescore_others, neighbors,k,
                        max_games, b, c)

        C_globalCum += Cg
        up = 0
        down = 0
        defe = 0

        for i in range(N):
            if kappa[i] == 0:
                up += 1
            elif kappa[i] == 1:
                down += 1
            else:
                defe += 1

        kappa_upCum   += up / N
        kappa_downCum += down / N
        kappa_defCum  += defe / N

        new_generation(kappa, ownimage, payoff,
                       imagescore_others, neighbors,k,
                       mutation_rate)
    return (
        kappa_upCum / num_generations,
        kappa_downCum / num_generations,
        kappa_defCum / num_generations,
        C_globalCum / num_generations
    )


@njit
def main_function(neighbors, k):
    np.random.seed(k * 123 + 7)
    mutation_rate = 0.001
    b, c = 1, 0.1
    num_generations = 10**7
    max_games = int(num_agents/2)*k

    kappa = np.random.randint(0,3,num_agents).astype(np.int32)
    ownimage = np.ones(num_agents)
    payoff = np.zeros(num_agents)
    imagescore_others = np.ones(num_agents)

    result = simulate(
        num_generations,
        kappa,
        ownimage,
        payoff,
        imagescore_others,
        neighbors,k,
        max_games,
        b,
        c,
        mutation_rate
    )
    out = np.zeros(5)
    out[0] = k
    out[1:] = result
    return out




# detect cores
num_cores = os.cpu_count()

# leave two cores free
set_num_threads(num_cores - 3)

@njit(parallel=True)
def run_all_k(neighbors_array, k_list):

    n = len(k_list)
    results = np.zeros((n,5))

    for i in prange(n):
        neighbors = neighbors_array[i]
        k = k_list[i]
        results[i] = main_function(neighbors, k)
    return results



end_result=run_all_k(neighbors_array,k_list)

np.savetxt(
    f"k_vs_frequencies_N={num_agents}.txt",
    end_result,
    header="k f_up f_down f_allD C_global_avg",
    fmt="%.6f"
)

print(end_result)
end_time = time.time()
runtime = end_time - start_time
print(f"Runtime: {runtime:.6f} seconds")