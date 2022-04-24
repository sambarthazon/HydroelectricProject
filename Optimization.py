from pulp import *
import pprint


print("\n\n\n------------------ New run ------------------") # Debug

"""
Création du problème, maximisation de la production électrique
"""
prob = LpProblem("Hydroelectric_Problem", LpMaximize)



"""
Période d'optimisation
"""
days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7', 'Day 8', 'Day 9', 'Day 10']
        #  'Day 11', 'Day 12', 'Day 13', 'Day 14', 'Day 15', 'Day 16', 'Day 17', 'Day 18', 'Day 19', 'Day 20',
        #  'Day 21', 'Day 22', 'Day 23', 'Day 24', 'Day 25', 'Day 26', 'Day 27', 'Day 28', 'Day 29', 'Day 30']


"""
Centrales hydroélectrique
"""
plants = ['Plant 1', 'Plant 2']


"""
Réservoirs des centrales
"""
tanks = ['Tank 1', 'Tank 2']


"""
Nombre de turbine dans chaque centrale
"""
turbines = [1, 2, 3]



"""
Le volume turbiné par la centrale c à la période t
"""
Xct = LpVariable.dicts(name = "Xct",
                       indices = (range(len(plants)), range(len(days))),
                       lowBound = 200,
                       upBound = 1400,
                       cat = "Continuous")


"""
Le volume déversé par la centrale c à la période t
"""
Yct = LpVariable.dicts(name = "Yct",
                       indices = (range(len(plants)), range(len(days))),
                       lowBound = 0,
                       upBound = 500,
                       cat = "Continuous")


"""
Le volume du réservoir associé à la centrale c à la période t
"""
Vct = LpVariable.dicts(name = "Vct",
                       indices = (range(len(plants)), range(len(days))),
                       cat = "Continuous")


"""
L'ensemble des apports hydriques non contrôlés à la centrale c à la période t
"""
ANCct = [[400 for _ in range(len(days))] for _ in range(len(plants))]


"""
Le niveau initial du réservoir associé à sa centrale
"""
InitVolume = [378, 475]


"""
Le niveau final du réservoir associé à sa centrale    
"""
FinalVolume = [355, 453]


"""
Le nombre de turbines actives à la centrale c à la période t
"""
NBctn = LpVariable.dicts(name = "NBctn", 
                         indices = (range(len(plants)), range(len(days)), range(len(turbines))),
                         cat="Binary")


"""
Puissance produite par la centrale c à la période t
"""
Pct = LpVariable.dicts(name = "Pct",
                       indices = (range(len(plants)), range(len(days))),
                       lowBound = 0,
                       upBound = 2000,
                       cat = "Continuous")



"""
Hyperplan associé à la centrale 1 en 3 dimensions pour chaque turbine
"""
H_1_x = [[0.25,-0.1], [0.26,-0.15], [0.27,-0.2]]
H_1_y = [[0.008406189344, 0.12], [0.008806189344, 0.125], [0.009406189344, 0.13]]
H_1_z = [[11, 252], [11, 300], [11, 380]]


"""
Hyperplan associé à la centrale 2 en 3 dimensions pour chaque turbine
"""
H_2_x = [[0.45, -0.35], [0.5, -0.38], [0.7, -0.40]]
H_2_y = [[0.009, 0.10], [0.009, 0.10], [0.009, 0.10]]
H_2_z = [[0, 800], [0, 800], [0, 800]]



"""
Fonction objective visant à maximiser la production d'électricité
"""
prob += lpSum(lpSum((Pct[plant][day])for plant in range(len(plants)))for day in range(len(days))), "Objective Function"



