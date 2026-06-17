import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'Times', 'DejaVu Serif']
plt.rcParams['mathtext.fontset'] = 'stix'



# Number values
n_list = [10,20,50,100,200,300,400,500,600,700,800,900,1000,1100,1200,1500]

# Data columns taken from the respective folders of N=the number from n_list
upstream =    [5.7,3.6, 3.2, 4.7, 8.4, 11.4, 14.2, 16.7, 19.1, 20.3, 22.2, 23.7,25.0,26.0,27.0,30.5]

defectors = [94.3,96.4, 96.8, 95.1, 91.6, 88.6, 85.8, 83.3, 80.9, 79.7, 77.7, 76.3,75.0,74.0,73.0,69.5]

total_coop = [5.4,2.9, 1.2, 0.5, 0.3, 0.2, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1,0.1,0.1,0.1,0.1]

# Convert percentages to fractions (0 to 1 scale)
upstream = [x/100 for x in upstream]
defectors = [x/100 for x in defectors]
total_coop = [x/100 for x in total_coop]

print(len(upstream))

plt.figure(figsize=(8,6))

plt.plot(n_list, upstream, color='#FF0000', linewidth=2.5)
plt.plot(n_list, defectors, color='#6082B6', linewidth=2.5)
plt.plot(n_list, total_coop, color='#555555', linewidth=2.5)


plt.xlabel(r"$N$",fontsize=30)
plt.title(r"$k=N-1$",fontsize=30)
plt.xticks([100, 400, 700, 1000, 1300], fontsize=25)
plt.yticks(fontsize=25)
plt.grid()
plt.tight_layout()
plt.savefig('Up_Def_Vs_N.png', dpi=300)
plt.show()