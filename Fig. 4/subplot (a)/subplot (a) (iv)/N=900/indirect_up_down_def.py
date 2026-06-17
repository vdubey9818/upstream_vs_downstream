import numpy as np
# import random
import matplotlib.pyplot as plt
# from collections import Counter
import time
from numba import njit
# import networkx as nx
from tqdm import tqdm
start_time = time.time()
# Parameters
num_agents = 900 # Number of agents
max_games = (num_agents-1)*450

mutation_rate = 0.001  # Probability of mutation
b, c = 1, 0.1  # Benefit and cost
num_generations = 10**7 # Number of generations

#kappa=0 is upsteam
#kappa=2 is alld

#create the array of upstream downstream and alld's
kappa = np.random.choice([0,2], num_agents)
ownimage = np.ones(num_agents) # keep initial motivation level high
payoff = np.zeros(num_agents)  # initial payoff is zero



@njit
def play_games(kappa,ownimage,payoff,max_games,b,c):
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

            else: #upstream individual is -vely motivated
                ownimage[receiver]=-1
        
        #donor is allD
        elif kappa[donor]==2:
            ownimage[receiver]=-1


        payoff[donor] +=c
        payoff[receiver] +=c

    # ---- cooperation levels (instantaneous) ----
    C_global = coop_total / total_interactions

    return C_global

#==================================================================
@njit
def new_generation(kappa, ownimage, payoff, mutation_rate):
    N = len(kappa)
    new_kappa = np.zeros(N, dtype=np.int32) # new kappa to store the values before moving it to next generation

    #compute the payoff sum to make sure reproduction happens according to payoff
    payoff_sum = 0
    for j in range(N):
        payoff_sum += payoff[j]

    for i in range(N):
        #sampling with payoff 
        if payoff_sum > 0:
            r = np.random.random() * payoff_sum #random number (0, total local payoff)
            s = 0
            for j in range(N): #find the index of the parent whose payoff crosess the cum dist
                s += payoff[j]
                if s >= r:
                    parent = j
                    break
        else:
            parent = np.random.randint(0, N)

        #incorporate mutation
        if np.random.random() > mutation_rate:
            new_kappa[i] = kappa[parent]
        else:
            new_kappa[i] = np.random.choice(np.array([0,2])) #with mutation rate kappa can take any of the two 0,2


    for i in range(N):
        kappa[i] = new_kappa[i]
        ownimage[i] = 1


#==================================================================
# Simulation and visualization
frequencies_sequence=np.zeros((num_generations,2))
frequencies_kappa = {num: 0 for num in [0, 2]}
C_global_cum = np.zeros(num_generations)


for gen in tqdm(range(num_generations), desc="Simulating"):
    Cg = play_games(kappa, ownimage, payoff,max_games, b, c)
    if gen == 0:
        C_global_cum[gen] = Cg
    else:
        C_global_cum[gen] = C_global_cum[gen-1] + Cg

    data_kappa = kappa
    for num in [0, 2]:
        frequencies_kappa[num] += np.sum(data_kappa == num) / num_agents
    frequencies_sequence[gen, :] = list(frequencies_kappa.values())
    new_generation(kappa, ownimage, payoff,mutation_rate)



# ===========================================
rows, _ = frequencies_sequence.shape
divisors = np.arange(1, rows + 1).reshape(-1, 1)
# Divide each row by the corresponding divisor
kappa_sequence = frequencies_sequence / divisors
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
fig, axes = plt.subplots(2, 2, figsize=(16, 10))

label_mat = ['upstream', 'downstream', 'allD']
colorbox = ['red', 'green', 'blue']

# ---- κ frequencies ----
for i in range(2):
    axes[0, i].plot(time, kappa_sequence[:, i],
                    color=colorbox[i], label=label_mat[i])
    axes[0, i].legend('upper left')
    axes[0, i].set_ylabel('⟨frequency⟩')

# ---- cooperation ----


axes[1, 0].plot(time, C_global_avg, color='black', lw=2)
axes[1, 0].set_title('Global cooperation')

for ax in axes[1]:
    ax.set_xlabel('Time')
    ax.set_ylabel('⟨cooperation⟩')

plt.tight_layout()
plt.savefig(f'coop_and_kappa_N={num_agents}_time={num_generations}.png', dpi=300)
plt.show()

