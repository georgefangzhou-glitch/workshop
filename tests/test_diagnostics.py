import math
import unittest
from workshop_lab.diagnostics import average_ranks, correlation_summary, coverage, spearman


class DiagnosticsTests(unittest.TestCase):
    def test_average_ties(self):
        self.assertEqual(average_ranks([4.,1.,2.,2.]), [4.,1.,2.5,2.5])

    def test_identical_and_reverse_spearman(self):
        self.assertAlmostEqual(spearman([1,2,2,4],[1,2,2,4]),1.)
        self.assertAlmostEqual(spearman([1,2,2,4],[4,3,3,1]),-1.)

    def test_hand_calculated_tied_coefficient(self):
        self.assertAlmostEqual(spearman([1.,2.,3.],[1.,1.,2.]),math.sqrt(3)/2)

    def test_common_finite_pairs_only(self):
        self.assertAlmostEqual(spearman([1,2,3,None,999],[3,2,1,8,float('nan')]),-1.)
        self.assertIsNone(spearman([1,2,None],[3,4,5]))

    def test_constant_cross_section_is_undefined(self):
        self.assertIsNone(spearman([1,1,1],[1,2,3]))

    def test_mean_abs_is_not_abs_mean(self):
        summary = correlation_summary([0.8,-0.8,None])
        self.assertEqual(summary['valid_days'],2)
        self.assertEqual(summary['mean_signed'],0.)
        self.assertEqual(summary['mean_absolute'],0.8)

    def test_unknown_is_not_zero(self):
        self.assertEqual(coverage([{'A':0.,'B':None,'C':float('nan')}]),[{'valid':1,'missing':2}])
        self.assertIsNone(correlation_summary([None])['mean_signed'])

    def test_bad_rank_inputs_or_pair_axes_blocked(self):
        with self.assertRaises(ValueError):
            average_ranks([1,None])
        with self.assertRaises(ValueError):
            spearman([1,2,3],[1,2])
