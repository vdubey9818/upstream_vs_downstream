import numpy as np
import matplotlib.pyplot as plt
import os
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import LinearSegmentedColormap

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'Times', 'DejaVu Serif']
plt.rcParams['mathtext.fontset'] = 'stix'

#=========================================================================
N_values = list(range(10, 201, 10))
max_N = max(N_values)
max_k = max_N-1
row_index=max_k-1


# Initialize matrices
f_up = np.full((row_index, len(N_values)), np.nan)
f_def = np.full((row_index, len(N_values)), np.nan)
C = np.full((row_index, len(N_values)), np.nan)

#extract data from the respective folders
for j, N in enumerate(N_values):
    file_path = f"N={N}/k_vs_frequencies_N={N}.txt"
    data = np.loadtxt(file_path)

    k_vals = data[:, 0].astype(int)
    index_vals=k_vals-2

    f_up[index_vals, j] = data[:, 1]
    f_def[index_vals, j] = data[:, 2]
    C[index_vals, j] = data[:, 3]

#white color for low values
def hex_cmap(hex_color, name):
    return LinearSegmentedColormap.from_list(name, ["#ffffff", hex_color])

# Create subplots
fig, axs = plt.subplots(2, 2, figsize=(8, 5))

#asign color and labels
plots = [
    (f_up, r"$x_U$", hex_cmap("#FF0000", "coral")),
    (f_def, r"$x_D$", hex_cmap("#6082B6", "blue")),
    (C, r"$C_T$", hex_cmap("#555555", "grey"))
]

# Assign specific positions
positions = [
    (0, 0),  # Upstream
    (1, 0),  # Defectors
    (1, 1)   # Cooperation level
]

#ploting
for ax, (matrix, title, cmap), (i,j) in zip(axs.flat,plots, positions):
    ax=axs[i,j]
    im = ax.imshow(matrix,
                   origin='lower',
                   aspect='auto',
                   cmap=cmap,
                   interpolation='none',vmin=0.0, vmax=1.0)

    # ax.set_title(title,fontsize=20)
    ax.set_xlabel(r"$N$",fontsize=15)
    ax.set_ylabel(r"$k$",fontsize=15)

    # y ticks setting
    ytick_vals = list(range(2, max_N+1, 30))
    ytick_pos = [k - 2 for k in ytick_vals]
    ax.set_yticks(ytick_pos)
    ax.set_yticklabels(ytick_vals,fontsize=10)

    # x ticks setting
    ax.set_xlim(0, len(N_values)-1)
    xtick_positions = list(range(0, len(N_values), 3))
    xtick_labels = [N_values[i] for i in xtick_positions]
    ax.set_xticks(xtick_positions)
    ax.set_xticklabels(xtick_labels,fontsize=10)

    # Create colorbar axis
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="6%", pad=0.05)
    cbar = fig.colorbar(im, cax=cax)
    cbar.ax.tick_params(labelsize=10)

# Remove the unused 2th subplot
fig.delaxes(axs[0, 1])
plt.tight_layout()
plt.savefig('number_vs_degree_up_def.png',dpi=300)


#===============================================================================
#------ploting the zoomed version the insets of the figure------
#===============================================================================

# --- ZOOMED UPSTREAM PLOT ---

k_min, k_max = 2, 8
row_start = k_min - 2
row_end   = k_max - 2

col_start = N_values.index(150)
col_end   = N_values.index(170)

zoom_up = f_up[row_start:row_end+1, col_start:col_end+1]

fig, ax = plt.subplots(figsize=(4,3))

im = ax.imshow(zoom_up,
               origin='lower',
               aspect='auto',
               cmap=hex_cmap("#FF0000", "coral"),
               interpolation='none',vmin=0.0, vmax=1.0)

# ax.set_title("Upstream (Zoomed)")
# ax.set_xlabel("N")
# ax.set_ylabel("k")

# ticks
k_vals = list(range(k_min, k_max+1, 2))
ytick_positions = [k - k_min for k in k_vals]

ax.set_yticks(ytick_positions)
ax.set_yticklabels(k_vals)

N_zoom = N_values[col_start:col_end+1]
ax.set_xticks(range(len(N_zoom)))
ax.set_xticklabels(N_zoom)

# control tick fontsize
ax.tick_params(axis='both', labelsize=30)

plt.tight_layout()
plt.savefig('zoomed_up.png',dpi=300)



# --- ZOOMED Defector PLOT ---

k_min, k_max = 2, 8
row_start = k_min - 2
row_end   = k_max - 2

col_start = N_values.index(150)
col_end   = N_values.index(170)

zoom_def = f_def[row_start:row_end+1, col_start:col_end+1]

fig, ax = plt.subplots(figsize=(4,3))

im = ax.imshow(zoom_def,
               origin='lower',
               aspect='auto',
               cmap=hex_cmap("#6082B6", "blue"),
               interpolation='none',vmin=0.0, vmax=1.0)

# ax.set_title("Upstream (Zoomed)")
# ax.set_xlabel("N")
# ax.set_ylabel("k")

# ticks
k_vals = list(range(k_min, k_max+1, 2))
ytick_positions = [k - k_min for k in k_vals]

ax.set_yticks(ytick_positions)
ax.set_yticklabels(k_vals)

N_zoom = N_values[col_start:col_end+1]
ax.set_xticks(range(len(N_zoom)))
ax.set_xticklabels(N_zoom)

# control tick fontsize
ax.tick_params(axis='both', labelsize=30)

plt.tight_layout()
plt.savefig('zoomed_def.png',dpi=300)



# --- ZOOMED cooperation PLOT ---

k_min, k_max = 2, 8
row_start = k_min - 2
row_end   = k_max - 2

col_start = N_values.index(150)
col_end   = N_values.index(170)

zoom_coop = C[row_start:row_end+1, col_start:col_end+1]

fig, ax = plt.subplots(figsize=(4,3))

im = ax.imshow(zoom_coop,
               origin='lower',
               aspect='auto',
               cmap=hex_cmap("#555555", "grey"),
               interpolation='none',vmin=0.0, vmax=1.0)


# ax.set_xlabel("N")
# ax.set_ylabel("k")

# ticks
k_vals = list(range(k_min, k_max+1, 2))
ytick_positions = [k - k_min for k in k_vals]

ax.set_yticks(ytick_positions)
ax.set_yticklabels(k_vals)

N_zoom = N_values[col_start:col_end+1]
ax.set_xticks(range(len(N_zoom)))
ax.set_xticklabels(N_zoom)

# control tick fontsize
ax.tick_params(axis='both', labelsize=30)

plt.tight_layout()
plt.savefig('zoomed_coop.png',dpi=300)
plt.show()