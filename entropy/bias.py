import numpy as np

def bias(file_path: str) -> float:
    """
    calculate the bias as the absolute deviation from 0.5 (ideal randomness)
    returns a value between 0 (unbiased) and 0.5 (fully biased)

    params:
        file_path (str): Path to the file containing 0s and 1s.

    returns:
        float: Bias value (|mean - 0.5|).
    """
    # handle binary file
    if file_path.endswith('.bin'):
        data = np.fromfile(file_path, dtype=np.uint8)
        bits = np.unpackbits(data)
        total = bits.size
        if total == 0:
            return 0.0
        count1 = np.count_nonzero(bits == 1)
        mean = count1 / total

    # handle text file
    elif file_path.endswith('.txt'):
        with open(file_path, 'r') as f:
            text = f.read()
        total = len(text)
        if total == 0:
            return 0.0
        arr = np.frombuffer(text.encode('ascii'), dtype=np.uint8)
        count1 = np.count_nonzero(arr == ord('1'))
        mean = count1 / total

    else:
        return 0.0

    # return absolute deviation from 0.5
    return abs(mean - 0.5)