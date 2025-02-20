import numpy as np

def mean(file_path: str):
    """
    A function to calculate the mean from a text file containing 1s and 0s using numpy (for speed)

    params:
        file_path (str) -> path from the location of the function call to the text file
    

    returns:
        float -> the mean of the data
    """
    data = []

    # handle binary file
    if file_path.endswith('.bin'):
        data = np.fromfile(file_path, dtype=np.uint8)
        bits = np.unpackbits(data)
        total = bits.size
        count1 = np.count_nonzero(bits == 1)

        return count1 / total

    # handle text file
    elif file_path.endswith('.txt'):
        arr = np.fromfile(file_path, dtype=np.uint8)
        total = arr.size
        count1 = np.count_nonzero(arr == ord('1'))

        return count1 / total
