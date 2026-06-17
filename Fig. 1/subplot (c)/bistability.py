import numpy as np
import matplotlib.pyplot as plt


plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'Times', 'DejaVu Serif']
plt.rcParams['mathtext.fontset'] = 'stix'

# ==========================================
# 1. LOAD REGIONS to get the bistable region
# ==========================================
R1 = np.load("region_fp1.npy")
R2 = np.load("region_fp2.npy")

# sanity check
print("Shape FP1:", R1.shape)
print("Shape FP2:", R2.shape)

# ===============================
# 2. INTERSECTION (BISTABILITY)
# ===============================
bistable = R1 & R2


# =========================
# 4. VISUALIZATION
# =========================
fig = plt.figure(figsize=(5, 4))
ax = fig.add_subplot(111, projection='3d')

colors = np.zeros(R1.shape + (4,), dtype=float)

# Only FP1 stable --- blue
colors[(R1 & ~R2)] = [0, 0, 1, 0.4]

# Only FP1 stable --- blue
colors[(~R1 & R2)] = [0, 0, 1, 0.4]

# Neither --- blue
colors[(~R1 & ~R2)] = [0, 0, 1, 0.4]

# BISTABLE --- Red 
colors[(R1 & R2)] = [1, 0, 0, 0.4]



ax.voxels(np.ones_like(R1, dtype=bool), facecolors=colors)
ax.set_xlabel(r'$h$',fontsize=25)
ax.set_ylabel(r'$g_{\rm{U}}$',fontsize=25)
ax.set_zlabel(r'$g_{\rm{Dn}}$',fontsize=25)


# =========================
# 10. NICE TICKS
# =========================
n=100
vals = np.linspace(0.01, 1.0, n)

# keep grid dense
ticks_dense = np.linspace(0, n-1, 5)

ax.set_xticks(ticks_dense)
ax.set_yticks(ticks_dense)
ax.set_zticks(ticks_dense)

# BUT only label 3 of them
labels = ['0', '', '0.5', '', '1']

ax.set_xticklabels(labels, fontsize=15)
ax.set_yticklabels(labels, fontsize=15)
ax.set_zticklabels(labels, fontsize=15)

ax.tick_params(axis='x', pad=1)
ax.tick_params(axis='y', pad=1)
ax.tick_params(axis='z', pad=1)

#saving plot

plt.subplots_adjust(left=0.05, right=1.0, top=0.90, bottom=0.05)
plt.savefig('feasible_stable_voxel.png', dpi=300)
plt.show()