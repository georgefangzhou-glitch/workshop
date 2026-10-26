import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from workshop_lab.__main__ import run_demo
from workshop_lab.synthetic import features, make_panel


class DemoTests(unittest.TestCase):
    def test_fixed_seed_is_reproducible(self):
        self.assertEqual(run_demo(days=20),run_demo(days=20))

    def test_all_four_pools_preserve_accounting_rows(self):
        summary,ledger = run_demo()
        self.assertEqual(summary['ledger_rows'],4*78)
        self.assertFalse(summary['performance_evidence'])
        for result in summary['pools'].values():
            self.assertEqual(result['accounting_rows'],78)
            self.assertEqual(result['valid_group_days'],73)
            self.assertEqual(result['retained_insufficient_days'],5)
        self.assertLess(summary['max_accounting_identity_error'],1e-12)
        self.assertEqual(len(ledger),312)

    def test_future_input_cannot_change_earlier_features(self):
        panel = make_panel(days=20)
        changed = copy.deepcopy(panel['close'])
        changed[15]['S000'] *= 10
        earlier = features(changed)
        self.assertEqual(earlier[0][:15],panel['signal'][:15])
        self.assertEqual(earlier[1][:15],panel['volatility'][:15])

    def test_unknown_feature_input_preserves_window_positions(self):
        closes = [{'A':10.+i} for i in range(12)]
        closes[3]['A'] = None
        momentum,_ = features(closes)
        self.assertIsNone(momentum[8]['A'])
        self.assertIsNotNone(momentum[9]['A'])

    def test_full_market_is_not_union_of_subpools(self):
        panel = make_panel(days=20)
        membership = panel['membership']
        subset_union = {s for pool in ('WIDE','MEDIUM','SMALL') for s,active in membership[pool][0].items() if active}
        self.assertEqual(len(subset_union),30)
        self.assertEqual(sum(membership['FULL'][0].values()),40)

    def test_members_rotate_without_modifying_signal(self):
        panel = make_panel(days=30)
        self.assertNotEqual(panel['membership']['SMALL'][19],panel['membership']['SMALL'][20])
        self.assertEqual(len(panel['signal'][20]),40)

    def test_cli_writes_strict_json_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            command=[sys.executable,'-m','workshop_lab','--days','12','--output',str(Path(temp)/'demo')]
            first=subprocess.run(command,capture_output=True,text=True,check=True)
            summary=json.loads(first.stdout)
            self.assertEqual(summary['ledger_rows'],40)
            saved=Path(temp)/'demo'/'summary.json'
            original=saved.read_bytes()
            second=subprocess.run(command,capture_output=True,text=True)
            self.assertNotEqual(second.returncode,0)
            self.assertEqual(saved.read_bytes(),original)
