from matplotlib import pyplot as plt
import numpy as np
import csv
import matplotlib.cbook as cbook

x = []
y = []
z = []

with open ("Experiments/HC-500-1600.csv", "r") as csvfile:
    plots = csv.reader(csvfile, delimiter =",")
    for row in plots:
        x.append(int(row[2]))
        z.append(int(row[0]))
        y.append(float(row[1]))

# Plot...
plt.scatter(x, y, c=z, s=50)
plt.gray()
print(x)
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
