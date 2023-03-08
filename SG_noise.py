'''
Reffered Code - QuTip-Notebooks
https://notebook.community/qutip/qutip-notebooks/examples/stern-gerlach-tutorial
'''

from qutip import Qobj,Bloch, ket
import numpy as np 
import matplotlib.pyplot as plt
from collections import namedtuple


up, down = ket("0"), ket("1")
Direction = namedtuple("Direction", ["theta", "phi"])


# coverting a given direction in theta and phi to a qubit representation
def convert_to_qubit(d):
    return np.cos(d.theta / 2) * up + np.exp(1j * d.phi) * np.sin(d.theta / 2) * down


# mesure the spin of the atom in Z direction only, function takes input of qubit
def measure_zspin(qubit):
    zspin = (up.dag() * qubit).tr()
    prob = np.abs(zspin) ** 2
    
    if np.random.uniform(0, 1) <= prob:
        return 1
    else:
        return -1

# give n number of random directions based on input
def random_direction():
    r = 0
    while r == 0: #check amplitude, recal. if found out to be zero
        x, y, z = np.random.normal(0, 1, 3) #get random normal distributed values in range of [0,1]
        r = np.sqrt(x**2 + y**2 + z**2) #cal amplitude
    
    #find the angles
    phi = np.arctan2(y, x)
    theta = np.arccos(z / r)
    return Direction(theta=theta, phi=phi)

#simulating stern gerlach with a quantum model
def stern_gerlach(n):
    directions = [random_direction() for _ in range(n)]
    atoms = [convert_to_qubit(d) for d in directions]
    zspins = [measure_zspin(q) for q in atoms]
    return atoms, zspins

def plot_outcome(atoms, spins):
    fig = plt.figure(figsize=(18.0, 8.0))
    fig.suptitle("Stern-Gerlach Experiment: Quantum Outcome", fontsize="xx-large")

    ax1 = plt.subplot(1, 2, 1, projection='3d')
    ax2 = plt.subplot(1, 2, 2)

    b = Bloch(fig=fig, axes=ax1)
    b.vector_width = 1
    b.vector_color = ["#{:x}0{:x}0ff".format(i, i) for i in range(10)]
    b.add_states(atoms)
    b.render()

    ax2.hist(spins)
    ax2.set_xlabel("Z-component of spin")
    ax2.set_ylabel("# of atoms")

    plt.show()

def with_noise(n, spins):
    
    noise = np.random.normal(0,0.4,n)
    spins += noise

    fig, ax = plt.subplots()
    ax.hist(spins, bins = 50)
    ax.set_xlabel("Z-component of spin")
    ax.set_ylabel("# of atoms")
    plt.show()

n = 1000
atoms, spins = stern_gerlach(n)
plot_outcome(atoms, spins)
with_noise(n, spins)
