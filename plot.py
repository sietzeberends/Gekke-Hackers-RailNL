from matplotlib import pyplot as plt
import numpy as np
import csv
import matplotlib.cbook as cbook

x = []
y = []
z = []


with open ("Experiments/HC-5-160000.csv", "r") as csvfile:
    plots = csv.reader(csvfile, delimiter =",")
    for row in plots:
        x.append(int(row[2]))
        z.append(int(row[0]))
        y.append(float(row[1]))

# Plot...
fig = plt.figure()
ax1 = fig.add_subplot(111)



ymax = max(y)
xpos = y.index(ymax)
xmax = x[xpos]
zmax = z[xpos]

ax1.annotate( str(ymax), xy=(xmax, ymax), xytext=(xmax, ymax+20),
arrowprops=dict(facecolor='yellow', shrink=0.01),
)


ax = plt.gca()
ax.set_facecolor('blue')
ax.set_facecolor((1, 1, 0))
plt.scatter(x, y, label = "Lijnvoering", c=z, s=5)


plt.gray()
print(x)
plt.xlabel("minuten")
plt.ylabel("score")
plt.title("SBG")
plt.legend()
cbar = plt.colorbar()
cbar.set_label('# trajecten')

# use_colours = {"1": "red", "2": "green", "3": "blue", "4": "purple", "5": "yellow", "6": "Black", "7" : "grey"}
# if z > 2:
#     plt.scatter(x,y, label = 'min', color = 'red', s =5)
# else:
#     plt.scatter(x,y, label = 'min', color = 'green', s =5)

print(y)
# plt.plot(x,y)
plt.show()
#
# fname = cbook.get_sample_data("Experiments.csv", asfileobj=False)
# fname2 = cbook.get_sample_data("data_x_x2_x3.csv", asfileobj=False)
