from driving_cycle_construction.DrivingCycle import DrivingCycle
from driving_cycle_construction.TransitionMatrixController import TransitionMatrixController
from driving_cycle_construction.AssessmentCriteriaCalculator import AssessmentCriteriaCalculator
from driving_cycle_construction.DCParametersCalculator import DCParametersCalculator
import pandas as pd

class DrivingCyclesController:
    def __init__(self, file, comparisonParameters = []):
        self.file = file
        self.segment_df = self.import_csv2pd(file)
        # generate the transition matrix
        tmc = TransitionMatrixController(self.segment_df)
        self.transition_matrix = tmc.get_transition_matrix()
        # generate the assessment criteria
        dc_parameter_controller = DCParametersCalculator(self.segment_df, id=-1)
        self.assessment_criteria = dc_parameter_controller.summarize()
        self.comparisonParameters = comparisonParameters

    def import_csv2pd(self, file):
        """Import csv to pandas dataframe.
        The first row of the data need to be the column name."""
        df = pd.read_csv(file.path + file.name + file.extension, sep=';', encoding='latin-1')
        return df

    def generate_cycle(self, iteration=20, dc_len=600, delta_speed=10):
        """Generate cycles and select the best one. 
        Cycles containes the potentiel cycles.
        Parameters containes the difference between the cycles parameter and the the assessment criteria.
        iteration: number of cycles generated
        dc_len: lenght of the cycles, in secondes
        delta_speed: accepted speed difference between two microtrips edges
        Return the selected cycle.
        """
        parameters = []
        cycles = []
        for i in range(0, iteration):
            cycle = DrivingCycle(self.segment_df, self.transition_matrix, dc_len, delta_speed, i)
            cycles.append(cycle)
            parameters.append(cycle.compute_difference(self.assessment_criteria))
        comparison_df = self.compare_cycle(parameters)
        nb = comparison_df['rank'].sort_values(ascending=True).index.values[0]
        cycles[nb].set_rank((comparison_df.iloc[int(nb)]['rank']))
        return cycles[nb]

    def compare_cycle(self, parameters):
        """Compare the cycles contained in parameters. 
        It ranks the cycles according to each criterion. The most performant cycle according to a 
        criterion is given a rank 0. This rank is added to the column rank, that containes the 
        sum of all ranks of a cycle. It only ranks the cycle according to the comparison parameters 
        in self.comparisonParameters.
        """
        comparison_df = pd.DataFrame(parameters)
        comparison_df['rank'] = 0
        if len(self.comparisonParameters) == 0:
            self.comparisonParameters = [col for col in comparison_df.columns if col != 'rank']
        for column in comparison_df[self.comparisonParameters]:
            index = comparison_df[column].sort_values(ascending=True).index.values
            for i in range(0, len(index)):
                comparison_df.loc[index[i], 'rank'] += i
        return comparison_df

