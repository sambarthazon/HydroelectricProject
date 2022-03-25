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


# Plant
plant = ['Plant 1', 'Plant 2']


# Xct variable : Turbined volume in plant c at period t (minFlowct < columnsXct < maxFlowct)
# Just for the compilation
minFlowct = 0
maxFlowct = 100

columnsXct = {plant[0]: [LpVariable("TurbinedVolume", minFlowct, maxFlowct, cat="Float")],
           plant[1]: [LpVariable("TurbinedVolume", minFlowct, maxFlowct, cat="Float")]}

linesXct = period

Xct = pd.DataFrame(columnsXct, index=linesXct)
# print("\n---------- Xct ----------\n", Xct)
# End Xct variable



# Yct variable : Discharged volume in plant c at period t (minWeirct < columnsYct < maxWeirct)
# Just for the compilation
minWeirct = 0
maxWeirct = 1000

columnsYct = {plant[0]: [LpVariable("DischargedVolume", minWeirct, maxWeirct, cat="Float")],
           plant[1]: [LpVariable("DischargedVolume", minWeirct, maxWeirct, cat="Float")]}

linesYct = period

Yct = pd.DataFrame(columnsYct, index=linesYct)
# print("\n---------- Yct ----------\n", Yct)
# End Yct variable



# Vct variable : Tank volume in plant c at period t
columnsVct = {plant[0]: [LpVariable("100", 100, cat="Float")],
           plant[1]: [LpVariable("230", 100, cat="Float")]}

linesVct = period

Vct = pd.DataFrame(columnsVct, index=linesVct)
# print("\n---------- Vct ----------\n",, Vct)
# End Vct variable



# ANCct variable : ??? in plant c at period t
columnsANCct = {plant[0]: 300,
           plant[1]: 300}

linesANCct = period

ANCct = pd.DataFrame(columnsANCct, index=linesANCct)
# print("\n---------- ANCct ----------\n", ANCct)
# End ANCct variable



InitialVolumec = 360

# Number of active turbines
NBctn = LpVariable("ActiveTurbines", cat="Binary")

# for i in plant:
#     for j in period:
        
prob += 2*Xct['Plant 1']['Day 1'], "Objective Function"

prob += Vct['Plant 1']['Day 2'] == ANCct['Plant 1']['Day 1'] + Vct['Plant 1']['Day 1'] - Xct['Plant 1']['Day 1'] - Yct['Plant 1']['Day 1'], "Tank volume of the first plant"
prob += Vct['Plant 1']['Day 1'] == InitialVolumec, "Initial volume in each tank"

# faire conversion entre m^2/s en hectom^2/jour



# Objection Function
# prob += lpSum(lpSum((2)for c in range(1, 2))for p in range(1, 30)), "Objective Function"

prob += lpSum(lpSum((2*Vct[c][p])for c in range(len(plants)))for p in range(len(days))), "Objective Function"

# Constraints to start with init volume
prob += Vct[0][0] == InitVolume[0]
prob += Vct[1][0] == InitVolume[1]


# Constraints to finish with final volume
prob += Vct[0][29] == FinalVolume[0]
prob += Vct[1][29] == FinalVolume[1]


for plant in range(len(plants)):
    for day in range(len(days)):
        # For each day
        if day == 0:
            # If day 1
            prob += Vct[plant][day+1] == ANCct[plant][day] + Vct[plant][day] - Xct[plant][day] - Yct[plant][day]
        elif day < 29:
            # If day 2 to 29
            if plant == 0:
                # If plant 1
                prob += Vct[plant][day+1] == ANCct[plant][day] + Vct[plant][day] - Xct[plant][day] - Yct[plant][day]
            elif plant == 1:
                # If plant 2
                prob += Vct[plant][day+1] == ANCct[plant][day] + Vct[plant][day] - Xct[plant][day] - Yct[plant][day] + Xct[0][day] + Yct[0][day]
            else:
                # Else
                print("Error plant")
        elif day == 29:
            # If day 30
            if plant == 0:
                # If plant 1
                prob += Vct[plant][29] == FinalVolume[0]
                prob += Vct[plant][day] == ANCct[plant][day] + Vct[plant][day] - Xct[plant][day] - Yct[plant][day]
            elif plant == 1:
                # If plant 2
                prob += Vct[plant][29] == FinalVolume[1]
                prob += Vct[plant][day] == ANCct[plant][day] + Vct[plant][day] - Xct[plant][day] - Yct[plant][day] + Xct[0][day] + Yct[0][day]
            else:
                # Else
                print("Error plant")
        else:
            # Else
            print("Error day")

# Constrains
# prob += Pct <= 2*Xcn, "Power produced by each plant"
# Variables en hectom^2/jour (conversion : m2/s = 0,086400 hecto^m2/jour)
# prob += Vct.loc['Day 1'][1] == ANCc1t + Vct.loc['Day 1'][1] - Xct.loc['Day 1'][1] - Yct.loc['Day 1'][1], "Tank volume of the first plant"
# prob += Vct.loc['Day 1'][1] == InitialVolumec, "Initial volume in each tank"
# prob += Vct30 == FinalVolumec, "Final volume in each tank"

prob.solve()
Xct['Plant 1']['Day 1'] = pulp.value(Xct.iloc[0, 0])
Yct['Plant 1']['Day 1'] = pulp.value(Yct.iloc[0, 0])
print("\n---------- Xct ----------\n", Xct)
print("\n---------- Yct ----------\n", Yct)