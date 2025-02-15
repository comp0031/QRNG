IBMQ_TOKEN =  'd85be79a49e049a8ea863a76f5ff43e3d61af162ba4c2a697bbeb32e6574f7f321b44f6d1d469c4b6387812e50eaf7fa654a0f5bd126fed29360b4eb8d089236'

import numpy as np

# Qiskit
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_state_city
import qiskit.quantum_info as qi

simulator = AerSimulator()

# create circuit
circ = QuantumCircuit(2)
circ.h(0)
circ.cx(0, 1)
circ.measure_all()

# Transpile for simulator
simulator = AerSimulator()
circ = transpile(circ, simulator)

# Run and get counts
result = simulator.run(circ).result()
counts = result.get_counts(circ)
plot_histogram(counts, title='Bell-State counts')
