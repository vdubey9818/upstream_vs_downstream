import matplotlib.pyplot as plt

# Degree values
n_list = [20,50,100,200,300,400,500,600,700,800]

# Data columns
upstream =    [11.7, 10.8, 16.4, 28.1, 33.5, 38.6,40.3,41.4,44.2,44.3]

downstream =  [63.5, 61.7, 55.6, 41.1, 34.3, 33.5,30.8,29.9,29.9,28.6]

defectors = [24.8, 27.5, 27.9, 30.8, 32.2, 27.9,28.9,28.7,25.9,27.1]

total_coop = [73.9, 69.6, 67.6, 62.2, 59.8, 62.6,60.7,60.1,62.1,60.4]


plt.figure(figsize=(8,6))

plt.plot(n_list, upstream, 'r-o', label='Upstream')
plt.plot(n_list, downstream, 'g-o', label='Downstream')
plt.plot(n_list, defectors, 'b-o', label='Defectors')
plt.plot(n_list, total_coop, 'k-o', label='Total Cooperation')

plt.xlabel("Number of Individuals (N)")
plt.ylabel("Percentage")
plt.title("Strategy Frequencies vs N")
plt.legend()
plt.grid(True)
plt.savefig('Up_Down_Def_Vs_N.png', dpi=300)
plt.tight_layout()
plt.show()
