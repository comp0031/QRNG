import numpy as np
from collections import Counter

def collision_entropy(file_path: str) -> float:
    """
    Computes the Collision Entropy for a file containing '0's and '1's.
    
    Collision Entropy is defined as:
        H_2 = -log2( sum(P(x)^2) )
    where P(x) is the probability of each unique value in the bitstream.

    Parameters:
        file_path (str): The path to the file.

    Returns:
        float: The collision entropy value.
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

    # calculate probabilities
    probabilities = [count / total for count in counts.values()]
    
    # calculate collision entropy
    return -np.log2(sum(p ** 2 for p in probabilities))
