import numpy as np
import random
import matplotlib.pyplot as plt


data = np.loadtxt("k_vs_frequencies_N=120.txt")

k_list=data[:,0]
up_list=data[:,1]
def_list=data[:,2]
coop_list=data[:,3]

plt.figure(figsize=(8,6))

plt.plot(k_list,up_list,marker='o',markersize=2.0,color='#FF0000')
plt.plot(k_list,def_list,marker='o',markersize=2.0,color='#6082B6')
plt.plot(k_list,coop_list,marker='o',markersize=2.0,color='#555555')

plt.grid(True)
plt.title(r'$N=120$',fontsize=20)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

plt.xlabel(r"$k$",fontsize=20)
plt.ylabel("Strategy frequency",fontsize=20)
plt.tight_layout()
plt.savefig('Degree_vs_UDf.png')
plt.show()