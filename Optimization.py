from pulp import *
import pandas as pd
# Maybe use numpy and panda for data of parameters and sets

print("\n\n\n------------------ New run ------------------") # Debug

# Creation of the problem
prob = LpProblem("Hydroelectric_Problem", LpMaximize)


# Periode of the optimization
period = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7', 'Day 8', 'Day 9', 'Day 10',
         'Day 11', 'Day 12', 'Day 13', 'Day 14', 'Day 15', 'Day 16', 'Day 17', 'Day 18', 'Day 19', 'Day 20',
         'Day 21', 'Day 22', 'Day 23', 'Day 24', 'Day 25', 'Day 26', 'Day 27', 'Day 28', 'Day 29', 'Day 30']


print("\n---------- Xct ----------")
# Xct variable : Turbined volume in plant c at period t (minFlowct < columnsXct < maxFlowct)
# Just for the compilation
minFlowct = 0
maxFlowct = 100

columnsXct = {'Plant 1': [LpVariable("TurbinedVolume", minFlowct, maxFlowct, cat="Float")],
           'Plant 2': [LpVariable("TurbinedVolume", minFlowct, maxFlowct, cat="Float")]}

linesXct = period

Xct = pd.DataFrame(columnsXct, index=linesXct)
print(Xct)
# End Xct variable


print("\n---------- Yct ----------")
# Yct variable : Discharged volume in plant c at period t (minWeirct < columnsYct < maxWeirct)
# Just for the compilation
minWeirct = 0
maxWeirct = 1000

columnsYct = {'Plant 1': [LpVariable("DischargedVolume", minWeirct, maxWeirct, cat="Float")],
           'Plant 2': [LpVariable("DischargedVolume", minWeirct, maxWeirct, cat="Float")]}

linesYct = period

Yct = pd.DataFrame(columnsYct, index=linesYct)
print(Yct)
# End Xct variable


print("\n---------- Vct ----------")
# Vct variable : Tank volume in plant c at period t
columnsVct = {'Plant 1': [LpVariable("100", 100, cat="Float")],
           'Plant 2': [LpVariable("230", 100, cat="Float")]}

linesVct = period

Vct = pd.DataFrame(columnsVct, index=linesVct)
print(Vct)
# End Vct variable


plant = [Xct, Yct, Vct]

ANCc1t = 300
# Tableau pour chaque centrale
InitialVolumec = 360

# Number of active turbines
NBctn = LpVariable("ActiveTurbines", cat="Binary")

for i in plant(0, 2):
    for j in linesXct(0, 29):
        print(2*Xct.iloc[i, j])
        prob += 2*Xct.iloc[i, j], "Objective Function"


# faire conversion entre m^2/s en hectom^2/jour



# Objection Function
# prob += lpSum(lpSum((2)for c in range(1, 2))for p in range(1, 30)), "Objective Function"


# Constrains
# prob += Pct <= 2*Xcn, "Power produced by each plant"
# Variables en hectom^2/jour (conversion : m2/s = 0,086400 hecto^m2/jour)
prob += Vct.loc['Day 1'][1] == ANCc1t + Vct.loc['Day 1'][1] - Xct.loc['Day 1'][1] - Yct.loc['Day 1'][1], "Tank volume of the first plant"
prob += Vct.loc['Day 1'][1] == InitialVolumec, "Initial volume in each tank"
# prob += Vct30 == FinalVolumec, "Final volume in each tank"

prob.solve()
print(pulp.value(Yct.loc['Day 1'][1]))
print(pulp.value(Xct.loc['Day 1'][1]))