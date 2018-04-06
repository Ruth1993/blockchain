import matplotlib.pyplot as plt

list = {}

x_values = range(7,16)
init_split = range(30,70,10)
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

for tr in init_split:
    y_values = []

    te = 100-tr

    for j in x_values:
        p = float(100)/float(tr+(te/j));
        new_tr = (p*float(tr))

        y_values.append(new_tr)

    print(y_values)   
    list[tr] = y_values
    plt.plot(x_values, y_values, colors[0])
    colors.remove([0])

plt.show()
