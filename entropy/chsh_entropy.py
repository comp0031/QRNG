import numpy as np

def chsh_min_entropy(chsh1: float, chsh2: float) -> float:
    """
    Computes min-entropy based on CHSH violation for device-independent randomness.
    
    Parameters:
        chsh1 (float): CHSH1 estimate from experiment.
        chsh2 (float): CHSH2 estimate from experiment.

    Returns:
        float: Min-entropy (higher means more quantum randomness).
    """
    #CHSH limits
    # Classical bound (no quantum advantage)
    # Max quantum violation (~2.828)

    classical_limit = 2.0  
    quantum_limit = 2 * np.sqrt(2)  

    def compute_single_min_entropy(chsh_value: float) -> float:
        """
        Computes min-entropy from a single CHSH estimate.
        """

        chsh_value = max(classical_limit, min(chsh_value, quantum_limit))

        P_guess = 0.5 + 0.5 * np.sqrt(2 - (chsh_value**2) / 4)
        P_guess = min(1.0, P_guess)

        # compute min-entropy
        return -np.log2(P_guess)

    #min-entropy
    min_entropy_1 = compute_single_min_entropy(chsh1)
    min_entropy_2 = compute_single_min_entropy(chsh2)

    return min(min_entropy_1, min_entropy_2)
