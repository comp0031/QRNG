# Quantum Random Bitstring Generation

This section focuses on the generation of random bitstrings via tripartite device - independent quantum random number generation on simulated and real quantum computation.
## Current Folders
- `tripartite_diqrng` contains generation files and results folder `tripartite-diqrng-results`
-`diqrng` conatins bipartite genertaion files for reference. 
## Current Files
- `generate_ghz.ipynb` file to run tripartite QRNG
- `ghz_circuits.py` file that prepars generation and checking circuits + calculates Mermin value 
- `ghz_generate.py` file with main code handling the tripartite QRNG
- `mermin-testing.ipynb` Plotting two different Mermin observables against each other depending on rotation angle.
- `generate.py` initial file for tripartite qrng which uses hash of pdf file to randomly chose generation or checking round.
- `utils` file that gets hash of pdf files.

## TODO
- Test on real backend 
- Entropy Estimation 
- Agree on experiement metrics (bipartite)