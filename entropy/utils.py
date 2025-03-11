import time
import numpy as np
import os

def measure_time(file_path: str, method_name: str, methods: dict, *args) -> tuple[float, float]:
    if method_name not in methods:
        raise ValueError(f"Method {method_name} not found in METHODS")
    method = methods[method_name]
    start_time = time.perf_counter()
    if method_name == "chsh":
        result = method(*args)
    else:
        result = method(file_path)
    end_time = time.perf_counter()
    return result, end_time - start_time

def scalability(file_paths: list[str], method_name: str, methods: dict) -> tuple[float, float]:
    if method_name not in methods:
        raise ValueError(f"Method {method_name} not found in METHODS")
    method = methods[method_name]
    times = []
    sizes = []
    
    for file_path in file_paths:
        if file_path.endswith('.bin'):
            size = os.path.getsize(file_path) * 8
        elif file_path.endswith('.txt'):
            with open(file_path, 'r') as f:
                size = len(f.read())
        else:
            continue
        
        n_runs = max(1000 // (size // 1000 + 1), 1)
        total_time = 0
        for _ in range(n_runs):
            start = time.perf_counter()
            method(file_path)
            total_time += time.perf_counter() - start
        times.append(total_time / n_runs)
        sizes.append(size)
    
    if len(sizes) < 2:
        return 0.0, 0.0
    
    unique_sizes = sorted(set(sizes))
    avg_times = [np.mean([t for sz, t in zip(sizes, times) if sz == s]) for s in unique_sizes]
    log_sizes = np.log10(unique_sizes)
    log_times = np.log10(avg_times)
    slope, intercept = np.polyfit(log_sizes, log_times, 1)
    return slope, intercept