import numpy as np
from .min_entropy import min_entropy

def bit_efficiency(file_path: str) -> float:
    """
    calculates bit efficiency as min-entropy per input bit.
    Higher values (up to 1) indicate more efficient randomness.

    params:
        file_path (str): Path to the file.

    returns:
        float: Min-entropy divided by total bits.
    """
    min_ent = min_entropy(file_path)
    if file_path.endswith('.bin'):
        data = np.fromfile(file_path, dtype=np.uint8)
        total_bits = data.size * 8  # 8 bits per byte
    elif file_path.endswith('.txt'):
        with open(file_path, 'r') as f:
            total_bits = len(f.read())
    else:
        return 0.0
    if total_bits == 0:
        return 0.0
    # print(f"{file_path}: min_ent={min_ent:.6f}, total_bits={total_bits}, bytes={data.size if file_path.endswith('.bin') else 'N/A'}")
    return min_ent / total_bits