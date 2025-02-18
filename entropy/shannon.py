import math
import numpy as np

def shannon_entropy(file_path: str) -> float:
    """
    A function to calculate the shannon entropy from a binary file containing 1s and 0s using numpy (for speed)

    params:
        file_path (str) -> path from the location of the function call to the binary file
    

    returns:
        float -> the hannon entropy for the function
    """
    data = np.fromfile(file_path, dtype=np.uint8)
    
    total = data.size
    if total == 0:
        return 0.0

    count0 = np.sum(data == ord('0'))
    count1 = np.sum(data == ord('1'))
    
    p0 = count0 / total
    p1 = count1 / total

    entropy = 0.0
    if p0 > 0:
        entropy -= p0 * math.log2(p0)
    if p1 > 0:
        entropy -= p1 * math.log2(p1)
    return entropy
