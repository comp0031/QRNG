from collections import Counter
import math
from qiskit import QuantumCircuit, generate_preset_pass_manager
from qiskit.quantum_info import SparsePauliOp
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2, EstimatorV2
from qiskit_aer import AerSimulator

simulated = "FakeKyiv"  # Change to simulate other QPUs
dynamic_fake_provider = __import__(
    "qiskit_ibm_runtime.fake_provider", fromlist=[simulated]
)
fake = getattr(dynamic_fake_provider, simulated)


BASES = [("X", "X", "X"), ("X", "Y", "Y"), ("Y", "X", "Y"), ("Y", "Y", "X")]


class GHZCircuit:

    def __init__(self, num_triple: int, token: str | None) -> None:
        if token:
            service = QiskitRuntimeService(channel="ibm_quantum", token=token)
            self._backend = service.least_busy(
                operational=True, simulator=False, min_num_qubits=num_triple * 3
            )
            self._sampler = SamplerV2(mode=self._backend)
            self._simulated = False
        else:
            print(f"Using simulated circuit ('{simulated}')")
            self._backend = fake()
            self._sampler = AerSimulator.from_backend(self._backend)
            self._simulated = True
        self._estimator = EstimatorV2(mode=self._backend)
        self.num_qubits = num_triple * 3
        self._measurements: dict[int, dict[tuple, int]] = {
            i: {basis: 0 for basis in BASES} for i in range(num_triple)
        }
        self._num_measurements: dict[tuple, int] = {basis: 0 for basis in BASES}

    def _generate_ghz(self) -> QuantumCircuit:
        qc = QuantumCircuit(self.num_qubits)
        # qc.h(0)
        # qc.cx(0, 1)
        # qc.cx(0, 2)
        # if self.num_qubits
        for i in range(0, self.num_qubits,3):
            qc.h(i)
            qc.cx(i, i+1)
            qc.cx(i, i+2)
        return qc

    def generate_numbers(self, num_shots: int) -> str:

        if not num_shots:
            return ""
        circuit = self._generate_ghz()
        circuit.measure_all()
        pass_manager = generate_preset_pass_manager(
            backend=self._backend, optimization_level=1
        )
        circuit = pass_manager.run(circuit)

        result = self._sampler.run([circuit], shots=num_shots, memory=True).result()
        if self._simulated:
            #counts = result.get_counts(0)
            #print(result.get_memory())
            bits = "".join(result.get_memory())
            
        else:
            bitstrings = result[0].data.meas.get_bitstrings()
            bits = "".join(bitstrings)

        return bits[::3]

    def check_measurement(self, basis: tuple, num_shots: int) -> None:
        # print("in check")
        if not num_shots:
            return
        qc = self._generate_ghz()
        
        for i,gate in enumerate(basis):
            if gate == "X":
                for j in range(0,self.num_qubits,3):
                    qc.h(i+j)
            elif gate == "Y":
                for j in range(0,self.num_qubits,3):
                    qc.sdg(i+j)
                    qc.h(i+j)
        # print("gene circi")
        qc.measure_all()
        pass_manager = generate_preset_pass_manager(
            target=self._backend.target, optimization_level=3
        )
        qc = pass_manager.run(qc)

        result = self._sampler.run([qc], shots=num_shots).result()
        counts = (
            result.get_counts()
            if self._simulated
            else dict(Counter(result[0].data.meas.get_bitstrings()))
        )

        for key in self._measurements.keys():
            for measurement, count in counts.items():
                # print(measurement, count)
                triplet_measurement = measurement[3 * key : 3 * key + 3]
                parity = (-1) ** (triplet_measurement.count("1"))
                self._measurements[key][basis] += parity * count

        self._num_measurements[basis] += num_shots

    def get_violations(self) -> list[float]:
        return [
            (
                (
                    self._measurements[i]["X", "X", "X"]
                    / self._num_measurements["X", "X", "X"]
                )
                - (
                    self._measurements[i]["X", "Y", "Y"]
                    / self._num_measurements["X", "Y", "Y"]
                )
                - (
                    self._measurements[i]["Y", "X", "Y"]
                    / self._num_measurements["Y", "X", "Y"]
                )
                - (
                    self._measurements[i]["Y", "Y", "X"]
                    / self._num_measurements["Y", "Y", "X"]
                )
            )
            for i in range(self.num_qubits // 3)
        ]
