from wurlitzer import pipes
import cryptomite as cm
import numpy as np
import contextlib
import threading
import time
import math
import io
import sys
import re
import os
from concurrent.futures import ThreadPoolExecutor

class SeededExtractors():
    def __init__(self, filepaths, methods):
        self.filepaths = filepaths
        self.methods = methods
        data_sets = {}
        self.k1_values = {}
        self.per_bit_entropies = {}
        self.extracted_data = {}
        self.entropies = {}
        for name, path in filepaths.items():
            if os.path.exists(path):
                data_sets[name] = self.load_binary(path)
                print(f"Loaded {name}: {len(data_sets[name])} bits")
            else:
                print(f"File {path} not found.")
        self.data_sets = data_sets
        for name, bit_array in self.data_sets.items():
            self.k1_values[name], self.per_bit_entropies[name] = self.estimate_min_entropy_frequency(bit_array)


    def estimate_min_entropy_frequency(self, bit_array):
        n = len(bit_array)
        counts = np.bincount(bit_array)
        if len(counts) < 2 or np.sum(counts) == 0:
            return 0.0, 0.0
        p_max = np.max(counts) / n
        per_bit_entropy = -np.log2(p_max)
        total_min_entropy = n * per_bit_entropy
        return total_min_entropy, per_bit_entropy
    
    def load_binary(self, file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        bit_array = np.unpackbits(np.frombuffer(data, dtype=np.uint8))
        return bit_array
    
    def extract_randomness_toeplitz(self, bit_array, k1, epsilon=2**-32):
        n = len(bit_array)
        m = max(1, int(k1 - 2 * np.log2(1 / epsilon)))
        seed_length = n + m - 1
        extractor = cm.toeplitz.Toeplitz(n, m)
        seed = np.random.randint(0, 2, seed_length).tolist()
        extracted_bits = extractor.extract(bit_array.tolist(), seed)
        return extracted_bits

    def extract_randomness_circulant(self, bit_array, k1, epsilon=2**-32):
        n = len(bit_array)
        # Ensure that n+1 is prime:
        required_seed_length = cm.utils.previous_prime(n + 1)
        n_valid = required_seed_length - 1
        if n_valid != n:
            print(f"Warning: For circulant extraction, adjusting input length from {n} to {n_valid} to meet prime requirements.")
            bit_array = bit_array[:n_valid]
            n = n_valid
        m = max(1, int(k1 - 2 * np.log2(1 / epsilon)))
        seed_length = n + 1  # Now guaranteed to be prime.
        extractor = cm.circulant.Circulant(n, m)
        seed = np.random.randint(0, 2, seed_length).tolist()
        extracted_bits = extractor.extract(bit_array.tolist(), seed)
        return extracted_bits

    def extract_randomness_dodis(self, bit_array, k1, k2=None, epsilon=2**-32):
        n = len(bit_array)
        n_valid = cm.utils.previous_na_set(n)
        if n_valid != n:
            print(f"Warning: For Dodis extraction, adjusting input length from {n} to {n_valid} to meet prime with primitive root 2 requirement.")
            bit_array = bit_array[:n_valid]
            n = n_valid
        
        if k2 is None:
            k2 = n
        
        m = max(1, int(k1 + k2 - n - 2 * np.log2(1 / epsilon)))
        
        seed_bits = np.random.randint(0, 2, n).tolist()
        
        extractor = cm.dodis.Dodis(n, m)
        
        extracted_bits = extractor.extract(list(bit_array), seed_bits)
        return extracted_bits
    
    def extract_randomness_trevisan(self, bit_array, k1, error=2**-32, seed_length=1):
        n = len(bit_array)
        extractor = cm.trevisan.Trevisan(n, int(k1), error)
        try:
            # Try extraction with the given seed_length.
            seed = np.random.randint(0, 2, seed_length).tolist()
            return extractor.extract(bit_array.tolist(), seed)
        except RuntimeError:
            # If extraction fails, capture the C++ cerr output using wurlitzer.pipes.
            with pipes() as (out, err):
                try:
                    extractor.extract(bit_array.tolist(), np.random.randint(0, 2, seed_length).tolist())
                except RuntimeError:
                    pass  # Expected to fail.
            captured = err.getvalue()
            # Look for a pattern like "Expected: 458752" in the captured output.
            m = re.search(r'Expected:\s*(\d+)', captured)
            if m:
                proper_seed_length = int(m.group(1))
                seed = np.random.randint(0, 2, proper_seed_length).tolist()
                # Parallelize the extraction process
                with ThreadPoolExecutor() as executor:
                    future = executor.submit(extractor.extract, bit_array.tolist(), seed)
                    return future.result()
            else:
                raise RuntimeError("Could not determine expected seed length from cerr output")

    def call_extractors(self, bits, k1):
        data = {}
        for method in self.methods:
            if method == "toeplitz":
                data["toeplitz"] = self.extract_randomness_toeplitz(bits, k1)
            elif method == "circulant":
                data["circulant"] = self.extract_randomness_circulant(bits, k1)
            elif method == "dodis":
                data["dodis"] = self.extract_randomness_dodis(bits, k1)
            elif method == "trevisan":
                data["trevisan"] = self.extract_randomness_trevisan(bits, k1)
        return data

    def extract_randomness(self):
        for name, bits in self.data_sets.items():
            print(f"extracting from {name}")
            if len(bits) > 1 and name in self.k1_values:
                k1 = self.k1_values[name]
                if k1 > 0:
                    self.extracted_data[name] = self.call_extractors(bits, k1)
                    # self.extracted_data[name] = {
                    #     "toeplitz": self.extract_randomness_toeplitz(bits, k1),
                    #     "circulant": self.extract_randomness_circulant(bits, k1),
                    #     "dodis": self.extract_randomness_dodis(bits, k1),
                    #     "trevisan": self.extract_randomness_trevisan(bits, k1)
                    # }
                    print(f"Extracted random bits for {name}")
                else:
                    print(f"Skipping {name}, insufficient min-entropy (k1 <= 0)")
            else:
                print(f"Skipping {name}, not enough bits for extraction or missing k1 value")

    def extract_entropies(self):
        for name, methods in self.extracted_data.items():
            og_entropy = self.k1_values[name]
            og_entropy_per_bit = self.per_bit_entropies[name]
            entropies_name = {}
            for method, result in methods.items():
                method_entropy, method_entropy_per_bit = self.estimate_min_entropy_frequency(result)
                entropies_name[method] = {'overall_entropy' : method_entropy,
                                        'per_bit_entropy' : method_entropy_per_bit}
            self.entropies[name]=entropies_name
        for name in self.filepaths.keys():
            print(f"For {name}, starting with a total entropy of {self.k1_values[name]} and a per bit entropy of {og_entropy_per_bit}")
            for method in self.methods:
                print(f"using {method} extraction")
                print(f"total entropy - {self.entropies[name][method]['overall_entropy']}")
                print(f"entropy per bit - {self.entropies[name][method]['per_bit_entropy']}")
            print("")
        return self.entropies
    
    def write_output(self, destination="extracted_output"):
        for name, methods in self.extracted_data.items():
            for method, result in methods.items():
                filepath = f"{destination}/{method}/{name}.bin"
                if not os.path.exists(os.path.dirname(filepath)):
                    os.makedirs(os.path.dirname(filepath))
                with open(filepath, "wb") as f:
                    f.write(np.packbits(np.array(result, dtype=np.uint8)))
                print(f"Extracted bits written to {filepath}")
    
if __name__ == '__main__':
    files = {
    "1024_input": "q_gen_input/1024_quantum.bin",
    "10k_input": "q_gen_input/10k_quantum.bin",
    "10k_0s_input": "q_gen_input/10k_0s.bin",
    # "420k_input": "q_gen_input/420k_q_error_corrected.bin",
    # "12M_input": "q_gen_input/12M_quantum.bin",
    # "100k_FakeBrisbane": "q_gen_input/100_kFakeBrisbane_sim.bin",
    # "100k_FakeKyiv": "q_gen_input/100_kFakeKyiv_sim.bin",
    # "100k_FakeSherbrooke": "q_gen_input/100_kFakeSherbrooke_sim.bin",
    }
    methods = ["trevisan"] #"toeplitz", "circulant", "dodis"]#, "trevisan"]

    seeded_extractor = SeededExtractors(files, methods)
    seeded_extractor.extract_randomness()
    seeded_extractor.extract_entropies()