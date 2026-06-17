import matplotlib.pyplot as plt


plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'Times', 'DejaVu Serif']
plt.rcParams['mathtext.fontset'] = 'stix'

# Number values
n_list = [10,20,30,40,50,100,200,300,400,500,600,700,800,900,1000]

# Data columns taken from the respective folders of N=the number from n_list
upstream =    [30.9,30.7,27.0,26.5, 25.7, 12.8, 2.6, 1.4,1.0,0.8,0.7,0.6,0.5,0.5,0.5]

downstream =  [37.6,42.9,47.6,52.5, 56.0, 80.7, 96.0, 98.4,98.8,99.0,99.2,99.3,99.4,99.4,99.4]

defectors = [31.5,26.4,24.4,20.9, 18.2, 6.5, 0.4, 0.2,0.2,0.2,0.1,0.1,0.1,0.1,0.1]

total_coop = [65.3,66.4,64.8,65.2, 64.8, 69.5, 65.8, 56.9,49.8,44.4,39.9,36.4,33.0,30.3,28.1]


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