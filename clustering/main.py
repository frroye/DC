from clustering.ClusteringController import *

#import data
files =[File("../data/microtrips/", "ID_37060_20181112_112249_m", ".csv"),
        File("../data/microtrips/", "ID_30095_20181110_m", ".csv"),
        File("../data/microtrips/", "ID_31823_20181110_104529_m", ".csv"),
        File("../data/microtrips/", "ID_31823_20181110_192040_m", ".csv"),
        File("../data/microtrips/", "ID_31823_20181112_113559_m", ".csv"),
        File("../data/microtrips/", "ID_37060_20181110_015918_m", ".csv")]


clustering_controller = ClusteringController(files)
#print(clustering_controller.get_microtrips_number())
PCA_columns = ['T', 'S', 'FuelR', 'FuelR_r', 'FuelRate_std', 'V', 'V_r', 'V_m', 'V_std', 'Acc', 'Dcc', 'Acc_2',
               'Acc_std', 'Idle_p', 'Acc_p', 'Cru_p', 'Cre_p', 'Dcc_p']
#clustering_controller.PCA(0.80, PCA_columns)
columns = ['V', 'FuelR', 'Acc']
clustering_controller.select_clustering_columns(columns)
clustering_controller.kmeans(6)
clustering_controller.visualize_cluster3D()
#clustering_controller.visualize_cluster()
clustering_controller.save_csv('V_Acc_FuelR')

#merge files

#pandas.DataFrame(pca.transform(df), columns=['PCA%i' % i for i in range(n_components)], index=df.index)

#adjust format

#apply PCA

#apply PAM

#