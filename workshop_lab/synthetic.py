"""Generated from scratch; these are not real securities or anonymized prices."""
from datetime import date, timedelta
from math import sin, sqrt
from random import Random
from .alignment import finite


def trading_positions(count, start=date(2024, 1, 2)):
    if count < 1:
        raise ValueError("Positive calendar length required")
    days, current = [], start
    while len(days) < count:
        if current.weekday() < 5:
            days.append(current)
        current += timedelta(days=1)
    return days


def features(closes, lookback=5):
    """Only closing prices at or before the current position are used."""
    if lookback < 2 or not closes:
        raise ValueError("At least a two-position window is required")
    symbols = sorted(closes[0])
    if any(set(row) != set(symbols) for row in closes):
        raise ValueError("Stock axes differ")
    momentum, volatility = [], []
    for pos in range(len(closes)):
        m, v = dict.fromkeys(symbols), dict.fromkeys(symbols)
        if pos >= lookback:
            for symbol in symbols:
                window = [closes[j][symbol] for j in range(pos-lookback, pos+1)]
                if any(not finite(p) or p <= 0 for p in window):
                    continue
                returns = [b/a-1 for a, b in zip(window, window[1:])]
                avg = sum(returns)/lookback
                m[symbol] = window[-1]/window[0]-1
                v[symbol] = sqrt(sum((r-avg)**2 for r in returns)/(lookback-1))
        momentum.append(m)
        volatility.append(v)
    return momentum, volatility


def make_panel(seed=37, days=80, stocks=40):
    if days < 10 or stocks < 40 or days*stocks > 1_000_000:
        raise ValueError("Use >=10 days, >=40 stocks, and at most one million stock-days")
    rng = Random(seed)
    symbols = [f"S{i:03d}" for i in range(stocks)]
    previous = {s: 30+rng.random()*70 for s in symbols}
    prices, closes = [], []
    for pos in range(days):
        common = rng.gauss(0, 0.008)
        vwap, close = {}, {}
        for j, symbol in enumerate(symbols):
            daily_return = common+rng.gauss(0, 0.012)+0.0006*sin(pos/9+j)
            vwap[symbol] = previous[symbol]*max(0.2, 1+daily_return)
            close[symbol] = vwap[symbol]*(1+rng.gauss(0, 0.003))
        prices.append(vwap)
        closes.append(close)
        previous = vwap
    momentum, volatility = features(closes)
    membership = {}
    for name, size in [('FULL', stocks), ('WIDE', stocks*3//4), ('MEDIUM', stocks//2), ('SMALL', stocks//4)]:
        rows = []
        for pos in range(days):
            rotation = (pos//20*7) % stocks
            members = {symbols[(rotation+j) % stocks] for j in range(size)}
            rows.append({s:s in members for s in symbols})
        membership[name] = rows
    return {"dates": trading_positions(days), "vwap": prices, "close": closes,
            "signal": momentum, "volatility": volatility, "membership": membership}
