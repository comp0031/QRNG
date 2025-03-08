from enum import Enum
import math

from diqrng import circuits


class AbortGeneration(Exception):

    def __init__(self, violations: list[float], threshold: float) -> None:
        message = f"Aborted. CHSH violations ({violations}) do not satisfy threshold ({threshold})"
        super().__init__(message)


class Round(Enum):
    GENERATE = 0
    CHECK = 1


def generate(rounds: list[int], bases: list[tuple], qubits: int, token: str | None, uncertainty=0.10):
    random_numbers = ""
    threshold = _get_threshold(uncertainty)
    bases_iter = iter(bases)
    chsh_circuit = circuits.ChshCircuit(qubits, token)

    for round in rounds:
        if Round(round) == Round.GENERATE:
            random_numbers += chsh_circuit.generate_numbers()
        elif Round(round) == Round.CHECK:
            violations = chsh_circuit.check_chsh(next(bases_iter))
            failures = [v for v in violations if v < threshold]
            if failures:
                raise AbortGeneration(failures, threshold)
        else:
            raise ValueError(f"Round type not recognised: {round}")
    return random_numbers


def _get_threshold(uncertainty: float) -> float:
    if uncertainty > 1:
        raise ValueError("Uncertainty cannot be greater than 1")
    return 2 * (math.sqrt(2) - uncertainty * (math.sqrt(2) - 1))