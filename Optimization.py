from pulp import *
import pandas as pd



print("\n\n\n------------------ New run ------------------") # Debug

# Creation of the problem
prob = LpProblem("Hydroelectric_Problem", LpMaximize)


# Period of the optimization
days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7', 'Day 8', 'Day 9', 'Day 10',
         'Day 11', 'Day 12', 'Day 13', 'Day 14', 'Day 15', 'Day 16', 'Day 17', 'Day 18', 'Day 19', 'Day 20',
         'Day 21', 'Day 22', 'Day 23', 'Day 24', 'Day 25', 'Day 26', 'Day 27', 'Day 28', 'Day 29', 'Day 30']


# Plant
plants = ['Plant 1', 'Plant 2']


# Tank
tanks = ['Tank 1', 'Tank 2']



# Xct variable : Turbined volume in plant c at day t (minFlowct < columnsXct < maxFlowct)
# Just for the compilation
minFlowct = 0
maxFlowct = 100

columnsXct = {plants[0]: [LpVariable("TurbinedVolume", minFlowct, maxFlowct, cat="Float")],
           plants[1]: [LpVariable("TurbinedVolume", minFlowct, maxFlowct, cat="Float")]}

linesXct = days

Xct = pd.DataFrame(columnsXct, index=linesXct)
# print("\n---------- Xct ----------\n", Xct)
# End Xct variable



# Yct variable : Discharged volume in plant c at day t (minWeirct < columnsYct < maxWeirct)
# Just for the compilation
minWeirct = 0
maxWeirct = 1000

columnsYct = {plants[0]: [LpVariable("DischargedVolume", minWeirct, maxWeirct, cat="Float")],
           plants[1]: [LpVariable("DischargedVolume", minWeirct, maxWeirct, cat="Float")]}

linesYct = days

Yct = pd.DataFrame(columnsYct, index=linesYct)
# print("\n---------- Yct ----------\n", Yct)
# End Yct variable



# Vct variable : Tank volume in plant c at day t
columnsVct = {plants[0]: [LpVariable("100", 100, cat="Float")],
           plants[1]: [LpVariable("230", 100, cat="Float")]}

linesVct = days

Vct = pd.DataFrame(columnsVct, index=linesVct)
# print("\n---------- Vct ----------\n",, Vct)
# End Vct variable



# ANCct variable : ??? in plant c at period t
columnsANCct = {plants[0]: 300,
           plants[1]: 300}

linesANCct = days

ANCct = pd.DataFrame(columnsANCct, index=linesANCct)
# print("\n---------- ANCct ----------\n", ANCct)
# End ANCct variable



# InitVolumec variable : initial volume of each plant in each tank
columnsInitVolume = {plants[0]: 100,
                     plants[1]: 100}

linesInitVolume = tanks

InitVolume = pd.DataFrame(columnsInitVolume, index=linesInitVolume)
# print("\n---------- InitVolume ----------\n", InitVolume)
# End InitVolume variable



# Number of active turbines
NBctn = LpVariable("ActiveTurbines", cat="Binary")

prob += 2*Xct['Plant 1']['Day 1'], "Objective Function"


itDayPlant1 = iter(days)
next(itDayPlant1)
itDayPlant2 = iter(days)
next(itDayPlant2)

for plant in plants:
    for day in days:
        if plant == 'Plant 1':
            print("Plant", plant)
            if day == 'Day 1':
                print("First day", day)
                print("Constraint for day 1")
                # V initiale - q + apports
                print(next(itDayPlant1))
            else:
                print("Another day", day)
                if day != 'Day 30':
                    prob += Vct[plant][next(itDayPlant1)] == ANCct[plant][day] + Vct[plant][day] - Xct[plant][day] - Yct[plant][day]
                else:
                    print("Constraint for day 30")
        elif plant == 'Plant 2':
            print("Plant", plant)
            if day == 'Day 1':
                print("First day", day)
                print("Constraint for day 1")
                # V initiale - q + apports
                print(next(itDayPlant2))
            else:
                print("Another day", day)
                if day != 'Day 30':
                    prob += Vct[plant][next(itDayPlant2)] == ANCct[plant][day] + Vct[plant][day] - Xct[plant][day] - Yct[plant][day] + Xct['Plant 1'][day] + Yct['Plant 1'][day]
                else:
                    print("Constraint for day 30")
        else:
            print("Not a plant")




# faire conversion entre m^2/s en hectom^2/jour
# Variables en hectom^2/jour (conversion : m2/s = 0,086400 hecto^m2/jour)



# Objection Function
# prob += lpSum(lpSum((2)for c in range(1, 2))for p in range(1, 30)), "Objective Function"




# print("\n---------- Xct ----------\n", Xct)
# print("\n---------- Yct ----------\n", Yct)