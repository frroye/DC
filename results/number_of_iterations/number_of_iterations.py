from driving_cycle_construction.DrivingCycle import *
from preprocessing.RawDataController import File
from matplotlib import pyplot
from numpy import array
import time


t0 = time.time()
directory_name = "test5"

cycle_len = 600

file = File("../../data/clustered_microtrips/", "PCA_7clusters", ".csv", )
dc_controller = DrivingCyclesController(file)

#pour un nombre d'itération de cycle i de 1 à n
#       pour un nombre  de sélection de cycle j de m fois
#           créer un cycle
#           enregistrer son dic diff dans une liste de dic
#       créer une df avec les diff, faire la moyenne des colonnes
#       enregistrer les moyennes dans une liste de dic
#  faire une df avec les moyennes des diff, avec comme id le nombre d'itération
# enregistrer la df

diff_i= []
it = []
it.append(1)
it.append(10)
it.append(50)
it.append(100)



for i in it:  # i : nb d'iération lors de la construction du cycle
    iteration = i
diff_j = []

    for j in range(0, 1):  # j : nb de cycle créé/sélectionné
diff_j.append(diff)
    df = pd.DataFrame(diff_j)
    df["iteration"] = iteration
    diff_i.append(df.mean())
    #diff_i.append(df.std())
    df = pd.concat(diff_i, axis=0, join='outer', ignore_index=False, keys=None,
                   levels=None, names=None, verify_integrity=False, copy=True)
    print(df)
    file_name = directory_name + str(iteration) + "_" + str(j) + ".csv"
    df.to_csv(file_name, sep=";")
    diff_i = []

print(time.time() - t0)


"""
x, y = zip(*lists) # unpack a list of pairs into two tuples

pyplot.plot(x, y)
pyplot.show()
"""





#print(driving_cycle.get_parameters())