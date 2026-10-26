"""Toy equal-weight groups, not an execution/cost/production backtest engine."""
from dataclasses import dataclass
from .alignment import finite


class InsufficientUniverse(ValueError):
    pass


@dataclass(frozen=True)
class GroupResult:
    absolute: dict
    excess: dict
    counts: dict
    high_minus_low: float


def group_returns(scores, returns, benchmark, groups=10):
    if not isinstance(groups, int) or isinstance(groups, bool) or groups < 2:
        raise ValueError("At least two groups are required")
    if set(scores) != set(returns):
        raise ValueError("Score and return stock axes differ")
    if not finite(benchmark):
        raise ValueError("Unknown benchmark")
    selected = sorted((s for s, v in scores.items() if finite(v)), key=lambda s: (scores[s], s))
    if len(selected) < groups:
        raise InsufficientUniverse("Not enough valid signals for all groups")
    # Do not use realized return availability to change the selected universe.
    if any(not finite(returns[s]) for s in selected):
        raise ValueError("Unknown selected return; no dropping or zero filling")
    buckets = {str(g): [] for g in range(1, groups+1)}
    for pos, symbol in enumerate(selected):
        buckets[str(pos*groups//len(selected)+1)].append(symbol)
    absolute = {g: sum(returns[s] for s in symbols)/len(symbols) for g, symbols in buckets.items()}
    excess = {g: value-benchmark for g, value in absolute.items()}
    hl = absolute[str(groups)]-absolute['1']
    assert abs(hl-(excess[str(groups)]-excess['1'])) < 1e-12
    return GroupResult(absolute, excess, {g:len(s) for g, s in buckets.items()}, hl)
