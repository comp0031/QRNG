from typing import List
import numpy as np
import os
from dotenv import load_dotenv

from qiskit import QuantumCircuit, generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2

LENGTH = 10000
FILENAME = 'bitstream.txt'

load_dotenv()

circ = QuantumCircuit(1)
circ.h(0)
circ.measure_all()

service = QiskitRuntimeService(channel="ibm_quantum", token=os.getenv('IBMQ_API_TOKEN'))
backend = service.least_busy(simulator=False, operational=True)
print(backend)
pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa_circ = pm.run(circ)

sampler = SamplerV2(mode=backend)
sampler.options.default_shots = LENGTH

job = sampler.run([isa_circ])

# Use the job ID to retrieve your job data later
print(f">>> Job ID: {job.job_id()}")

result = job.result()
bitstring = result[0].data.meas.get_bitstrings()
bitstream_quantum = ''.join(bitstring)
# Write the bitstream to a file
with open(FILENAME, 'w') as f:
    f.write(bitstream_quantum)