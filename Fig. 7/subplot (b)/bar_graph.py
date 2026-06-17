import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'Times', 'DejaVu Serif']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'


data = np.loadtxt("k_vs_frequencies_N=150.txt")

k_list = data[:,0]

Avg_U = data[:,8]
E_UD  = data[:,10]

# ----------------------------
# Calculating gamma1
# ----------------------------
score2 = Avg_U / E_UD

# Normalize
score2_norm = score2 / np.max(score2)

# ----------------------------
# Plot
# ----------------------------
plt.figure(figsize=(8,6))


bars=plt.bar(k_list, score2_norm, width=0.6, color='#BDB5D5')


# Add hatch only to maximum bar
# ----------------------------
max_idx = np.argmax(score2_norm)
bars[max_idx].set_hatch('//')
bars[max_idx].set_linewidth(2)

#-----------------------------

plt.xlabel(f"$k$", fontsize=40)
plt.ylabel(f"$\gamma_1(k)$", fontsize=40)

# plt.title(r"$N=150$", fontsize=20)

plt.xticks(fontsize=30)
plt.yticks(fontsize=30)

plt.grid()

plt.tight_layout()

plt.savefig('Normalized_cluster_strength_bar.png')
plt.show()