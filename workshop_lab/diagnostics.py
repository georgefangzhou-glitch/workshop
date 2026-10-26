"""Pairwise finite-value Spearman with average ties and explicit aggregation."""
from math import sqrt
from .alignment import finite


def average_ranks(values):
    if not all(finite(v) for v in values):
        raise ValueError("Rank input must be finite")
    order = sorted(range(len(values)), key=values.__getitem__)
    ranks = [0.0] * len(values)
    start = 0
    while start < len(order):
        end = start + 1
        while end < len(order) and values[order[end]] == values[order[start]]:
            end += 1
        rank = (start + 1 + end) / 2
        for pos in order[start:end]:
            ranks[pos] = rank
        start = end
    return ranks


def spearman(x, y, min_pairs=3):
    if len(x) != len(y):
        raise ValueError("Pair axes differ")
    if min_pairs < 3:
        raise ValueError("Require at least three pairs")
    pairs = [(a, b) for a, b in zip(x, y) if finite(a) and finite(b)]
    if len(pairs) < min_pairs:
        return None
    a, b = (average_ranks(list(v)) for v in zip(*pairs))
    a = [v - sum(a)/len(a) for v in a]
    b = [v - sum(b)/len(b) for v in b]
    denominator = sqrt(sum(v*v for v in a) * sum(v*v for v in b))
    return sum(u*v for u, v in zip(a, b)) / denominator if denominator else None


def correlation_summary(values):
    clean = [v for v in values if finite(v)]
    return {"valid_days": len(clean),
            "mean_signed": sum(clean)/len(clean) if clean else None,
            "mean_absolute": sum(abs(v) for v in clean)/len(clean) if clean else None}


def coverage(rows):
    return [{"valid": sum(finite(v) for v in row.values()),
             "missing": sum(not finite(v) for v in row.values())} for row in rows]
