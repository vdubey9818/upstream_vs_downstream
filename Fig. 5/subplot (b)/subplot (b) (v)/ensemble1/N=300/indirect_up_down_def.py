import numpy as np
import random
import matplotlib.pyplot as plt
from collections import Counter
import time
from numba import njit
import networkx as nx
from tqdm import tqdm
start_time = time.time()
# Parameters
num_agents = 300 # Number of agents
max_games = (num_agents-1)*150

mutation_rate = 0.005  # Probability of mutation
b, c = 1, 0.1  # Benefit and cost
num_generations = 10**7 # Number of generations

#kappa=0 is upsteam
#kappa=1 is downstream
#kappa=2 is alld

#create the array of upstream downstream and alld's
kappa = np.random.choice([0,1,2], num_agents)
ownimage = np.ones(num_agents) # keep initial motivation level high
payoff = np.zeros(num_agents)  # initial payoff is zero
imagescore_others=np.ones(num_agents) # initial image score is good


@njit
def play_games(kappa,ownimage,payoff,imagescore_others,max_games,b,c):
    coop_total = 0
    total_interactions = 0
    N = len(kappa)
    for i in range(N):
        payoff[i] = 0
    for g in range(max_games):
        donor = np.random.randint(0, N)
        receiver = np.random.randint(0, N-1) #generate a random receiver Index-shift method
        if receiver >= donor:
            receiver += 1
        total_interactions += 1
        #donor is upstream
        if kappa[donor]==0:
            if ownimage[donor] == 1: #upstream individual is +vely motivated
                payoff[donor] -= c
                payoff[receiver] += b
                coop_total += 1
                ownimage[receiver]=1
                imagescore_others[donor] = 1

            else: #upstream individual is -vely motivated
                ownimage[receiver]=-1
                imagescore_others[donor] = -1
        #donor is downstream
        elif kappa[donor]==1:
            if imagescore_others[receiver] == 1:
                payoff[donor] -= c
                payoff[receiver] += b
                coop_total += 1
                ownimage[receiver] = 1
                imagescore_others[donor] = 1
            else:
                ownimage[receiver] = -1
                imagescore_others[donor] =-1
        
        #donor is allD
        elif kappa[donor]==2:
            ownimage[receiver]=-1
            imagescore_others[donor] = -1
    C_global = coop_total / total_interactions

    return C_global


@njit
def fermi_update(kappa, payoff, beta, mutation_rate):
    N = len(kappa)
    fraction=0.1
    num_updates = int(fraction * N)
    for _ in range(num_updates):
        i = np.random.randint(0, N)
        j = np.random.randint(0, N-1)
        if j >= i:
            j += 1

        # Fermi probability
        prob = 1.0 / (1.0 + np.exp(-beta * (payoff[j] - payoff[i])))

        if np.random.random() < prob:
            if np.random.random() > mutation_rate:
                kappa[i] = kappa[j]
            else:
                kappa[i] = np.random.randint(0, 3)


#==================================================================
# Simulation and visualization
frequencies_sequence=np.zeros((num_generations,3))
frequencies_kappa = {num: 0 for num in [0, 1, 2]}
C_global_cum = np.zeros(num_generations)

beta=1.0

for gen in tqdm(range(num_generations), desc="Simulating"):
    Cg = play_games(kappa, ownimage, payoff,imagescore_others,max_games, b, c)
    if gen == 0:
        C_global_cum[gen] = Cg
    else:
        C_global_cum[gen] = C_global_cum[gen-1] + Cg

    data_kappa = kappa
    for num in [0, 1, 2]:
        frequencies_kappa[num] += np.sum(data_kappa == num) / num_agents
    frequencies_sequence[gen, :] = list(frequencies_kappa.values())
    fermi_update(kappa, payoff,beta,mutation_rate)
    for i in range(num_agents):
        ownimage[i] = 1
        imagescore_others[i] = 1



# ===========================================
rows, _ = frequencies_sequence.shape
divisors = np.arange(1, rows + 1).reshape(-1, 1)
# Divide each row by the corresponding divisor
kappa_sequence = frequencies_sequence / divisors
# kappa_sequence = frequencies_sequence

divisors = np.arange(1, num_generations + 1)
C_global_avg = C_global_cum / divisors




np.savetxt(f'kd_sequenceN={num_agents}_time={num_generations}UpDownAlld.txt',kappa_sequence[-100:])
np.savetxt(f'sequenceN={num_agents}_time={num_generations}global_coop_avg.txt',C_global_avg[-100:])


#=================================================================================
end_time = time.time()
runtime = end_time - start_time
print(f"Runtime: {runtime:.6f} seconds")
#===================================================================
time = np.arange(kappa_sequence.shape[0])
fig, axes = plt.subplots(2, 3, figsize=(16, 10))

label_mat = ['Upstream','Downstream','Defectors']
colorbox = ['red', 'green', 'blue']

# ---- κ frequencies ----
for i in range(3):
    axes[0, i].plot(time, kappa_sequence[:, i],
                    color=colorbox[i], label=label_mat[i])
    axes[0, i].legend(loc='upper left')
    axes[0, i].set_ylabel('⟨frequency⟩')




axes[1, 0].plot(time, C_global_avg, color='black', lw=2, label='Cooperation')
axes[1, 0].legend(loc='upper left')

plt.tight_layout()
plt.savefig(f'coop_and_kappa_N={num_agents}_time={num_generations}.png', dpi=300)
plt.show()

