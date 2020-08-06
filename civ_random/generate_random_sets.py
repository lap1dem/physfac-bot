import numpy as np
import itertools
from typing import Tuple, List, Any

def generate_random_sets(instances: List[int], dimension: int, sum: int = 0) -> Tuple[List[Tuple[int]], List[int], List[int]]:
    combinations = list(itertools.product(instances, repeat=dimension))

    if sum > 0:
        static_sum = []
        for comb in combinations:
            if np.sum(comb) == sum:
                static_sum.append(comb)
        combinations = static_sum

    probs = np.histogram(combinations, bins=dimension)[0]
    probs = probs / np.sum(probs)
    items = np.unique(combinations)
    return (combinations, probs, items)
