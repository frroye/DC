"""
Permet d'évaluer la performance de cycles créés pour un nombre 
d'itération variable. La vitesse est le seul critère de comparaison 
considéré. Les microtrips sont segmentées en segments de 250m et 
sont classifiés dans 7 clusters selon un PCA sur 15 paramètres caractéristiques 
et à l'aide de l'algorithme des k-moyens.

"""

from driving_cycle_construction.DrivingCycle import *
from driving_cycle_construction.DrivingCycleController import *
from preprocessing.RawDataController import File
from matplotlib import pyplot
from numpy import array
import time


t0 = time.time()
directory_name = "test5"

cycle_len = 1800

file = File("../../data/clustered_microtrips/", "PCA_7clusters", ".csv", )
cycle_comparison_parameters = ['V']
dc_controller = DrivingCyclesController(file, cycle_comparison_parameters)

diff_average= []
diff_std= []

it = []
it.append(1)
it.append(10)
it.append(50)
it.append(100)
it.append(200)
it.append(500)
it.append(800)
it.append(1000)

for i in it:  # i : nb d'itération lors de la construction du cycle
    iteration = i
    diff_j = []
    for j in range(0, 30):  # j : nb de cycle créé/sélectionné
        dc = dc_controller.generate_cycle(iteration, cycle_len, 20)
        diff_j.append(dc.difference)

    df = pd.DataFrame(diff_j)
    print(i)
    df["iteration"] = iteration
    diff_average.append(df.mean())
    diff_std.append(df.std())

print(time.time() - t0)
file_name_average = directory_name + str(iteration) + "_" + str(j) + "average"+ ".csv"
file_name_std = directory_name + str(iteration) + "_" + str(j) + "std"+ ".csv"
pd.DataFrame(diff_average).to_csv(file_name_average, sep=";")
pd.DataFrame(diff_std).to_csv(file_name_std, sep=";")