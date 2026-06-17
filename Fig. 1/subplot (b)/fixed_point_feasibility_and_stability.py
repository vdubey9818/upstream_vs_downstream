import numpy as np
import matplotlib.pyplot as plt


plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'Times', 'DejaVu Serif']
plt.rcParams['mathtext.fontset'] = 'stix'

# =========================
# 1. LOAD DATA (robust to NaN/NA)
# =========================
data = np.genfromtxt("jacobian_data_downstream.txt", missing_values="NA", filling_values=np.nan)

h  = data[:, 0]
gu = data[:, 1]
gd = data[:, 2]

J11 = data[:, 3]
J12 = data[:, 4]
J21 = data[:, 5]
J22 = data[:, 6]

# =========================
# 2. PARAMETERS
# =========================
b = 1.0
c = 0.1
mu = 0.001

# =========================
# 3. Safe devision to avoid nan
# =========================
def safe_div(num, den):
    out = np.full_like(num, np.nan, dtype=float)
    np.divide(num, den, out=out, where=(den != 0))
    return out

# =========================
# 4. COMPUTE FIXED POINT
# =========================

# common denominator
D1 = b*(gd - gu) + c*(-gd + h)
D2 = (b - c)*gd*D1

# x*
x_term2 = safe_div(np.ones_like(D1), D1)
xfixed =  mu * x_term2

# y*
y_num2 = -2*b*gd + 2*c*gd + b*gu - c*h
y_term2 = safe_div(y_num2, D2)
yfixed = 1 + mu * y_term2

# =========================
# 5. FEASIBILITY CONDITION
# =========================
valid = (
    (xfixed >=0) & (xfixed < 1) &
    (yfixed >0) & (yfixed <= 1) &
    (xfixed + yfixed < 1)
)

# remove NaNs
valid = valid & (~np.isnan(xfixed)) & (~np.isnan(yfixed))

# =========================
# 6. EIGENVALUE STABILITY
# =========================
eigvals = []

for i in range(len(J11)):
    if np.any(np.isnan([J11[i], J12[i], J21[i], J22[i]])):
        eigvals.append([np.nan, np.nan])
    else:
        vals = np.real(np.linalg.eigvals([[J11[i], J12[i]], [J21[i], J22[i]]]))
        eigvals.append(np.sort(vals))

eigvals = np.array(eigvals)

# largest eigenvalue (controls stability)
lambda_max = eigvals[:, 1]

# =========================
# 7. RESHAPE GRID
# =========================
n = int(round(len(h) ** (1/3)))

valid_grid = valid.reshape((n, n, n))
lambda_max_grid = lambda_max.reshape((n, n, n))

# =========================
# 8. FINAL REGION
# =========================
stable = (lambda_max_grid < 0)
stable = stable & (~np.isnan(lambda_max_grid))

# combine: existence + stability
final_region = valid_grid & stable

# =========================
# 9. VOXEL PLOT
# =========================
fig = fig = plt.figure(figsize=(5, 4))
ax = fig.add_subplot(111, projection='3d')

alpha = 0.4 # adjust to manage the contrast of the plot
colors = np.zeros(final_region.shape + (4,), dtype=float)

# red = exists + stable
colors[final_region] =[1, 0, 0, alpha]

# blue = everything else
colors[~final_region] =  [0, 0, 1, alpha]

ax.voxels(np.ones_like(final_region, dtype=bool), facecolors=colors)

# ax.set_title("Stable & Feasible Fixed Point Region")
ax.set_xlabel(r'$h$',fontsize=25)
ax.set_ylabel(r'$g_{\rm{U}}$',fontsize=25)
ax.set_zlabel(r'$g_{\rm{Dn}}$',fontsize=25)

# =========================
# 10. NICE TICKS
# =========================
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

plt.subplots_adjust(left=0.05, right=1.0, top=0.90, bottom=0.05)
plt.savefig('feasible_stable_voxel.png', dpi=300)
np.save("region_fp2.npy", final_region)  #save this to find the bistable region
plt.show()