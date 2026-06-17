import numpy as np
import os

# this code just take values from the corresponding folders and take the average

base_path = "."
ensembles = [f"ensemble{i}" for i in range(1, 6)]
N_values = [10,20,30,40,50,70,100,150,200,300,400,500,600,700,800,900,1000]

results = {}

for N in N_values:
    collected = []          # for κ frequencies
    collected_coop = []     # for cooperation

    for ens in ensembles:
        folder = os.path.join(base_path, ens, f"N={N}")

        for file in os.listdir(folder):

            # ---- κ sequence file ----
            if file.startswith(f"kd_sequenceN={N}") and file.endswith(".txt"):
                filepath = os.path.join(folder, file)
                data = np.loadtxt(filepath)

                last_row = data[-1]   # [up, down, def]
                collected.append(last_row)

            # ---- cooperation file ----
            if file.startswith(f"sequenceN={N}") and "global_coop_avg" in file:
                filepath = os.path.join(folder, file)
                data = np.loadtxt(filepath)

                last_val = data[-1]   # scalar
                collected_coop.append(last_val)

    collected = np.array(collected)
    collected_coop = np.array(collected_coop)

    mean_vals = np.mean(collected, axis=0)
    mean_coop = np.mean(collected_coop)

    results[N] = {
        "mean": mean_vals * 100,
        "coop": mean_coop * 100
    }

# ---- Print ----
for N in results:
    mean = results[N]["mean"]
    coop = results[N]["coop"]

    print(f"\nN = {N}")
    print(f"Upstream   = {mean[0]:.1f}")
    print(f"Downstream = {mean[1]:.1f}")
    print(f"Defectors  = {mean[2]:.1f}")
    print(f"Cooperation= {coop:.1f}")