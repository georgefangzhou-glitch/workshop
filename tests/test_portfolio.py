import unittest
from workshop_lab.portfolio import InsufficientUniverse, group_returns


class PortfolioTests(unittest.TestCase):
    def setUp(self):
        self.scores = {f'S{i:03d}':float(i) for i in range(20)}
        self.returns = {s:value/100 for s,value in self.scores.items()}

    def test_hand_calculated_ten_groups(self):
        result = group_returns(self.scores,self.returns,0.02)
        self.assertEqual(set(result.counts.values()),{2})
        self.assertAlmostEqual(result.absolute['1'],0.005)
        self.assertAlmostEqual(result.absolute['10'],0.185)
        self.assertAlmostEqual(result.high_minus_low,0.18)

    def test_absolute_excess_and_HL_identities(self):
        result = group_returns(self.scores,self.returns,-0.01)
        self.assertAlmostEqual(result.absolute['10'],result.excess['10']-0.01)
        self.assertAlmostEqual(result.high_minus_low,result.excess['10']-result.excess['1'])

    def test_missing_selected_return_blocks_instead_of_dropping(self):
        self.returns['S019'] = None
        with self.assertRaisesRegex(ValueError,'Unknown selected return'):
            group_returns(self.scores,self.returns,0.)

    def test_unknown_unselected_return_does_not_change_selection(self):
        self.scores['S019'] = None
        self.returns['S019'] = None
        result = group_returns(self.scores,self.returns,0.)
        self.assertEqual(sum(result.counts.values()),19)
        self.assertTrue(all(n>0 for n in result.counts.values()))

    def test_not_enough_signals_is_explicit(self):
        with self.assertRaises(InsufficientUniverse):
            group_returns({'A':1.},{'A':0.1},0.)

    def test_ties_are_deterministic_independent_of_dict_order(self):
        tied = {s:1. for s in self.scores}
        a = group_returns(tied,self.returns,0.)
        b = group_returns(dict(reversed(list(tied.items()))),self.returns,0.)
        self.assertEqual(a,b)

    def test_unknown_benchmark_blocked(self):
        with self.assertRaises(ValueError):
            group_returns(self.scores,self.returns,None)

    def test_invalid_group_count_blocked(self):
        for value in (1,True,2.5):
            with self.subTest(value=value),self.assertRaises(ValueError):
                group_returns(self.scores,self.returns,0.,groups=value)
