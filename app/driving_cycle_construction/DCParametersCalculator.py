""" Calculate the parameters of a driving cycle:
1	SAFD    Matrix of speed and acceleration	%
2	V_	Average speed of the entire driving cycle	Km/h
3	Vr	Average running speed	Km/h
4	Vm	Maximum speed	Km/h
5	Acc	Average acceleration of all acceleration phases	m/s2
6	Dcc	Average deceleration of all deceleration phases	m/s2
7	C	Average number of acceleration-deceleration changes (and vice versa) within one driving period	NA
8	A^2	Root mean square acceleration	m/s2
9	RP	Road power	kW
Time proportions of driving modes:
10	Idle_p	Idle (speed = 0)	%
11	Acc_p	Acceleration (acceleration ≥ 0.1 m/s2)	%
12	Cru_p	Cruising (- 0.1 m/s2 < acceleration < 0.1 m/s2, average speed > 20 km/h)	%
13	Dcc_p	Deceleration (acceleration ≤ -0.1 m/s2)	%
14	Cre_p	Creeping (- 0.1 m/s2 < acceleration < 0.1 m/s2, average speed < 20 km/h)	%

These parameters will be compare with the assessment criteria."""

import numpy as np

class DCParametersCalculator:

    def __init__(self, df, id):
        self.df = df #à changer pour une df contenant les infos des segments
        self.id = id
        self.parameters = self.summarize()


    def summarize(self):
        p_v = {'id': self.id,
               'V': self.compute_mean("V"),
               'Vr': self.compute_mean("V_r"),
               'Vm': self.compute_Vm(),
               'FuelR': self.compute_mean("FuelR"),
               'FuelR_r': self.compute_mean("FuelR_r"),
               'Acc': self.compute_mean("Acc"),
               'Dcc': self.compute_mean("Dcc"),
               'Acc2': self.compute_mean("Acc_2"),
               'V_std': self.compute_mean('V_std'),
               'FuelR_std': self.compute_mean('FuelRate_std'),
               'Acc_std': self.compute_mean('Acc_std'),
               'Idle_p': self.compute_mean('Idle_p'),
               'Acc_p': self.compute_mean('Acc_p'),
               'Dcc_p': self.compute_mean('Dcc_p'),
               'Cru_p': self.compute_mean('Cru_p'),
               'Cre_p': self.compute_mean('Cre_p')
               }
        return p_v

    def compute_mean(self, column):
        """Compute the time weighed mean of a column"""
        return np.average(self.df[column], weights=self.df['T'])

    def compute_Vm(self):
        """Compute the maximum speed of the database"""
        return self.df[['V_m']].max()[0]

    def get_parameters(self):
        return self.parameters


