import numpy as np
from collections import Counter

def renyi_entropy(file_path: str, alpha: float = 2.0) -> float:
    """
    Computes the Rényi Entropy of order α for a file containing '0's and '1's.

    Rényi Entropy is defined as:
        H_α = (1 / (1 - α)) * log2( sum(P(x)^α) )
    where P(x) is the probability of each unique value in the bitstream.

    Parameters:
        file_path (str): The path to the file.
        alpha (float): The order of Rényi entropy. Default is 2.

    Returns:
        float: The Rényi entropy value.
    """

    if alpha <= 0 or alpha == 1:
        raise ValueError("Rényi entropy is not defined for α ≤ 0 or α = 1")

    # Handle binary files
    if file_path.endswith('.bin'):
        data = np.fromfile(file_path, dtype=np.uint8)
        bits = np.unpackbits(data)
        total = bits.size
        if total == 0:
            return 0.0
        counts = Counter(bits)

    # Handle text files
    elif file_path.endswith('.txt'):
        with open(file_path, 'r') as f:
            text = f.read()
        total = len(text)
        if total == 0:
            return 0.0
        arr = np.frombuffer(text.encode('ascii'), dtype=np.uint8)
        count0 = np.count_nonzero(arr == ord('0'))
        count1 = np.count_nonzero(arr == ord('1'))
        counts = {0: count0, 1: count1}

    else:
        return 0.0

    # calculate probabilities
    probabilities = [count / total for count in counts.values()]
    
    # calculate renyi entropy
    sum_p_alpha = sum(p ** alpha for p in probabilities)
    renyi_value = (1 / (1 - alpha)) * np.log2(sum_p_alpha)

    return renyi_value
