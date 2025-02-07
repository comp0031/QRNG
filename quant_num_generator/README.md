# Quantum Random Bitstring Generation

This section focuses on the generation of random bitstrings via simulated and real quantum computation.

## Current Files
- `simulated_comp.py` does repeated generation of random bitstrings using a simulated quantum computer and python's random module. A basic entropy measure is taken of both, and averaged across many iterations.
- `ibmq_generation.ipynb` submits a job to either IBMQ or a local simulator, using logical qubits to account for errors.
- `12M_quantum.bin` contains a 12 million bit bitstream generated on IBMQ's ibm_sherbrooke using 127 parallel qubits and hadamards, taking 32s over 100k shots.
- `10k_quantum.bin` contains a 10000 bit bitstream generated on IBMQ's ibm_kyiv using a single qubit and hadamard, taking 4s over 10k shots.
- `1024_quantum.bin` contains a 1024 bit bitstream generated on IBMQ's ibm_kyiv using a single qubit and hadamard, taking 2s over 1024 shots.
- `10k_0s.bin` contains the result of measuring 10000 0s on ibm_kyiv using a single qubit and immediate measurement. Shows erroneous 1 measurements.
- `420k_q_error_corrected.bin` contains 420k bit bitstream with 3:1 majority vote logical qubit error correction using IBMQ's ibm_kyiv using 126 qubits and hadamards over 10k shots, taking 5s

## TODO
- [ ] Add noise to the simulator to reflect realistic quantum computer behaviour
- [x] Generate longer bitstrings with real quantum hardware
    - Generated 12.7M bit stream.
- [ ] Investigate whether the number of cubits used per run (i.e. several qubit lines and a hadamard on each) affects bias / entropy. Since IBM's free hardware has 127 qubits, using all of them would likely increase bits per second.
- [ ] Research implementing a method of compensating for compensating for rotational bias in real quantum hardware?
    - Implemented logical qubits that resolve to the majority vote of physical qubits
