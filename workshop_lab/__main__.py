"""Run the synthetic-only lab: python -m workshop_lab --output artifacts/demo."""
import argparse
import csv
import json
from pathlib import Path
from .alignment import align_exit_dated, finite
from .diagnostics import correlation_summary, spearman
from .portfolio import InsufficientUniverse, group_returns
from .synthetic import make_panel


def run_demo(seed=37, days=80, stocks=40):
    panel = make_panel(seed, days, stocks)
    all_days = align_exit_dated(panel['dates'], panel['signal'], panel['vwap'])
    benchmark = {day.exit_date:sum(day.returns.values())/stocks for day in all_days}
    feature_corr = []
    for a, b in zip(panel['signal'], panel['volatility']):
        symbols = sorted(a)
        feature_corr.append(spearman([a[s] for s in symbols], [b[s] for s in symbols]))
    ledger, per_pool = [], {}
    max_identity_error = 0.0
    for pool, members in panel['membership'].items():
        aligned = align_exit_dated(panel['dates'], panel['signal'], panel['vwap'], members)
        valid, invalid, daily_ic = 0, 0, []
        for day in aligned:
            row = {"pool":pool, "signal_date":str(day.signal_date), "entry_date":str(day.entry_date),
                   "exit_date":str(day.exit_date), "valid_signals":sum(finite(v) for v in day.scores.values()),
                   "status":"valid", "benchmark":benchmark[day.exit_date], "g1_absolute":None,
                   "g10_absolute":None, "g1_excess":None, "g10_excess":None, "high_minus_low":None, "rank_ic":None}
            try:
                result = group_returns(day.scores, day.returns, row['benchmark'])
            except InsufficientUniverse:
                invalid += 1
                row['status'] = 'insufficient_signals'
            else:
                valid += 1
                row.update(g1_absolute=result.absolute['1'],g10_absolute=result.absolute['10'],
                           g1_excess=result.excess['1'],g10_excess=result.excess['10'],high_minus_low=result.high_minus_low)
                symbols = sorted(day.scores)
                row['rank_ic'] = spearman([day.scores[s] for s in symbols], [day.returns[s] for s in symbols])
                daily_ic.append(row['rank_ic'])
                error = max(abs(row['g10_absolute']-row['g10_excess']-row['benchmark']),
                            abs(row['high_minus_low']-(row['g10_excess']-row['g1_excess'])))
                max_identity_error = max(max_identity_error, error)
            ledger.append(row)
        per_pool[pool] = {"accounting_rows":len(aligned), "valid_group_days":valid,
                          "retained_insufficient_days":invalid, "rank_ic":correlation_summary(daily_ic)}
    summary = {"data":"synthetic_generated_from_scratch", "real_securities_or_indices":False,
               "seed":seed, "calendar_days":days, "stocks":stocks, "ledger_rows":len(ledger),
               "benchmark":"synthetic full-universe equal-weight daily VWAP returns", "groups":10,
               "clock":"after-close signal t; VWAP entry t+1; exit-dated return t+2", "fees":"not modeled; gross toy arithmetic",
               "feature_spearman":correlation_summary(feature_corr), "max_accounting_identity_error":max_identity_error,
               "pools":per_pool, "performance_evidence":False}
    assert max_identity_error < 1e-12
    return summary, ledger


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed', type=int, default=37)
    parser.add_argument('--days', type=int, default=80)
    parser.add_argument('--stocks', type=int, default=40)
    parser.add_argument('--output', type=Path, default=Path('artifacts/demo'))
    args = parser.parse_args()
    paths = [args.output/'summary.json', args.output/'ledger.csv']
    if any(p.exists() for p in paths):
        parser.error('Output already exists; choose a fresh --output directory')
    try:
        summary, ledger = run_demo(args.seed, args.days, args.stocks)
    except ValueError as exc:
        parser.error(str(exc))
    args.output.mkdir(parents=True, exist_ok=True)
    with paths[0].open('x', encoding='utf8') as f:
        json.dump(summary, f, ensure_ascii=False, allow_nan=False, indent=2)
        f.write('\n')
    with paths[1].open('x', encoding='utf8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(ledger[0]))
        writer.writeheader()
        writer.writerows(ledger)
    print(json.dumps(summary, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
