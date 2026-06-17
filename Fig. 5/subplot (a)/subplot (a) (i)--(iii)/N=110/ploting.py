import numpy as np
import random
import matplotlib.pyplot as plt


data = np.loadtxt("k_vs_frequencies_N=110.txt")

k_list=data[:,0]
up_list=data[:,1]
def_list=data[:,2]
coop_list=data[:,3]

plt.plot(k_list,up_list,marker='o',color='red')
plt.plot(k_list,def_list,marker='o',color='blue')
plt.plot(k_list,coop_list,marker='o',color='black')
plt.grid()
plt.title('Strategy freq. vs Degree')
plt.savefig('new_born_updateN=110network.png')
plt.show()