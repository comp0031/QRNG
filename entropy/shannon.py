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
    # handle binary file
    if file_path.endswith('.bin'):
        data = np.fromfile(file_path, dtype=np.uint8)
        total = data.size
        # count 1s and 0s 
        count0 = np.count_nonzero(data == 0)
        count1 = np.count_nonzero(data == 1)

    # handle text file
    elif file_path.endswith('.txt'):
        
        with open(file_path, 'r') as f:
            text = f.read()
        total = len(text)
        # convert text to ascii codes
        arr = np.frombuffer(text.encode('ascii'), dtype=np.uint8)
        count0 = np.count_nonzero(arr == ord('0'))
        count1 = np.count_nonzero(arr == ord('1'))
    
    if total == 0:
        return 0.0

    # compute probability
    p0 = count0 / total
    p1 = count1 / total
    
    # compute entropy
    probs = np.array([p0, p1])
    # avoid div by 0 error
    non_zero = probs > 0
    entropy = -np.sum(probs[non_zero] * np.log2(probs[non_zero]))
    return entropy
