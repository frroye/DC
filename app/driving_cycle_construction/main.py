import random
import pandas as pd
from preprocessing.MicrotripData import MicrotripData
from driving_cycle_construction.AssessmentCriteriaCalculator import AssessmentCriteriaCalculator
from driving_cycle_construction.DrivingCycle import DrivingCycle
from driving_cycle_construction.DrivingCycleController import DrivingCyclesController
from driving_cycle_construction.DCParametersCalculator import DCParametersCalculator
from preprocessing.RawDataController import File
""""""
"""
cycle_len = 600

#driving_cycle = DrivingCycle(file, transition_matrix, dc_len=cycle_len, delta_speed=5)
#driving_cycle.get_full_driving_cycle()
#driving_cycle.visualize_dc('Speed')
file = File("../data/clustered_microtrips/", "V_Acc_FuelR", ".csv", )

dc_controller = DrivingCyclesController(file)
dc = DrivingCycle(dc_controller.segment_df, dc_controller.transition_matrix, cycle_len, 20, 0)

print(dc.get_parameters())
full_data = []
full_data.append(dc.get_full_driving_cycle())
ac_calculator = AssessmentCriteriaCalculator(full_data)
print(ac_calculator.get_parameters())
#print(dc_controller.generate_cycle(iteration=3, dc_len=600, delta_speed=10))

#print(driving_cycle.get_parameters())

pd.set_option('display.max_columns', None)
df = pd.read_csv("test.csv",
                 sep=';', encoding='latin-1')

microtripData = MicrotripData(None)
microtripData.verification(df)
parameter_1 = microtripData.summarize_rawData()
print(parameter_1)
dc_parameter_calculator = DCParametersCalculator(parameter_1, 0)
print(dc_parameter_calculator.get_parameters())

full_data = []
full_data.append(df)
ac = AssessmentCriteriaCalculator()
print(ac.get_parameters())

"""
cycle_len = 600
file = File("../data/clustered_microtrips/", "PCA_7clusters", ".csv", )
dc_controller = DrivingCyclesController(file)
dc = DrivingCycle(dc_controller.segment_df, dc_controller.transition_matrix, cycle_len, 20, 0)
print(dc.parameters)
dc.visualize_dc('Speed')

