import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from matplotlib.patches import FancyArrowPatch

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'Times', 'DejaVu Serif']
# -------------------------------------------------------
# Parameters (edit according to region in the voxel plot)
# -------------------------------------------------------
b = 1
c = 0.1
h = 0.7
g_u = 0.8
g_d = 0.3

A = np.array([
    [h*(b-c), g_u*b - h*c, -c*h],
    [b*h - g_u*c, g_d*(b-c), 0],
    [h*b, 0, 0]
])

mu = 0.001


def replicator_additive(t, x):
    f = A @ x
    phi = x @ f
    n = len(x)

    return x * (f - phi) + mu * (1 - 3 * x)


#-------------------------------------------------
#convert berrycentric to cartesian coordinate (2d)
# ------------------------------------------------

V1 = np.array([0, 0])
V2 = np.array([1, 0])
V3 = np.array([0.5, np.sqrt(3)/2])

def bary_to_cartesian(x):
    return x[0]*V1 + x[1]*V2 + x[2]*V3

# -------------------------------
# Ploting
# -------------------------------
fig, ax = plt.subplots(figsize=(6,4.5))

triangle = np.array([V1, V2, V3, V1])
ax.plot(triangle[:,0], triangle[:,1], 'k',linewidth=2 )

resolution = 10
T = 300


for x1 in np.linspace(0.00, 1.0, resolution):
    for x2 in np.linspace(0.0, 1.0, resolution):
        if x1 + x2 < 1.0:

            x0 = np.array([x1, x2, 1-x1-x2])

            sol = solve_ivp(replicator_additive, [0, T], x0, max_step=0.1)

            traj = np.array([bary_to_cartesian(sol.y[:,i]) for i in range(sol.y.shape[1])])

            # ---- Plot trajectory (same color)
            ax.plot(traj[:,0], traj[:,1], color='black', linewidth=0.8)

            # ---- Add small arrows along trajectory
            arrow_spacing = 500  # larger = fewer arrows

            for k in range(0, len(traj)-1, arrow_spacing):
                arrow = FancyArrowPatch((traj[k,0], traj[k,1]),
                        (traj[k+1,0], traj[k+1,1]),
                        arrowstyle='->',
                        mutation_scale=10,
                        linewidth=0.5,
                        color='black')
                ax.add_patch(arrow)

# Vertex labels
ax.text(V1[0]-0.12, V1[1]-0.06, "Upstream",fontsize=20)
ax.text(V2[0]-0.25, V2[1]-0.06, "Downstream",fontsize=20)
ax.text(V3[0]-0.12, V3[1]+0.03, "Defector",fontsize=20)

ax.set_aspect('equal')
ax.axis('off')
plt.tight_layout()
plt.savefig('phase_diagram.png', dpi=300)
plt.show()