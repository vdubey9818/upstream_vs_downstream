import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'Times', 'DejaVu Serif']
plt.rcParams['mathtext.fontset'] = 'stix'


# Number values
n_list = [10,20,50,100,200,300,400,500,600,700,800,900,1000,1100,1200,1500]

# Data columns taken from the respective folders of N=the number from n_list
upstream =    [14.3,13.6, 11.9, 13.3, 18.9, 24.7, 29.6, 34.0, 37.4, 40.3, 42.4, 44.0,45.8,46.3,47.4,49.5]

downstream =  [48.7,59.2, 63.7, 63.2, 59.3, 55.6, 52.4, 50.1, 48.0, 46.9, 46.3, 46.0,45.5,45.8,45.4,44.8]

defectors = [37.0,27.2, 24.4, 23.5, 21.8, 19.7, 18.0, 15.9, 14.6, 12.8, 11.3, 10.0,8.7,7.9,7.1,5.7]

total_coop = [62.8,72.1, 73.8, 72.4, 69.8, 67.9, 66.5, 65.7, 64.4, 64.1, 63.8, 63.8,63.5,63.5,62.9,60.8]


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
plt.xticks([100, 400, 700, 1000, 1300], fontsize=25)
plt.yticks(fontsize=25)
plt.grid(True)
plt.tight_layout()
plt.savefig('Up_Down_Def_Vs_N.png', dpi=300)
plt.show()