from itertools import product


ws = file('StationsHolland.csv','r',1)

for cell in rows: 
    x = list.append(cell)
for cell in ws.columns[C]: 
	y = list.append(cell)

coordinates = list(product(x(width), y(height)))
print(coordinates)
