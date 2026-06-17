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
num_agents = 100  # Number of agents
beta=1.0
k_list = np.arange(2,100,1)

#define network
def create_network(N, k, seed=None):

    if k == N - 1:
        return nx.complete_graph(N)

    if k == N - 2:
        # Create perfect matching (1-regular graph)
        nodes = list(range(N))
        if seed is not None:
            np.random.seed(seed)
        np.random.shuffle(nodes)

        G_small = nx.Graph()
        for i in range(0, N, 2):
            G_small.add_edge(nodes[i], nodes[i+1])

        # Complement → (N-2)-regular connected graph
        return nx.complement(G_small)

    if k == 2:
        return nx.cycle_graph(N)

    if k > (N - 1) // 2:
        k_small = N - 1 - k
        print(f"Using complement trick: generating {k_small}-regular graph")
        while True:
            G_small = nx.random_regular_graph(d=k_small, n=N, seed=seed)
            # Only require connectivity if possible
            if k_small != 1 and nx.is_connected(G_small):
                break
            elif k_small == 1:
                break

        G = nx.complement(G_small)

    else:
        while True:
            G = nx.random_regular_graph(d=k, n=N, seed=seed)
            if nx.is_connected(G):
                break

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
    C_global = coop_total / total_interactions
    return C_global

    #==================================================================
@njit
def new_generation(kappa, ownimage, payoff, imagescore_others,neighbors,k, mutation_rate):
    N = len(kappa)
    fraction=0.1
    num_updates=int(fraction*N)
    for _ in range(num_updates):
        i = np.random.randint(0, N)
        nbrs = neighbors[i][:k]
        j = nbrs[np.random.randint(0, len(nbrs))] # create empty array to fill with local group
        # Fermi probability
        prob = 1.0 / (1.0 + np.exp(-beta * (payoff[j] - payoff[i])))
        if np.random.random() < prob:
            if np.random.random() > mutation_rate:
                kappa[i] = kappa[j]
            else:
                kappa[i]=np.random.randint(0,3)

    for i in range(N):
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
def main_function(neighbors, k, seed):
    np.random.seed(seed)
    mutation_rate = 0.005
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
# set_num_threads(20)

@njit(parallel=True)
def run_all_k(neighbors_array, k_list,num_runs):

    n = len(k_list)
    results = np.zeros((n,5))

    for i in prange(n):
        neighbors = neighbors_array[i]
        k = k_list[i]

        temp = np.zeros(4)

        for run in range(num_runs):
            seed=1000*i+run
            out= main_function(neighbors, k, seed)
            temp+=out[1:]
        temp/=num_runs

        results[i, 0] = k
        results[i, 1:] = temp
    return results


num_runs=5
end_result=run_all_k(neighbors_array,k_list,num_runs)

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