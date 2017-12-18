from matplotlib import pyplot as plt
import numpy as np
import csv
import matplotlib.cbook as cbook
import math
import matplotlib.mlab as mlab
x = []
y = []
z = []

x1 = []
y1 = []
z1 = []


with open ("Experiments/SA-500-1600-HARDCODED.csv", "r") as csvfile:
    plots = csv.reader(csvfile, delimiter =",")
    for row in plots:
        x.append(int(row[2]))
        z.append(int(row[0]))
        y.append(float(row[1]))
with open ("Experiments/SA-5-160000-T1250-HARDCODED.csv", "r") as csvfile:
    plots = csv.reader(csvfile, delimiter =",")
    for row in plots:
        x1.append(int(row[2]))
        z1.append(int(row[0]))
        y1.append(float(row[1]))


# Plot...
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax2 = fig.add_subplot()

yBar = np.mean(y)
yVar = np.var(y)
yS = yVar ** 0.5
n = len(y)

yBarAlternative = np.mean(y)
yVarAlternative = np.var(y)
ySAlternative = yVar ** 0.5
nalternative = len(y)


ymax = max(y)
xpos = y.index(ymax)
xmax = x[xpos]
zmax = z[xpos]

ax1.annotate( str(yBar), xy=(yBar, 0.000225), xytext=(yBar, 0.000225),
arrowprops=dict(facecolor='yellow', shrink=0.01),
)


ax = plt.gca()
ax.set_facecolor('blue')
ax.set_facecolor((1, 0, 0))
# plt.scatter(x, y, label = "Lijnvoering", c=z, s=5)

plt.plot(y,mlab.normpdf(y, yBar, yS))
#
# plt.gray()
# print(x)
# plt.xlabel("minuten")
# plt.ylabel("score")
# plt.title("SBG")
# plt.legend()
# cbar = plt.colorbar()
# cbar.set_label('# trajecten')

# use_colours = {"1": "red", "2": "green", "3": "blue", "4": "purple", "5": "yellow", "6": "Black", "7" : "grey"}
# if z > 2:
#     plt.scatter(x,y, label = 'min', color = 'red', s =5)
# else:
#     plt.scatter(x,y, label = 'min', color = 'green', s =5)

print((yS))
print (yBar)
# plt.plot(x,y)
plt.show()
#
# fname = cbook.get_sample_data("Experiments.csv", asfileobj=False)
# fname2 = cbook.get_sample_data("data_x_x2_x3.csv", asfileobj=False)
