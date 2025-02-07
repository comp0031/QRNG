from typing import List
import numpy as np
import random
from dotenv import load_dotenv

from qiskit import QuantumCircuit
from qiskit_aer.primitives import SamplerV2
from qiskit_ibm_runtime import QiskitRuntimeService

load_dotenv()

class QuantRNG:
    def __init__(self, qubits: int, shots: int, sampler: SamplerV2 = None, circuit: QuantumCircuit = None):
        """
        Args:
            qubits: The number of qubits in the quantum circuit. Determines how large the random numbers can be.
            shots: The number of shots to run the quantum circuit / the number of random numbers to generate.
            sampler: The sampler to use for running the quantum circuit. Defaults to SamplerV2.
            circuit: The quantum circuit to use for generating random numbers. Defaults to hadamards on all qubits.
        """
        self.qubits = qubits
        self.shots = shots
        self.circ: QuantumCircuit = circuit
        self.sampler = sampler
        if not self.circ:
            self.default_circuit()
        if not self.sampler:
            self.sampler = SamplerV2()
    
    def default_circuit(self):
        self.circ = QuantumCircuit(self.qubits)
        self.circ.h(range(self.qubits))
        self.circ.measure_all()
    
    def set_sampler(self, sampler: SamplerV2):
        self.sampler = sampler
    
    def set_circuit(self, circuit: QuantumCircuit):
        self.circ = circuit
    
    def _run(self):
        job = self.sampler.run([self.circ], shots=self.shots)
        return job.result()
    
    def get_counts(self) -> dict:
        result = self._run()
        return result[0].data.meas.get_bitstrings()
    
    def get_bitstream(self) -> List[int]:
        counts = self.get_counts()
        return [int(k, 2) for k in counts]

def calc_entropy(binary_string: str) -> float:
    if not binary_string:
        return 0.0

    arr = np.array(list(binary_string), dtype=int)
    counts = np.bincount(arr)
    probabilities = counts[counts > 0] / len(arr)
    entropy = -np.sum(probabilities * np.log2(probabilities))
    return entropy

if __name__ == '__main__':
    length = 10000000

    entropy_trials = 100
    results = {'Quantum': [], 'Classical': []}

    rng = QuantRNG(1, length)
    for _ in range(entropy_trials):
        # Quantum random number generation
        bitstream_quantum = ''.join([str(b) for b in rng.get_bitstream()])
        entropy = calc_entropy(bitstream_quantum)
        results['Quantum'].append(entropy)

        # Typical random number generation
        bitstream_classical = ''.join([str(random.randint(0, 1)) for _ in range(length)])
        entropy = calc_entropy(bitstream_classical)
        results['Classical'].append(entropy)
    
    quantum_avg = sum(results['Quantum']) / entropy_trials
    classical_avg = sum(results['Classical']) / entropy_trials
    print(f'Quantum entropy results: {quantum_avg}')
    print(f'Classical entropy results: {classical_avg}')