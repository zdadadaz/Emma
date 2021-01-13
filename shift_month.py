# day is the samllest unit in time

import numpy as np
import pandas as pd
from pulp import *

# Set
B = 0
M = [i for i in range(1,3)]
F = [i for i in range(3,8)]
P = [i for i in range(8,13)]
T = [i for i in range(0, 31)]

# Data
Total_employees = 1 + len(M) + len(F) + len(P)
exp_df = pd.read_csv('./exp_off.csv', index_col=0).values
dayoff_df = pd.read_csv('./day_off.csv', index_col=0).values
minWorkPerDay = 7
minAnePerDay = 5
ane = [1 for i in range(Total_employees)]
ane[0] = 0
ane[-2:] = [0,0]
kimochi_ratio = [1 for i in range(Total_employees)]
alldayoff = set([i for i in range(3,31,7)]) # Monday day off
weekend = set([i for i in range(1,31,7)] + [i for i in range(2,31,7)]) # Monday day off

# Variable 
Xbt = {}
for t in T:
    for i in range(Total_employees):
        Xbt[(i,t)] = LpVariable(str(t)+'_'+str(i), lowBound=0, upBound=1, cat='Integer') #'Continuous', 'Integer'
Yb = {}
for i in range(Total_employees):
    Yb[i] = LpVariable('kimo_'+str(i), lowBound=0, upBound=1, cat='Integer') #'Continuous', 'Integer'

# Objectives:
# prob = LpProblem("Mixed Problem", LpMaximize)
prob = LpProblem("Mixed Problem", LpMinimize)
# prob += lpSum([Xbt[(i,t)] for i in range(Total_employees) for t in T]) - lpSum([Yb[i]*kimochi_ratio[i] for i in range(Total_employees)])
prob += lpSum([Xbt[(i,t)] for i in range(Total_employees) for t in T]) + lpSum([Yb[i]*kimochi_ratio[i] for i in range(Total_employees)])
for t in T:
    if t in alldayoff: 
        prob += lpSum([Xbt[(i,t)] for i in range(Total_employees)]) <= 0 # all worker day off
    else:
        if t in weekend:
            for j in P[:-1]:
                prob += Xbt[(j,t)] == 0 # part-time weekend off
        prob += lpSum([Xbt[(i,t)] for i in range(3)]) >= 2 # at least two manager
        prob += lpSum([Xbt[(i,t)] for i in range(Total_employees)]) >= minWorkPerDay # minimum worker per day
        prob += lpSum([Xbt[(i,t)]*ane[i] for i in range(Total_employees)]) >= minAnePerDay # minimum Ane worker per day
        # day off can't work
        for i in range(Total_employees):
            if dayoff_df[i][t] == 1:
                prob += Xbt[(i,t)] == 0
        # exp day work, kimochi warui
        for i in range(Total_employees):
            prob += exp_df[i][t] + Xbt[(i,t)] <= 1+Yb[i]
prob.solve()
res ={}
kimo = {}
for v in prob.variables():
    if v.name[0] =='k':
        print(v.name, "=", v.varValue)
    else:
        tmp = v.name.split('_')
        res[(int(tmp[0]), int(tmp[1]) )] = v.varValue

# for i in range(Total_employees):
#     tmp = []
#     for t in T:
#         tmp += [res[(t,i)]]
#     print(tmp)

# for t in T:
#     for i in range(Total_employees):
#         if res[(t,i)] >0.1 and exp_df[i][t]>0:
#             print('kimochi',i,t)

out_dict = {}
for t in T:
    tmp = []
    for i in range(Total_employees):
        if res[(t,i)] > 0.2:
            tmp += ['work']
        else:
            tmp += ['off']
    out_dict[t+1] = tmp
# print(out_dict)
out_df = pd.DataFrame.from_dict(out_dict)
out_df.to_csv('output.csv',index=False)