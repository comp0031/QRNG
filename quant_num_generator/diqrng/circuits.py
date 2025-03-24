from collections import Counter
import math
from qiskit import QuantumCircuit, generate_preset_pass_manager
from qiskit.quantum_info import SparsePauliOp
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2, EstimatorV2
from qiskit_aer import AerSimulator

simulated = 'FakeKyiv' # Change to simulate other QPUs
dynamic_fake_provider = __import__('qiskit_ibm_runtime.fake_provider', fromlist=[simulated])
fake = getattr(dynamic_fake_provider, simulated)


BASES = [('Z', 'Z'), ('Z', 'X'), ('X', 'Z'), ('X', 'X')]


class ChshCircuit:

    def __init__(self, num_pairs: int, token: str | None, angle: float=math.pi/4) -> None:
        if token:
            service = QiskitRuntimeService(channel="ibm_quantum", token=token)
            self._backend = service.least_busy(operational=True, simulator=False, min_num_qubits=num_pairs * 2)
            self._sampler = SamplerV2(mode=self._backend)
            self._simulated = False
        else:
            print(f"Using simulated circuit ('{simulated}')")
            self._backend = fake()
            self._sampler = AerSimulator.from_backend(self._backend)
            self._simulated = True
        self._estimator = EstimatorV2(mode=self._backend)
        self.num_qubits = num_pairs * 2
        self._angle = angle
        self._measurements: dict[int, dict[tuple, int]] = {i: {basis: 0 for basis in BASES} for i in range(num_pairs)}
        self._num_measurements: dict[tuple, int] = {basis: 0 for basis in BASES}

    
    def _generate_entangled_qubits(self) -> QuantumCircuit:
        circuit = QuantumCircuit(self.num_qubits)
        circuit.h(range(0, self.num_qubits, 2))
        circuit.cx(range(0, self.num_qubits, 2), range(1, self.num_qubits, 2))
        circuit.ry(self._angle, range(0, self.num_qubits, 2))
        return circuit


    def generate_numbers(self, num_shots: int) -> str:
        if not num_shots:
            return ''
        circuit = self._generate_entangled_qubits()
        circuit.measure_all()
        pass_manager = generate_preset_pass_manager(backend=self._backend, optimization_level=1)
        circuit = pass_manager.run(circuit)

        result = self._sampler.run([circuit], shots=num_shots).result()
        if self._simulated:
            counts = result.get_counts(0)
            bits = ''.join(counts.keys())
        else:
            bitstrings = result[0].data.meas.get_bitstrings()
            bits =  ''.join(bitstrings)

        return bits[::2]


    def check_measurement(self, basis: tuple, num_shots: int) -> None:
        if not num_shots:
            return
        circuit = self._generate_entangled_qubits()
        A, B = basis
        if A == 'X':
            circuit.h(range(0, self.num_qubits, 2))
        if B == 'X':
            circuit.h(range(1, self.num_qubits, 2))
        circuit.measure_all()
        pass_manager = generate_preset_pass_manager(target=self._backend.target, optimization_level=3)
        circuit: QuantumCircuit = pass_manager.run(circuit)
        
        result = self._sampler.run([circuit], shots=num_shots).result()
        if self._simulated:
            counts = result.get_counts()
        else:
            bitstrings = result[0].data.meas.get_bitstrings()
            counts= dict(Counter(bitstrings))
        
        for key in self._measurements.keys():
            for measurement, count in counts.items():
                pair_measurement = measurement[2*key:2*key+2]
                if pair_measurement[0] == pair_measurement[1]:
                    self._measurements[key][basis] += count
                else:
                    self._measurements[key][basis] -= count

        self._num_measurements[basis] += num_shots

    
    def get_violations(self) -> list[float]:
        return [
            (
                (self._measurements[i]['Z', 'Z'] / self._num_measurements['Z', 'Z'])
                + (self._measurements[i]['X', 'Z'] / self._num_measurements['X', 'Z']) 
                - (self._measurements[i]['Z', 'X'] / self._num_measurements['Z', 'X'])
                + (self._measurements[i]['X', 'X'] / self._num_measurements['X', 'X']) 
            )
            for i in range(self.num_qubits // 2)
        ]

    def _chsh_operator(self, base, i):
        A, B = base

        def _pad(a, b):
            return 'I' * i + a + b + 'I' * (self.num_qubits - i - 2)
        
        return SparsePauliOp.from_list(
            [
                (_pad(A, A), 1),
                (_pad(A, B), 1),
                (_pad(B, A), -1),
                (_pad(B, B), 1)
            ]
        )