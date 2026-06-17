import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'Times', 'DejaVu Serif']
plt.rcParams['mathtext.fontset'] = 'stix'


# Number values
n_list = [10,20,30,40,50,70,100,150,200,300,400,500,600,700,800,900,1000]

# Data columns taken from average values from the taking_average.py code
upstream =    [16.4, 12.0, 10.8, 10.3, 10.8, 12.5, 16.2, 21.9, 27.5, 34.1, 37.8,40.2, 42.1, 44.5, 45.7, 47.4, 49.1]

downstream =  [52.7, 61.1, 63.2, 63.3, 62.4, 60.4, 55.9, 47.3, 41.0,35.0, 32.7, 31.1, 30.2,29.8, 29.2, 29.1, 28.8]

defectors = [30.9, 26.9, 26.0, 26.4, 26.7, 27.2, 27.9, 30.8, 31.5, 30.9, 29.5, 28.7,27.7, 25.6, 25.1, 23.5, 22.1]

total_coop = [68.4, 71.7, 72.0, 71.2, 70.5, 69.3, 67.5, 63.4, 61.7, 60.9,61.2,60.9,61.2,62.3, 62.2, 62.9, 63.3]


# Convert percentages to fractions (0 to 1 scale)
upstream = [x/100 for x in upstream]
downstream = [x/100 for x in downstream]
defectors = [x/100 for x in defectors]
total_coop = [x/100 for x in total_coop]

plt.figure(figsize=(8,6))

plt.plot(n_list, upstream, color='#FF0000', linewidth=2.5)
plt.plot(n_list, downstream, color='#4F7942', linewidth=2.5)
plt.plot(n_list, defectors, color='#6082B6', linewidth=2.5)
plt.plot(n_list, total_coop, color='#555555', linewidth=2.5)


plt.xlabel(r"$N$",fontsize=30)
plt.title(r"$k=N-1$",fontsize=30)
plt.xticks([100, 300, 500, 700, 900], fontsize=25)
plt.yticks(fontsize=25)
plt.grid(True)
plt.tight_layout()
plt.savefig('Up_Down_Def_Vs_N.png', dpi=300)
plt.show()