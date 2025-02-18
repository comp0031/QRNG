from .shannon import shannon_entropy
from .chisquared import chi_squared_entropy
# from .compression import compression_entropy
# from .markov import markov_entropy

METHODS = {
    "shannon": shannon_entropy,
    "chi_squared": chi_squared_entropy,
    # "markov": markov_entropy,
    # "compression": compression_entropy,
}

__all__ = ["METHODS"]
