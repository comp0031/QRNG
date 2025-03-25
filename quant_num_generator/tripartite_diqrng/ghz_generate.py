from enum import Enum
import math
from itertools import cycle

from tripartite_diqrng import ghz_circuits


class AbortGeneration(Exception):

    def __init__(
        self, violations: list[float], upper_bound: float, lower_bound: float
    ) -> None:
        message = f"Aborted. Mermin violation ({violations}) do not satisfy bounds [{upper_bound};{lower_bound}]"
        super().__init__(message)


class Round(Enum):
    GENERATE = 0
    CHECK = 1


def generate(
    rounds: list[int],
    num_triple: int,
    token: str | None,
    bases: list[tuple] | None,
    gen_shots: int = 1,
    check_shots=10,
    uncertainty=0.20,
) -> str:
    """
    Generate random numbers using the GHZ protocol. The length of sequence generated will \
        be the product of the number of triples, the number of shots, and the number of GENERATE \
        rounds.
    
    Parameters:
        rounds (list[int]): A list of integers representing the rounds to run. 0 for GENERATE, 1 \
            for CHECK.
        num_triples (int): The number of ghz states to use.
        token (str | None): The IBM Quantum token to use. If None, a simulated circuit will be \
            used.   
        bases (list[tuple] | None): A list of tuples representing the bases to use for each round.\
             If None, the bases will cycle through the default bases. Bases should be 3-tuple of \
            strings, either 'X' or 'Y'.
        gen_shots (int): The number of shots to use for the GENERATE round.
        check_shots (int): The number of shots to use for the CHECK round.
        uncertainty (float): The uncertainty to allow in the Mermin violations.
        angle (float): The angle to use for the entangled qubits. Maximal Mermin violations are \
            produced when angle = pi/2.
    
    Returns:
        str: A string of random numbers generated using the GHZ protocol.

    Raises:
        AbortGeneration: If the CHSH violations do not satisfy the threshold.
    """
    random_numbers = ""
    bounds = get_bounds(uncertainty)
    lower_bound, upper_bound = bounds[0], bounds[1]
    iter_bases = (
        iter(bases)
        if bases
        else cycle([("X", "X", "X"), ("X", "Y", "Y"), ("Y", "X", "Y"), ("Y", "Y", "X")])
    )
    ghz_circuit = ghz_circuits.GHZCircuit(num_triple, token)
    num_gens = 0

    for round in rounds:
        if Round(round) == Round.GENERATE:
            num_gens += 1
        elif Round(round) == Round.CHECK:
            random_numbers += ghz_circuit.generate_numbers(
                num_shots=gen_shots * num_gens
            )
            num_gens = 0
            ghz_circuit.check_measurement(next(iter_bases), num_shots=check_shots)
        else:
            raise ValueError(f"Round type not recognised: {round}")

    violations = ghz_circuit.get_violations()
    print("Violations")
    print("==========")
    print("vio", violations)
    failures = [v for v in violations if v < lower_bound or v > upper_bound]
    if failures:
        raise AbortGeneration(failures, lower_bound, upper_bound)

    # Generate any remaining random numbers
    random_numbers += ghz_circuit.generate_numbers(num_shots=gen_shots * num_gens)
    return random_numbers


def get_bounds(uncertainty: float) -> float:
    if uncertainty > 1:
        raise ValueError("Uncertainty cannot be greater than 1")
    lower_bound = 2 * (math.sqrt(2) - uncertainty * (math.sqrt(2) - 1))
    upper_bound = 4
    return (lower_bound, upper_bound)
