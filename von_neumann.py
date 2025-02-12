import cryptomite
from math import log2
from collections import Counter
import os

# files
files = {
    "12M_input": "q_gen_input/12M_quantum.bin",
    "10k_input": "q_gen_input/10k_quantum.bin",
    "1024_input": "q_gen_input/1024_quantum.bin",
    "10k_0s_input": "q_gen_input/10k_0s.bin",
    "420k_input": "q_gen_input/420k_q_error_corrected.bin",
}
bitstring_length = {
    "12M_input": [],
    "10k_input": [],
    "1024_input": [],
    "10k_0s_input": [],
    "420k_input": [],
}
entropies = {
    "12M_input": [],
    "10k_input": [],
    "1024_input": [],
    "10k_0s_input": [],
    "420k_input": [],
}


# Get Bits
def unpack(file):
    with open(file, "rb") as f:
        data = f.read()
    bit_seq = "".join(format(byte, "08b") for byte in data)

    return bit_seq


# Extraction
def extraction():
    for name, file in files.items():
        binary = unpack(file)
        bitstring_length[name].append(len(binary))
        entropy = calc_shannon_entropy(binary)
        entropies[name].append(entropy)
        von_neuman_extractor = cryptomite.utils.von_neumann(binary)
        bitstring_length[name].append(len(von_neuman_extractor))
        entropy_extraction = calc_shannon_entropy(von_neuman_extractor)
        entropies[name].append(entropy_extraction)
        with open(f"extractor_output/{name}.txt", "a") as f:
            f.write("".join(x for x in von_neuman_extractor))


# Bit loss
def bit_loss():
    for name, lengths in bitstring_length.items():
        if lengths[0] != 0:
            loss = (1 - (lengths[1] / lengths[0])) * 100
            print(f"The bit loss percentage on the input :{name} is {loss}%.")
        else:
            print(f"input bit string is empty")


# Shannon Entropy
def calc_shannon_entropy(original_bitstring):
    total_length = len(original_bitstring)
    bit_counts = Counter(original_bitstring)
    p0, p1 = bit_counts["0"] / total_length, bit_counts["1"] / total_length
    entropy = -(p0 * log2(p0) + p1 * log2(p1))
    return entropy


def print_entropy():
    for name, entropy in entropies.items():
        print(
            f"For {name} the start entropy is :{entropy[0]} and the entropy post extraction is : {entropy[1]}"
        )


extraction()
bit_loss()
print_entropy()
