# Quantum Random Bitstring Generation

This section focuses on the generation of random bitstrings via simulated and real quantum computation.

## Current Files
- `simulated_comp.py` does repeated generation of random bitstrings using a simulated quantum computer and python's random module. A basic entropy measure is taken of both, and averaged across many iterations.
- `ibmq_generation.py` submits a a job to IBMQ to generate a random bitstring of a length defined in the file's `LENGTH` constant. It saves this bitstring to a file defined in the `FILENAME` constant.
- `10k_quantum.txt` contains a 10000 character bitstring generated on IBMQ's ibm_kyiv, taking 4s. Job ID: cyjqhmenrmz0008tgg5g
- `1024_quantum.txt` contains a 1024 character bitstring generated on IBMQ's ibm_kyiv, taking 2s. Job ID: cyjqewknrmz0008tgf50

## TODO
- Add noise to the simulator to reflect realistic quantum computer behaviour
- Generate longer bitstrings with real quantum hardware
- Investigate whether the number of cubits used per run (i.e. several qubit lines and a hadamard on each) affects bias / entropy. Since IBM's free hardware has 127 qubits, using all of them would likely increase bits per second.
- Research implementing a method of compensating for compensating for rotational bias in real quantum hardware?