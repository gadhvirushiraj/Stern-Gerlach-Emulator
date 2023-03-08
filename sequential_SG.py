'''
Reffered Code - QuTip-Notebooks
https://notebook.community/qutip/qutip-notebooks/examples/stern-gerlach-tutorial
'''



from qutip import ket
import numpy as np 
import matplotlib.pyplot as plt
from collections import namedtuple

class detector_series():

    def __init__(self, series_analyser, series_path, n):
        self.series_analyser = series_analyser
        self.series_path = series_path
        self.n = n
        self.direction = namedtuple("Direction", ["theta", "phi"])

    def sequence_data_parcel(self):

        if(len(self.series_analyser) != len(self.series_path)):
            print("Length of analyser list and path list not as per required: ERROR")
            exit()

        data = [self.generate_random_direction() for _ in range(self.n)]
        last_detector = (0,0)
        for i in range(len(self.series_analyser)):
            up, down = self.check_detector_type(i)

            if last_detector != (up, down):
                data = [self.generate_random_direction() for _ in range(len(data))]

            temp = []
            result = self.make_detector(data, up, down)[self.series_path[i]]
            temp = [data[j] for j in range(len(result)) if result[j] == True]
            
            data = temp
            last_detector = (up, down)
            

    def check_detector_type(self, i):
        if self.series_analyser[i] == "X":
            return (ket("0") + ket("1"))/np.sqrt(2), (ket("0") - ket("1"))/np.sqrt(2)
        elif self.series_analyser[i] == "Y":
            return (ket("0") + 1j*ket("1"))/np.sqrt(2), (ket("0") - 1j*ket("1"))/np.sqrt(2)
        elif self.series_analyser[i] == "Z":
            return ket("0"), ket("1")
        else:
            print("INVALID INPUT: ERROR")
            exit()

    def make_detector(self, data, up, down):
        atoms = [self.convert_to_qubit(d) for d in data]
        spins = np.array([self.measure_spin(q,up) for q in atoms])
        self.plot_outcomes(spins)
        return [spins == 1, spins == -1]

    def generate_random_direction(self):
        r = 0
        while r == 0:
            x, y, z = np.random.normal(0, 1, 3)
            r = np.sqrt(x**2 + y**2 + z**2)
        phi = np.arctan2(y, x)
        theta = np.arccos(z / r)

        return self.direction(theta=theta, phi=phi)

    def convert_to_qubit(self, d):
        up, down = ket("0"), ket("1")
        return np.cos(d.theta / 2) * up + np.exp(1j * d.phi) * np.sin(d.theta / 2) * down

    def measure_spin(self, qubit, up):
        spin = (up.dag() * qubit).tr()
        prob = np.abs(spin) ** 2
        
        if 0.5 <= prob:
            return 1
        else:
            return -1

    def plot_outcomes(self, spins):
        fig, ax = plt.subplots()
        ax.hist(spins)
        ax.set_xlabel("component of spin")
        ax.set_ylabel("# of atoms")
        plt.show()


analyser = ['Z', 'Z', 'X', 'Z']
path = [1, 0, 0, 0]
d1 = detector_series(analyser, path, 1000)
d1.sequence_data_parcel()
