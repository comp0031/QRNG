import math
from enum import Enum
import random as Random
from utils import hash_pdf_to_number

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeManilaV2
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime import EstimatorV2 as Estimator


QiskitRuntimeService.save_account(
    channel="ibm_quantum",
    token="3b804182dcf5d92a78f5342e3c48bc71edd10a6e3a857928bd90f0c4fd2af986144fdb4b99551ef6c857b615e26a1186572c0aee4ec5d460427ca1884c7b5d26",
    set_as_default=True,
    overwrite=True,
)

# Load saved credentials
service = QiskitRuntimeService()
backend = FakeManilaV2()
backend.name


class AbortGeneration(Exception):

    def __init__(self, mermin_score: float) -> None:
        upper_bound = 4
        lower_bound = 2
        if mermin_score > upper_bound:
            message = f"Aborted. Mermin score : {mermin_score} above upper bound :{upper_bound} "
        else:
            message = f"Aborted. Mermin score : {mermin_score} below lower bound : {lower_bound}"

        super().__init__(message)


class Round(Enum):
    GENERATE = "0"
    CHECK = "1"


def create_ghz_circuit():
    qc = QuantumCircuit(3, 3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(0, 2)
    return qc


def generate(rounds: str) -> str:
    random_numbers = ""
    mermin_score = 0
    qc = create_ghz_circuit()
    check_rounds = 0

    for round in rounds:
        if Round(round) == Round.GENERATE:
            
            bitstrings = generate_numbers()
            random_numbers += select_nth_from_sequence(bitstrings)

        elif Round(round) == Round.CHECK:
            
            mermin_score += check_mermin(qc)
            check_rounds += 1

    abort = check_game_score(mermin_score, check_rounds)
    if abort:
        raise AbortGeneration()

    print(len(random_numbers))
    return random_numbers

# Measure circuit to get random number 
def generate_numbers() -> list[str]:
    qc = create_ghz_circuit()
    qc.measure_all()
    sampler = StatevectorSampler()
    pub = qc
    job_sampler = sampler.run([pub], shots=1)  
    result_sampler = job_sampler.result()[0]
    bitstrings = result_sampler.data.meas.get_bitstrings()
    return bitstrings

# Randomly select 1 number from each triple
def select_nth_from_sequence(bitstrings: list[str]) -> str:
    random = Random.randint(0, 2)
    res = []
    if bitstrings:
        res = [bitstring[random] for bitstring in bitstrings]
    return "".join(res)

# Calculate the mermin score
def check_mermin(qc: QuantumCircuit) -> float:

    observable = SparsePauliOp.from_list(
        [("XXX", 1), ("XYY", -1), ("YXY", -1), ("YYX", -1)]
    )
    target = backend.target
    pm = generate_preset_pass_manager(target=target, optimization_level=3)

    ghz_circuit = pm.run(qc)
    isa_observable = observable.apply_layout(layout=ghz_circuit.layout)
    estimator = Estimator(mode=backend)

    pub = (
        ghz_circuit,  
        [[isa_observable]], 
    )

    job_result = estimator.run(pubs=[pub])
    job = estimator.run(pubs=[pub])
    job_result = job.result()
    ghz_est = job_result[0].data.evs[0]

    #print(ghz_est[0])
    return ghz_est[0]


# Calculate the average value of the mermin equation over check rounds, if under/above quantum
# threshold set the abort flag to true and abort session.
def check_game_score(scores: float, check_rounds: int) -> bool:
    abort = False
    stat_tolerance = 0.10
    lower_bound = 2 * math.sqrt(2) - stat_tolerance
    upper_bound = 4
    game_score = scores / check_rounds

    if game_score < lower_bound or game_score > upper_bound:
        abort = True

    return abort

# Save random number sequence to txt file
def save_random_nums(bitstring: str, filename: str) -> None:
    with open(
        f"quant_num_generator/tripartite-diqrng/tripartite-diqrng-results/{filename}.txt",
        "a",
    ) as f:
        f.write("".join(bitstring))


if __name__ == "__main__":

    pdf_path = (
        "quant_num_generator/tripartite-diqrng/pdfcoffee.com-emily-remler copy.pdf"
    )

    sequences = {
        "100_bits": hash_pdf_to_number(pdf_path, 256),
        "500_bits": hash_pdf_to_number(pdf_path, 1024),
        "1k_bits": hash_pdf_to_number(pdf_path, 2048),
        "4k_bits": hash_pdf_to_number(pdf_path, 8192),
    }
    for name, ran_rounds in sequences.items():
        rounds = ran_rounds
        print(len(rounds))
        bitstring = generate(rounds)
        save_random_nums(bitstring, name)
