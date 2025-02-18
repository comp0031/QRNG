from .shannon import shannon_entropy
# from .compression import compression_entropy
# from .markov import markov_entropy

METHODS = {
    "shannon": shannon_entropy,
    # "markov": markov_entropy,
    # "compression": compression_entropy,
}

__all__ = ["METHODS"]
