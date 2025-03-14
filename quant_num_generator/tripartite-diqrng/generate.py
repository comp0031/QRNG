from qiskit import QuantumCircuit, ClassicalRegister
from qiskit.primitives import StatevectorSampler
from enum import Enum
import random as Random


class Round(Enum):
    GENERATE = 0
    CHECK = 1


def create_ghz_circuit():
    qc = QuantumCircuit(3, 3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(0, 2)
    return qc


def generate(rounds: list[int]):
    random_numbers = ""
    qc = create_ghz_circuit()

    for round in rounds:
        if Round(round) == Round.GENERATE:
            bitstrings = generate_numbers(qc)
            select_nth_from_sequence(bitstrings)
        elif Round(round) == Round.CHECK:
            violations = chsh_circuit.check_chsh(next(bases_iter))
            failures = [v for v in violations if v < threshold]
            if failures:
                raise AbortGeneration(failurs, threshold)
        else:
            raise ValueError(f"Round type not recognised: {round}")
    return random_numbers


def generate_numbers(qc: QuantumCircuit) -> list[str]:
    qc.measure_all()
    sampler = StatevectorSampler()
    pub = qc
    job_sampler = sampler.run([pub])
    result_sampler = job_sampler.result()[0]
    bitstrings = result_sampler.data.meas.get_bitstrings()
    return bitstrings


def select_nth_from_sequence(bitstrings: list[str]) -> str:
    random = Random.randint(0, 2)
    res = []
    if bitstrings:
        res = [bitstring[random] for bitstring in bitstrings]
    return "".join(res)

