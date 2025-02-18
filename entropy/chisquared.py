import numpy as np

def chi_squared_entropy(file_path: str) -> float:
    """
    Computes the chi-squared statistic for a file containing only '0's and '1's.
    
    The chi-squared statistic is computed as:
    
        chi2 = ((observed0 - expected)^2 / expected) + ((observed1 - expected)^2 / expected)
    
    where expected = total_count / 2.
    
    Parameters:
        file_path (str): The path to the file.
    
    Returns:
        float: The chi-squared statistic.
    """

    # handle binary
    if file_path.endswith('.bin'):
        data = np.fromfile(file_path, dtype=np.uint8)
        total = data.size
        count0 = np.count_nonzero(data == 0)
        count1 = np.count_nonzero(data == 1)
    
    # handle text
    elif file_path.endswith('.txt'):
        
        with open(file_path, 'r') as f:
            text = f.read()
        total = len(text)
        # convert to numpy array of ASCII codes.
        arr = np.frombuffer(text.encode('ascii'), dtype=np.uint8)
        count0 = np.count_nonzero(arr == ord('0'))
        count1 = np.count_nonzero(arr == ord('1'))

    # avoid 0s error 
    if total == 0:
        return 0.0

    # expected distribution of half 1s and half 0s
    expected = total / 2.0

    # computer chisquared
    chi2 = ((count0 - expected) ** 2) / expected + ((count1 - expected) ** 2) / expected
    return chi2
