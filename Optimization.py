from pulp import *
import pprint


print("\n\n\n------------------ New run ------------------") # Debug

# Creation of the problem
prob = LpProblem("Hydroelectric_Problem", LpMaximize)


# Period of the optimization
days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7', 'Day 8', 'Day 9', 'Day 10',
         'Day 11', 'Day 12', 'Day 13', 'Day 14', 'Day 15', 'Day 16', 'Day 17', 'Day 18', 'Day 19', 'Day 20',
         'Day 21', 'Day 22', 'Day 23', 'Day 24', 'Day 25', 'Day 26', 'Day 27', 'Day 28', 'Day 29', 'Day 30']


# Plants
plants = ['Plant 1', 'Plant 2']


# Tanks
tanks = ['Tank']



# Xct variable : Turbined volume in plant c at day t (minFlowct < columnsXct < maxFlowct)

Xct = LpVariable.dicts(name = "Xct",
                       indices = (range(len(plants)), range(len(days))),
                       lowBound = 0,
                       upBound = 100,
                       cat = "Continuous")

# print("\n---------- Xct ----------\n", Xct)
# End Xct variable



# Yct variable : Discharged volume in plant c at day t (minWeirct < columnsYct < maxWeirct)

Yct = LpVariable.dicts(name = "Yct",
                       indices = (range(len(plants)), range(len(days))),
                       lowBound = 0,
                       upBound = 1000,
                       cat = "Continuous")

# print("\n---------- Yct ----------\n", Yct)
# End Yct variable



# Vct variable : Tank volume in plant c at day t

Vct = LpVariable.dicts(name = "Vct",
                       indices = (range(len(plants)), range(len(days))),
                       lowBound = 0,
                       cat = "Continuous")

# print("\n---------- Vct ----------\n", Vct)
# End Vct variable


# Pct variable : ___ in plant c at day t

Pct = LpVariable.dicts(name = "Pct",
                       indices = (range(len(plants)), range(len(days))),
                       lowBound = 0,
                       cat = "Continuous")

# print("\n---------- Pct ----------\n", Pct)
# End Pct variable


# ANCct variable : ??? in plant c at period t

ANCct = []
for i in range(len(plants)):
    array = []
    for j in range(len(days)):
        array.append(50)
    ANCct.append(array)

# print("\n---------- ANCct ----------\n", ANCct)
# End ANCct variable



# InitVolumec variable : initial volume of each plant in each tank

InitVolume = [100, 100]

# print("\n---------- InitVolume ----------\n", InitVolume)
# End InitVolume variable


# InitVolumec variable : final volume of each plant in each tank

FinalVolume = [80, 80]

# print("\n---------- FinalVolume ----------\n", FinalVolume)
# End FinalVolume variable


# Number of active turbines
turbines = [1, 2, 3]

NBctn = LpVariable.dicts(name = "NBctn", 
                         indices = (range(len(plants)), range(len(days)), range(len(turbines))),
                         cat="Binary")



# Objective function
prob += lpSum(lpSum((2*Vct[plant][day])for plant in range(len(plants)))for day in range(len(days))), "Objective Function"


for plant in range(len(plants)):
    # For each plant
    for day in range(len(days)):
        # For each day
        prob += Pct[plant][day] == (NBctn[plant][day][0]*1) + (NBctn[plant][day][1]*2) + (NBctn[plant][day][2]*3)
        for combine in NBctn[plant][day]:
            prob += lpSum(NBctn[plant][day]) == 1
        if day == 0:
            # If day 1
            prob += Vct[plant][0] == InitVolume[plant]
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

        
        
prob.solve()
        

        
for plant in range(len(plants)):
    # For each plant
    for day in range(len(days)):
        # For each day
        Xct[plant][day] = pulp.value(Xct[plant][day])
        Yct[plant][day] = pulp.value(Yct[plant][day])
        Vct[plant][day] = pulp.value(Vct[plant][day])
        Pct[plant][day] = pulp.value(Pct[plant][day])
        for turbine in range(len(turbines)):
            NBctn[plant][day][turbine] = pulp.value(NBctn[plant][day][turbine])



pp = pprint.PrettyPrinter(indent = 2)

# Print Xct
print("\n---------- Xct ----------")
pp.pprint(Xct)
    
    
# Print Yct
print("\n---------- Yct ----------")
pp.pprint(Yct)


# Print Vct
print("\n---------- Vct ----------")
pp.pprint(Vct)


# Print NBctn
print("\n---------- NBctn ----------")
pp.pprint(NBctn)


# Print Pct
print("\n---------- Pct ----------")
pp.pprint(Pct)

# faire conversion entre m^3/s en hectom^3/jour
# Variables en hectom^3/jour (conversion : m^3/s = 0,086400 hectom^3/jour)

# Convertire ANC, X et Y en hectom^3 pas besoin pour V car déjà en hectom^3
