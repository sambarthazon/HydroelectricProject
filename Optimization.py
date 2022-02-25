from pulp import *
# Maybe use numpy and panda for data of parameters and sets

print("-------------------------------------")

# Creation of the problem
prob = LpProblem("Hydroelectric_Problem", LpMaximize)

# Just for the compilation
minFlowct = 0
maxFlowct = 300

minWeirct = 0
maxWeirct = 1000

Pcp = Pct = Xcn = Vc1t = ANCc1t = Xc1t = Yc1t = Vct1 = InitialVolumec = Vct30 = FinalVolumec = 1


# Creation of the variables

# Turbined volume at plant 'c' and period 't' between minimum flow and maximum flow
Xct = LpVariable("TurbinedVolume", minFlowct, maxFlowct, cat="Float")

# Discharged volume at plant 'c' and period 't' between minimum weir and maximum weir
Yct = LpVariable("DischargedVolume", minWeirct, maxWeirct, cat="Float")

# Volume of the tank at plant 'c' and period 't' 
Vct = LpVariable("TankVolume", cat="Float")

# Number of active turbines
NBctn = LpVariable("ActiveTurbines", cat="Binary")

# Objection Function
prob += lpSum(lpSum((Pcp)for c in range(1, 2))for p in range(1, 30)), "Objective Function"

# Constrains
prob += Pct <= 2*Xcn, "Power produced for each plant"
prob += Vc1t == ANCc1t + Vc1t - Xc1t - Yc1t, "Tank volume of the first plant"
prob += lpSum(NBctn for n in range(1, 3)) == 1, "Single active turbine combination"
prob += Vct1 == InitialVolumec, "Initial volume in each tank"
prob += Vct30 == FinalVolumec, "Final volume in each tank"
