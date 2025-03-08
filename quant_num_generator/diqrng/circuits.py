import math
import numpy as np
from qiskit import QuantumCircuit, generate_preset_pass_manager
from qiskit.quantum_info import SparsePauliOp
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2, EstimatorV2
from qiskit_aer import AerSimulator

simulated = 'FakeBrisbane' # Change to simulate other QPUs
dynamic_fake_provider = __import__('qiskit_ibm_runtime.fake_provider', fromlist=[simulated])
fake = getattr(dynamic_fake_provider, simulated)


class ChshCircuit:

    def __init__(self, num_qubits: int, token: str | None) -> None:
        if num_qubits % 2:
            raise ValueError("Number of qubits must be even")
        if token:
            service = QiskitRuntimeService(channel="ibm_quantum", token=token)
            self._backend = service.least_busy(operational=True, simulator=False, min_num_qubits=num_qubits)
            self._sampler = SamplerV2(mode=self._backend)
            self._simulated = False
        else:
            print("Using simulated circuit")
            self._backend = fake()
            self._sampler = AerSimulator.from_backend(self._backend)
            self._simulated = True
        self._estimator = EstimatorV2(mode=self._backend)
        self.num_qubits = num_qubits


    def generate_numbers(self) -> str:
        # Prepare Circuit
        circuit = _generate_entangled_qubits(self.num_qubits)
        circuit.measure_all()
        pass_manager = generate_preset_pass_manager(backend=self._backend, optimization_level=1)
        circuit = pass_manager.run(circuit)

        # Run Circuit
        result = self._sampler.run([circuit], shots=1).result()
        if self._simulated:
            counts = result.get_counts(0)
            bits = list(counts.keys())[0]
        else:
            bitstrings = np.array(result[0].data.meas.get_bitstrings())
            bits =  ''.join(bitstrings)

        return bits[::2]


    def check_chsh(self, basis: tuple) -> list[float]:
        circuit = _generate_entangled_qubits(self.num_qubits)
        pm = generate_preset_pass_manager(target=self._backend.target, optimization_level=3)
        circuit: QuantumCircuit = pm.run(circuit)
        
        observables = []
        for i in range(0, self.num_qubits, 2):
            observable = self._chsh_operator(basis, i)
            observable = observable.apply_layout(circuit.layout)
            observables.append(observable)

        pub = [(
            circuit,
            observables,
        )]

        result = self._estimator.run(pubs=pub).result()
        return [float(v) for v in result[0].data.evs]

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


def _generate_entangled_qubits(num_qubits: int) -> QuantumCircuit:
    circuit = QuantumCircuit(num_qubits)
    circuit.h(range(0, num_qubits, 2))
    circuit.cx(range(0, num_qubits, 2), range(1, num_qubits, 2))
    circuit.ry(math.pi / 4, range(0, num_qubits, 2))
    return circuit