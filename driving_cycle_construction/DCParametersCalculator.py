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


class DCParametersCalculator:

    def __init__(self, dc_controller):
        self.dc_controller = dc_controller
        self.df_segment = self.dc_controller.df_segment
        self.df = self.df_segment #à changer pour une df contenant les infos des segments
        self.dc_len = self.df[["T"]].sum()

    def summarize(self):
        p_v = {'V': self.compute_mean("V"),
               'Vr': self.compute_mean("V_r"),
               'Vm': self.compute_Vm(),
               'FuelR': self.compute_mean("FuelR"),
               'FuelRr': self.compute_mean("FuelRr"),
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
        df = self.df[column]*self.df["T"]
        return df.sum()/self.dc_len[0]


    def compute_Vm(self):
        """Compute the maximum speed of the database"""
        return self.df[['V_m']].max()[0]



