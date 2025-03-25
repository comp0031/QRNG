from enum import Enum
import math
from itertools import cycle

from diqrng import circuits


class AbortGeneration(Exception):

    def __init__(self, violations: list[float], threshold: float) -> None:
        message = f"Aborted. CHSH violations ({violations}) do not satisfy threshold ({threshold})"
        super().__init__(message)


class Round(Enum):
    GENERATE = 0
    CHECK = 1


def generate(
        rounds: list[int],
        num_pairs: int,
        token: str | None,
        bases: list[tuple] | None,
        gen_shots: int=1,
        check_shots=10,
        uncertainty=0.20,
        angle=math.pi/4
    ) -> str:
    """
    Generate random numbers using the CHSH protocol. The number of random numbers generated will \
        be the product of the number of pairs, the number of shots, and the number of GENERATE \
        rounds.
    
    Parameters:
        rounds (list[int]): A list of integers representing the rounds to run. 0 for GENERATE, 1 \
            for CHECK.
        num_pairs (int): The number of pairs of entangled qubits to use.
        token (str | None): The IBM Quantum token to use. If None, a simulated circuit will be \
            used.   
        bases (list[tuple] | None): A list of tuples representing the bases to use for each round.\
             If None, the bases will cycle through the default bases. Bases should be 2-tuple of \
            strings, either 'Z' or 'X'.
        gen_shots (int): The number of shots to use for the GENERATE round.
        check_shots (int): The number of shots to use for the CHECK round.
        uncertainty (float): The uncertainty to allow in the CHSH violations.
        angle (float): The angle to use for the entangled qubits. Maximal CHSH violations are \
            produced when angle = pi/4.
    
    Returns:
        str: A string of random numbers generated using the CHSH protocol.

    Raises:
        AbortGeneration: If the CHSH violations do not satisfy the threshold.
    """
    random_numbers = ""
    threshold = get_threshold(uncertainty)
    iter_bases = iter(bases) if bases else cycle([('Z', 'Z'), ('Z', 'X'), ('X', 'Z'), ('X', 'X')])
    chsh_circuit = circuits.ChshCircuit(num_pairs, token, angle)
    num_gens = 0

    for round in rounds:
        if Round(round) == Round.GENERATE:
            num_gens += 1
        elif Round(round) == Round.CHECK:
            random_numbers += chsh_circuit.generate_numbers(num_shots=gen_shots * num_gens)
            num_gens = 0
            chsh_circuit.check_measurement(next(iter_bases), num_shots=check_shots)
        else:
            raise ValueError(f"Round type not recognised: {round}")
    
    violations = chsh_circuit.get_violations()
    print("Violations")
    print("==========")
    print(violations)
    failures = [v for v in violations if v < threshold]
    if failures:
        raise AbortGeneration(failures, threshold)

    # Generate any remaining random numbers
    random_numbers += chsh_circuit.generate_numbers(num_shots=gen_shots * num_gens)
    return random_numbers

def get_threshold(uncertainty: float) -> float:
    if uncertainty > 1:
        raise ValueError("Uncertainty cannot be greater than 1")
    return 2 * (math.sqrt(2) - uncertainty * (math.sqrt(2) - 1))