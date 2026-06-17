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
num_agents = 150  # Number of agents
k_list = np.array([2,3,4,5,6,7,8,9])

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
def compute_clusters_and_interfaces(kappa, neighbors, k):
    N = len(kappa)
    visited = np.zeros(N, dtype=np.int32)

    # Results
    num_comp_U = 0
    num_comp_D = 0
    num_comp_Def = 0

    max_size_U = 0
    max_size_D = 0
    max_size_Def = 0

    sum_size_U = 0
    sum_size_D = 0
    sum_size_Def = 0

    interface_edges_U_D = 0
    interface_edges_U_Def = 0
    interface_edges_D_Def = 0

    # --------------------------------------------
    # Count interface edges (U-D) (U-Def) (D-Def)
    # --------------------------------------------
    for i in range(N):
        for j in range(k):
            nbr = neighbors[i][j]
            if nbr > i:  # avoid double counting
                if (kappa[i] == 0 and kappa[nbr] == 1) or (kappa[i] == 1 and kappa[nbr] == 0):
                    interface_edges_U_D += 1
                elif (kappa[i] == 0 and kappa[nbr] == 2) or (kappa[i] == 2 and kappa[nbr] == 0):
                    interface_edges_U_Def += 1
                elif (kappa[i] == 1 and kappa[nbr] == 2) or (kappa[i] == 2 and kappa[nbr] == 1):
                    interface_edges_D_Def += 1

    # -------------------------------------------
    # Find connected components
    # -------------------------------------------
    for i in range(N):

        if visited[i] == 1:
            continue


        # BFS
        stack = np.empty(N, dtype=np.int32)
        top = 0

        stack[top] = i
        top += 1
        visited[i] = 1

        comp_size = 0
        comp_type = kappa[i] # upstream-0, downstream-1, defector-2


        while top > 0:
            node = stack[top - 1]
            top -= 1

            comp_size += 1

            for j in range(k):
                nbr = neighbors[node][j]

                if visited[nbr] == 0 and kappa[nbr] == comp_type:
                    visited[nbr] = 1
                    stack[top] = nbr
                    top += 1

        # Update stats
        if comp_type == 0:  #upstream
            num_comp_U += 1
            sum_size_U += comp_size

            if comp_size > max_size_U:
                max_size_U = comp_size

        elif comp_type == 1: #downstream
            num_comp_D += 1
            sum_size_D += comp_size

            if comp_size > max_size_D:
                max_size_D = comp_size

        elif comp_type == 2: #defector
            num_comp_Def +=1
            sum_size_Def += comp_size

            if comp_size > max_size_Def:
                max_size_Def = comp_size

    avg_size_U = 0.0
    avg_size_D = 0.0
    avg_size_Def = 0.0

    if num_comp_U > 0:
        avg_size_U = sum_size_U / num_comp_U

    if num_comp_D > 0:
        avg_size_D = sum_size_D / num_comp_D

    if num_comp_Def > 0:
        avg_size_Def = sum_size_Def / num_comp_Def

    return num_comp_U, num_comp_D, num_comp_Def, max_size_U, max_size_D, max_size_Def, avg_size_U, avg_size_D, avg_size_Def, interface_edges_U_D, interface_edges_U_Def, interface_edges_D_Def




@njit
def simulate(num_generations, kappa, ownimage, payoff, imagescore_others,
             neighbors,k, max_games, b, c, mutation_rate):

    C_globalCum = 0.0
    kappa_upCum = 0.0
    kappa_downCum = 0.0
    kappa_defCum = 0.0

    avgU_compCum = 0.0
    avgD_compCum = 0.0
    avgDef_compCum = 0.0

    numU_compCum = 0.0
    numD_compCum = 0.0
    numDef_compCum = 0.0

    maxU_compCum = 0.0
    maxD_compCum = 0.0
    maxDef_compCum = 0.0

    interfaceCum_U_D = 0.0
    interfaceCum_U_Def = 0.0
    interfaceCum_D_Def = 0.0

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
        numU, numD, numDef, maxU, maxD, maxDef, avgU, avgD, avgDef, interUD, interUDef, interDDef = compute_clusters_and_interfaces(kappa, neighbors, k)
        
        numU_compCum += numU
        numD_compCum += numD
        numDef_compCum += numDef

        maxU_compCum += maxU
        maxD_compCum += maxD
        maxDef_compCum += maxDef

        avgU_compCum += avgU
        avgD_compCum += avgD
        avgDef_compCum += avgDef
        
        interfaceCum_U_D += interUD
        interfaceCum_U_Def += interUDef
        interfaceCum_D_Def += interDDef

        new_generation(kappa, ownimage, payoff,
                       imagescore_others, neighbors,k,
                       mutation_rate)
    return (
    kappa_upCum / num_generations,
    kappa_downCum / num_generations,
    kappa_defCum / num_generations,
    C_globalCum / num_generations,
    numU_compCum / num_generations,
    numD_compCum / num_generations,
    numDef_compCum / num_generations,
    maxU_compCum / num_generations,
    maxD_compCum / num_generations,
    maxDef_compCum/num_generations,
    avgU_compCum / num_generations,
    avgD_compCum / num_generations,
    avgDef_compCum / num_generations,
    interfaceCum_U_D / num_generations,
    interfaceCum_U_Def / num_generations,
    interfaceCum_D_Def / num_generations
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
    out = np.zeros(17)
    out[0] = k
    out[1:] = result
    return out




# detect cores
# num_cores = os.cpu_count()

# leave two cores free
# set_num_threads(num_cores - 3)

@njit(parallel=True)
def run_all_k(neighbors_array, k_list):

    n = len(k_list)
    results = np.zeros((n,17))

    for i in prange(n):
        neighbors = neighbors_array[i]
        k = k_list[i]
        results[i] = main_function(neighbors, k)
    return results



end_result=run_all_k(neighbors_array,k_list)

np.savetxt(
    f"k_vs_frequencies_N={num_agents}.txt",
    end_result,
    header="k f_up f_down f_allD C_global_avg Ncomp_U Ncomp_D Ncomp_Def Smax_U Smax_D Smax_Def Avg_U Avg_D Avg_Def E_UD E_UDef E_DDef",
    fmt="%.6f"
)

print(end_result)
end_time = time.time()
runtime = end_time - start_time
print(f"Runtime: {runtime:.6f} seconds")