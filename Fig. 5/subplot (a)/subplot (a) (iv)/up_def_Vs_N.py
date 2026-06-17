import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'Times', 'DejaVu Serif']
plt.rcParams['mathtext.fontset'] = 'stix'

# Degree values
n_list = [10,20,50,100,200,300,400,500,600,700,800]

# Data columns taken from the respective folders of N=the number from n_list
upstream =    [9.5011628,3.2743465, 2.2975392, 2.4119615, 2.43740515, 2.45140097, 2.48037123, 2.49161364, 2.47696668, 2.50305186, 2.48328158]

defectors = [90.4988400,96.7256535, 97.7024608, 97.5880385, 97.56259485, 97.54859903, 97.51962877, 97.50838636, 97.52303332, 97.49694814, 97.51671842]

total_coop = [8.6193624, 1.64255374, 0.12202588, 0.05563624, 0.02641123, 0.01738372, 0.01307587, 0.01044952, 0.00862379, 0.00744999, 0.00645564]


# Convert percentages to fractions (0 to 1 scale)
upstream = [x/100 for x in upstream]
defectors = [x/100 for x in defectors]
total_coop = [x/100 for x in total_coop]


plt.figure(figsize=(8,6))

plt.plot(n_list, upstream, color='#FF0000', linewidth=2.5)
plt.plot(n_list, defectors, color='#6082B6', linewidth=2.5)
plt.plot(n_list, total_coop, color='#555555', linewidth=2.5)

plt.xlabel(r"$N$",fontsize=30)
plt.title(r"$k=N-1$",fontsize=30)
plt.xticks([100, 300, 500, 700], fontsize=25)
plt.yticks(fontsize=25)
plt.grid()
plt.tight_layout()
plt.savefig('Up_Def_Vs_N.png', dpi=300)
plt.show()
