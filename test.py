import commands

data = "start minpool 4 3"
z = data[len(commands.START_MINPOOL):].split() #take the remaining part of the command as the amount of zeros
print(z)

z1 = int(z[0])
z2 = int(z[1])

print(z1)
print(z2)
