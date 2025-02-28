from .shannon import shannon_entropy
from .chisquared import chi_squared_entropy
from .mean import mean
from .min_entropy import min_entropy 
from .collision import collision_entropy
from .renyi import renyi_entropy
from .chsh_entropy import chsh_min_entropy
# from .compression import compression_entropy
# from .markov import markov_entropy

METHODS = {
    "shannon": shannon_entropy,
    "chi_squared": chi_squared_entropy,
    "mean": mean,
    "min_entropy": min_entropy,
    "collision": collision_entropy,
    "renyi": renyi_entropy,
    "chsh": chsh_min_entropy
    # "markov": markov_entropy,
    # "compression": compression_entropy,
}

__all__ = ["METHODS"]
