line = "152,506"
x, y = map(int, line.split(","))
f = open("results.txt", "w")
f.write(line)
print(type(x), x)