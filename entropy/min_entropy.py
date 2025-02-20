import numpy as np
from collections import Counter

def min_entropy(file_path: str) -> float:
    """
    Computes the Min-Entropy for a file containing '0's and '1's.
    
    Min-Entropy is defined as:
        H_inf = -log2(max(P(x)))
    where P(x) is the probability of the most frequent symbol in the bitstream.

    Parameters:
        file_path (str): The path to the file.

    Returns:
        float: The min-entropy value.
    """

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
        # invalid file ext
        return 0.0

    # compute probabilities and find the max
    max_count = max(counts.values())
    max_prob = max_count / total

    # min-entropy = -log2(max_prob)
    return -np.log2(max_prob)
