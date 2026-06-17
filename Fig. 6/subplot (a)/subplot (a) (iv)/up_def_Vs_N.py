import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'Times', 'DejaVu Serif']
plt.rcParams['mathtext.fontset'] = 'stix'


# Number values
n_list = [10, 20,50,100,200,300,400,500,600,700,800]

# Data columns taken from the respective folders of N=the number from n_list
upstream =    [44.8, 42.9, 33.1, 30.3, 26, 26,26.2,26.5,26.4,26.6,26.1]

defectors = [55.2, 57.1, 66.9, 69.7, 74.0, 74.0,73.8,73.5,73.6,73.4,73.8]

total_coop = [41.1, 34.5, 14.8, 4.3, 0.3, 0.04,0.02,0.01,0.008,0.006,0.005]


# Convert percentages to fractions (0 to 1 scale)
upstream = [x/100 for x in upstream]
defectors = [x/100 for x in defectors]
total_coop = [x/100 for x in total_coop]


plt.figure(figsize=(8,6))

plt.plot(n_list, upstream, color='#FF0000', linewidth=2.5)
plt.plot(n_list, defectors, color='#6082B6', linewidth=2.5)
plt.plot(n_list, total_coop, color='#555555', linewidth=2.5)

plt.xlabel(r"$N$",fontsize=20)
plt.title(r"$k=N-1$",fontsize=20)


plt.xlabel(r"$N$",fontsize=30)
plt.title(r"$k=N-1$",fontsize=30)
plt.xticks([100, 300, 500, 700], fontsize=25)
plt.yticks(fontsize=25)
plt.grid()
plt.tight_layout()
plt.savefig('Up_Def_Vs_N.png', dpi=300)
plt.show()
