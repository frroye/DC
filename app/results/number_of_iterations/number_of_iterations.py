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
cycle_comparison_parameters = ['V','Vr','Vm','Acc','Dcc','Acc2','Idle_p','Acc_p','Dcc_p','Cru_p','Cre_p']

#'V','Vr','Vm','FuelR','FuelR_r','Acc','Dcc','Acc2','V_std','FuelR_std','Acc_std','Idle_p','Acc_p','Dcc_p','Cru_p','Cre_p'
dc_controller = DrivingCyclesController(file, cycle_comparison_parameters)

#pour un nombre d'itération de cycle i de 1 à n
#       pour un nombre  de sélection de cycle j de m fois
#           créer un cycle
#           enregistrer son dic diff dans une liste de dic
#       créer une df avec les diff, faire la moyenne des colonnes
#       enregistrer les moyennes dans une liste de dic
#  faire une df avec les moyennes des diff, avec comme id le nombre d'itération
# enregistrer la df

diff_average= []
diff_std= []

it = []
it.append(1)
it.append(10)
#it.append(20)
#it.append(30)
#it.append(40)
it.append(50)
it.append(100)
it.append(200)
it.append(300)
it.append(400)
it.append(500)
it.append(600)
it.append(700)
it.append(800)
it.append(900)
it.append(1000)
#it.append(100)


for i in it:  # i : nb d'itération lors de la construction du cycle
    iteration = i
    diff_j = []
    for j in range(0, 30):  # j : nb de cycle créé/sélectionné
        dc = dc_controller.generate_cycle(iteration, cycle_len, 20)
        diff_j.append(dc.difference)

    df = pd.DataFrame(diff_j)
    print(i)
    df["iteration"] = iteration
    #print(df)
    #df["iteration"] = iteration
    diff_average.append(df.mean())
    diff_std.append(df.std())
    #diff_i.append(df.std())
    #df = pd.concat(diff_i, axis=0, join='outer', ignore_index=False, keys=None,
    #             levels=None, names=None, verify_integrity=False, copy=True)
    #print(diff_j)
    #file_name = directory_name + str(iteration) + "_" + str(j) + ".csv"
    #df.to_csv(file_name, sep=";")
    #diff_j = []

print(time.time() - t0)
#print(pd.DataFrame(diff_average))
file_name_average = directory_name + str(iteration) + "_" + str(j) + "average"+ ".csv"
file_name_std = directory_name + str(iteration) + "_" + str(j) + "std"+ ".csv"
pd.DataFrame(diff_average).to_csv(file_name_average, sep=";")
pd.DataFrame(diff_std).to_csv(file_name_std, sep=";")


"""
x, y = zip(*lists) # unpack a list of pairs into two tuples

pyplot.plot(x, y)
pyplot.show()
"""





#print(driving_cycle.get_parameters())