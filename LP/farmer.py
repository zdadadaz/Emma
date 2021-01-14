import numpy as np
from pulp import *

# Set
I = [i for i in range(2)] # choc, plain
name = ['choc', 'plain']

# Data 
pricei = [4,2]
timei = [20,50]
milki = [250,200]
eggi = [4,1]
Fegg = 30
Fmilk = 5000
Day = 8*60

# Variable 
Xi = {}
for i in I:
    # Xi[i] = LpVariable(name[i], lowBound=0, cat='Continuous')
    Xi[i] = LpVariable(name[i], lowBound=0, cat='Integer')

# Objective
prob = LpProblem("Mixed Problem", LpMaximize)
prob += lpSum([pricei[i] * Xi[i] for i in I])

# Constraint
prob += lpSum([eggi[i] * Xi[i] for i in I])<=30 # egg
prob += lpSum([milki[i] * Xi[i] for i in I])<=5000 #
prob += lpSum([timei[i] * Xi[i] for i in I])<=8*60

prob.solve()

for v in prob.[variables():
    print(v.name, "=", v.varValue)