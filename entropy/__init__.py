from .shannon import shannon_entropy
from .chisquared import chi_squared_entropy
from .bias import bias
from .min_entropy import min_entropy 
from .collision import collision_entropy
from .renyi import renyi_entropy
from .chsh_entropy import chsh_min_entropy
from .bit_efficiency import bit_efficiency
# from .compression import compression_entropy
# from .markov import markov_entropy
from .utils import measure_time, scalability

METHODS = {
    "shannon": shannon_entropy,
    "chi_squared": chi_squared_entropy,
    "bias": bias,
    "min_entropy": min_entropy,
    "collision": collision_entropy,
    "renyi": renyi_entropy,
    "chsh": chsh_min_entropy,
    "bit_efficiency": bit_efficiency
    # "markov": markov_entropy,
    # "compression": compression_entropy,
}

__all__ = ["METHODS", "measure_time", "scalability"]
