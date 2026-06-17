import numpy as np
import random
import matplotlib.pyplot as plt


plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'Times', 'DejaVu Serif']
plt.rcParams['mathtext.fontset'] = 'stix'



data = np.loadtxt("k_vs_frequencies_N=150.txt")

k_list=data[:,0]
up_list=data[:,1]
def_list=data[:,2]
coop_list=data[:,3]

plt.figure(figsize=(8,6))

plt.plot(k_list,up_list,marker='o',markersize=3.0,color='#FF0000')
plt.plot(k_list,def_list,marker='o',markersize=3.0,color='#6082B6')
plt.plot(k_list,coop_list,marker='o',markersize=3.0,color='#555555')


plt.grid(True)
plt.title(r'$N=150$',fontsize=30)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)

plt.xlabel(r"$k$",fontsize=30)
plt.tight_layout()
plt.savefig('Degree_vs_UDf.png',dpi=300)
plt.show()