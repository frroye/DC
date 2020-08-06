

from driving_cycle_construction.AssessmentCriteriaCalculator import AssessmentCriteriaCalculator
from driving_cycle_construction.TransitionMatrixController import TransitionMatrixController
from driving_cycle_construction.DrivingCycleController import DrivingCycleConstructor, DrivingCyclesController
from driving_cycle_construction.DCParametersCalculator import DCParametersCalculator
from preprocessing.RawDataController import File


#  generate the assessment criteria
ac_calculator = AssessmentCriteriaCalculator()
ac_calculator.summarize_AC()
ac_calculator.save_csv()
assessment_criteria = ac_calculator.get_AC()


#  generate the transition matrix
file = File("../data/clustered_microtrips/", "V_Acc_FuelR", ".csv", )
tmc = TransitionMatrixController(file)
transition_matrix = tmc.get_transition_matrix()

cycle_len = 100

dc_constructor = DrivingCycleConstructor(file, transition_matrix, 100)
dc_ = dc_constructor.generate_DC()

dc_controller = DrivingCyclesController(dc_constructor.df_segment, assessment_criteria)

dc_parameter_calculator = DCParametersCalculator(dc_controller)
print(dc_parameter_calculator.compute_Vm())

