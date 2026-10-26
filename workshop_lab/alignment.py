"""After-close signals matched to next-day entry and exit-dated returns.

There is no universal shift: the two positions below follow this explicit clock.
Unknown positions are retained; this module never connects to a data provider.
"""
from dataclasses import dataclass
from datetime import date
from math import isfinite
from numbers import Real


def finite(value):
    return isinstance(value, Real) and not isinstance(value, bool) and isfinite(value)


def validate_panel(dates, rows):
    if not dates or len(dates) != len(rows):
        raise ValueError("A nonempty matching calendar is required")
    if not all(isinstance(d, date) for d in dates):
        raise ValueError("Calendar values must be dates")
    if dates != sorted(set(dates)):
        raise ValueError("Calendar must be unique and increasing")
    symbols = set(rows[0])
    if not symbols or any(set(row) != symbols for row in rows):
        raise ValueError("Stock axes must be complete and identical")
    return symbols


@dataclass(frozen=True)
class AlignedDay:
    signal_date: date
    entry_date: date
    exit_date: date
    scores: dict
    returns: dict


def align_exit_dated(dates, signals, vwap, membership=None):
    """Keep return rows t+2, with signal/membership at t, entry VWAP at t+1."""
    symbols = validate_panel(dates, vwap)
    if validate_panel(dates, signals) != symbols:
        raise ValueError("Signal and price stock axes differ")
    if membership is not None:
        if validate_panel(dates, membership) != symbols:
            raise ValueError("Membership stock axes differ")
        if any(type(v) is not bool for row in membership for v in row.values()):
            raise ValueError("Historical membership must be known booleans")
    result = []
    for exit_pos in range(2, len(dates)):
        signal_pos = exit_pos - 2
        scores, returns = {}, {}
        for symbol in sorted(symbols):
            member = membership is None or membership[signal_pos][symbol]
            scores[symbol] = signals[signal_pos][symbol] if member else None
            entry, end = vwap[exit_pos-1][symbol], vwap[exit_pos][symbol]
            returns[symbol] = end / entry - 1 if finite(entry) and finite(end) and entry > 0 and end > 0 else None
        result.append(AlignedDay(dates[signal_pos], dates[exit_pos-1], dates[exit_pos], scores, returns))
    return result
