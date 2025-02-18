import math
import numpy as np

def shannon_entropy(file_path: str) -> float:
    """
    A function to calculate the shannon entropy from a text file containing 1s and 0s using numpy (for speed)

    params:
        file_path (str) -> path from the location of the function call to the text file
    

    returns:
        float -> the hannon entropy for the function
    """
    with open(file_path, 'r') as f:
        data = f.read()
        
    # Filter out any characters that are not '0' or '1'
    total = len(data)
    if total == 0:
        return 0.0

    # Convert the string to a NumPy array of bytes directly.
    # This avoids creating an intermediate list.
    arr = np.frombuffer(data.encode('ascii'), dtype=np.uint8)
    
    # Count occurrences by comparing with the ASCII codes for '0' and '1'
    count0 = np.sum(arr == ord('0'))
    count1 = np.sum(arr == ord('1'))

    p0 = count0 / total
    p1 = count1 / total

    entropy = 0.0
    if p0 > 0:
        entropy -= p0 * math.log2(p0)
    if p1 > 0:
        entropy -= p1 * math.log2(p1)
    
    return entropy
