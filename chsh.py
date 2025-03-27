import numpy as np

def chsh_min_entropy(*chsh: float) -> float:
    """
    Computes min-entropy based on CHSH violation for device-independent randomness.
    
    Parameters:
        chsh (float): CHSH estimates from experiments.

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

    return min(map(lambda x: compute_single_min_entropy(x), chsh))

print("===== CHSH =====")

CHSHS = [2.774666666666667, 2.763466666666667, 2.7306, 2.6206, 2.7123333333333335, 2.7248]
print("Using CHSHs: ", CHSHS)
print("Min Entropy Is: ", chsh_min_entropy(*CHSHS))
