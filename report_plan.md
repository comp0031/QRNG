# Quantum Random Number Generation Research Report Plan

## 1. Abstract
- Brief overview of the research project
- Summary of the different QRNG methods compared
- Highlights of key findings
- Mention of randomness extractors and evaluation metrics

## 2. Introduction
- Importance of true randomness in computing and cryptography
- Limitations of classical PRNGs
- Quantum mechanics as a source of true randomness
- Overview of the three QRNG methods being studied
- Research objectives and structure of the report

## 3. Quantum Error Correction
- Theoretical vs. practical randomness generation
- Sources of error in quantum computers
- Discussion of depolarization, thermal relaxation, and readout errors
- Experiments with unitary rotation to mitigate errors
- Results and limitations of error correction approach

## 4. Basic QRNG
- Theoretical foundation (superposition principle)
- Circuit design (Hadamard gate approach)
- Implementation details on IBM quantum hardware
- Analysis of raw output characteristics
- Limitations and sources of bias

## 5. Device-Independent Quantum Random Number Generation
### 5.1 Bipartite DIQRNG
- Bell's inequality and CHSH inequality explanation
- Entanglement-based protocol description
- Check rounds vs. generation rounds
- Security advantages over device-dependent QRNG
- Implementation challenges

### 5.2 Tripartite DIQRNG
- GHZ states and three-qubit entanglement
- Mermin's inequality explanation
- Protocol description and implementation
- Advantages and limitations compared to bipartite approach

## 6. Randomness Extraction
### 6.1 Unseeded Extraction
- Von Neumann extractor
- Other unseeded approaches
- Analysis of effectiveness

### 6.2 Seeded Extraction
- Universal hash families
- Trevisan's extractor
- Implementation details
- Performance evaluation

## 7. Evaluation and Comparison
- Entropy analysis of raw outputs
- Statistical test suite results (NIST, Diehard, etc.)
- Computational efficiency comparison
- Security analysis
- Hardware requirements and practical considerations

## 8. Conclusion
- Summary of key findings
- Recommendations for practical QRNG implementation
- Future research directions

## 9. References
- Academic papers
- Quantum computing resources
- Statistical testing frameworks 