"""Boucle pour chaque centrale"""
for plant in range(len(plants)):
    """Boucle pour chaque jour"""
    for day in range(len(days)):

        """Initialisation des bornes pour Vct en fonction de la centrale"""
        if plant == 0:
            Vct[plant][day].lowBound = 350
            Vct[plant][day].upBound = 385
        elif plant == 1:
            Vct[plant][day].lowBound = 450
            Vct[plant][day].upBound = 500
        else:
            print("Error plant")

        """Boucle pour chaque combinaison de turbine"""
        for combine in NBctn[plant][day]:
            """Mise en place de la fonction de production en fonction de la centrale"""
            if plant == 0:
                prob += Pct[plant][day] <= H_1_x[combine][0] * (Xct[plant][day]*0.086400) + H_1_y[combine][0] * Vct[plant][day] + H_1_z[combine][0] + (1 - NBctn[plant][day][combine]) * 2000
                prob += Pct[plant][day] <= H_1_x[combine][1] * (Xct[plant][day]*0.086400) + H_1_y[combine][1] * Vct[plant][day] + H_1_z[combine][1] + (1 - NBctn[plant][day][combine]) * 2000
            elif plant == 1:
                prob += Pct[plant][day] <= H_2_x[combine][0] * (Xct[plant][day]*0.086400) + H_2_y[combine][0] * Vct[plant][day] + H_2_z[combine][0] + (1 - NBctn[plant][day][combine]) * 2000
                prob += Pct[plant][day] <= H_2_x[combine][1] * (Xct[plant][day]*0.086400) + H_2_y[combine][1] * Vct[plant][day] + H_2_z[combine][1] + (1 - NBctn[plant][day][combine]) * 2000
            else:
                print("Error plant")

            """Une seule combinaison de turbine doit être active pour chaque jour"""
            prob += lpSum(NBctn[plant][day]) == 1

        """Contraintes de volume du réservoir en fonction des jours et des centrales"""
        if day == 0:
            prob += Vct[plant][0] == InitVolume[plant]
            prob += Vct[plant][day+1] == (ANCct[plant][day]*0.086400) + Vct[plant][day] - (Xct[plant][day]*0.086400) - (Yct[plant][day]*0.086400)
        elif day < 9:
            if plant == 0:
                prob += Vct[plant][day+1] == (ANCct[plant][day]*0.086400) + Vct[plant][day] - (Xct[plant][day]*0.086400) - (Yct[plant][day]*0.086400)
            elif plant == 1:
                prob += Vct[plant][day+1] == (ANCct[plant][day]*0.086400) + Vct[plant][day] - (Xct[plant][day]*0.086400) - (Yct[plant][day]*0.086400) + (Xct[plant-1][day]*0.086400) + (Yct[plant-1][day]*0.086400)
            else:
                print("Error plant")
        elif day == 9:
            if plant == 0:
                prob += Vct[plant][9] == FinalVolume[0]
                prob += Vct[plant][day] == (ANCct[plant][day]*0.086400) + Vct[plant][day] - (Xct[plant][day]*0.086400) - (Yct[plant][day]*0.086400)
            elif plant == 1:
                prob += Vct[plant][9] == FinalVolume[1]
                prob += Vct[plant][day] == (ANCct[plant][day]*0.086400) + Vct[plant][day] - (Xct[plant][day]*0.086400) - (Yct[plant][day]*0.086400) + (Xct[plant-1][day]*0.086400) + (Yct[plant-1][day]*0.086400)
            else:
                print("Error plant")
        else:
            print("Error day")



"""
Appel du solver
"""
prob.solve()


"""
Assigniation des résultats
"""
for plant in range(len(plants)):
    for day in range(len(days)):
        Xct[plant][day] = pulp.value(Xct[plant][day])
        Yct[plant][day] = pulp.value(Yct[plant][day])
        Vct[plant][day] = pulp.value(Vct[plant][day])
        Pct[plant][day] = pulp.value(Pct[plant][day])
        for turbine in range(len(turbines)):
            NBctn[plant][day][turbine] = pulp.value(NBctn[plant][day][turbine])


"""
Pour un meilleur affichage
"""
pp = pprint.PrettyPrinter(indent = 2)

"""
Affichage de Xct
"""
print("\n---------- Xct ----------")
pp.pprint(Xct)
    
    
"""
Affichage de Yct
"""
print("\n---------- Yct ----------")
pp.pprint(Yct)


"""
Affichage de Vct
"""
print("\n---------- Vct ----------")
pp.pprint(Vct)


"""
Affichage de NBctn
"""
print("\n---------- NBctn ----------")
pp.pprint(NBctn)


"""
Affichage de Pct
"""
print("\n---------- Pct ----------")
pp.pprint(Pct)



"""Les variables 'Xct', 'Yct' et 'ANCct' étaient en m^3/s nous les avons convertis en hectomètre^3/jour, 
avec le coefficient : m^3/s = 0.086400 hectomètre^3/jour

Nous devons également convertir la puissance en MW/j
"""
