from pyscipopt import Model, quicksum
import numpy as np

model = Model("try")
x = model.addVar("x")
y = model.addVar("y")
z = [[model.addVar("({}, {})".format(i,j)) for i in range(5)] for j in range(5)]

model.addCons(2 * x + y <= 10, "costs")
model.addCons(x + quicksum(z[i][j] for i in range(5) for j in range(5)) <= 30, "weight")

model.setObjective( x + y , "maximize")
model.optimize()

if model.getStatus() != 'optimal':
    print('LP is not feasible!')
else:
    print("Optimal value: %f" % model.getObjVal())
    print("x: = %f" % model.getVal(x))
    print("y: = %f" % model.getVal(y))

print(z)