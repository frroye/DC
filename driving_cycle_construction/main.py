

from driving_cycle_construction.AssessmentCriteriaCalculator import AssessmentCriteriaCalculator
from driving_cycle_construction.TransitionMatrixController import TransitionMatrixController
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


