import copy
from datetime import date, timedelta
import unittest
from workshop_lab.alignment import align_exit_dated


class AlignmentTests(unittest.TestCase):
    def setUp(self):
        self.dates = [date(2024, 1, 2)+timedelta(days=i) for i in range(4)]
        self.prices = [{'A':10.,'B':20.},{'A':20.,'B':20.},{'A':30.,'B':40.},{'A':60.,'B':20.}]
        self.scores = [{'A':100.+i,'B':200.+i} for i in range(4)]

    def test_explicit_entry_exit_clock(self):
        first, second = align_exit_dated(self.dates, self.scores, self.prices)
        self.assertEqual((first.signal_date, first.entry_date, first.exit_date), tuple(self.dates[:3]))
        self.assertEqual(first.scores['A'], 100.)
        self.assertEqual(first.returns['A'], 0.5)
        self.assertEqual(second.scores['A'], 101.)
        self.assertEqual(second.returns['A'], 1.)

    def test_membership_uses_signal_date_not_exit_date(self):
        members = [{'A':True,'B':False},{'A':False,'B':True},{'A':False,'B':True},{'A':False,'B':True}]
        first, second = align_exit_dated(self.dates, self.scores, self.prices, members)
        self.assertEqual(first.scores, {'A':100.,'B':None})
        self.assertEqual(second.scores, {'A':None,'B':201.})

    def test_unknown_prices_keep_calendar_positions(self):
        self.prices[1]['A'] = None
        aligned = align_exit_dated(self.dates, self.scores, self.prices)
        self.assertEqual(len(aligned), 2)
        self.assertIsNone(aligned[0].returns['A'])
        self.assertEqual(aligned[1].returns['A'], 1.)

    def test_unknown_signal_is_not_filled(self):
        self.scores[0]['A'] = None
        self.assertIsNone(align_exit_dated(self.dates, self.scores, self.prices)[0].scores['A'])

    def test_duplicate_and_reversed_dates_blocked(self):
        for dates in [self.dates[:2]+self.dates[1:3],list(reversed(self.dates))]:
            with self.subTest(dates=dates), self.assertRaises(ValueError):
                align_exit_dated(dates, self.scores, self.prices)

    def test_ragged_axes_blocked(self):
        del self.scores[2]['B']
        with self.assertRaises(ValueError):
            align_exit_dated(self.dates, self.scores, self.prices)

    def test_unknown_membership_blocked(self):
        members = [{'A':True,'B':True} for _ in self.dates]
        members[0]['A'] = None
        with self.assertRaises(ValueError):
            align_exit_dated(self.dates, self.scores, self.prices, members)

    def test_inputs_unchanged(self):
        saved = copy.deepcopy((self.dates,self.scores,self.prices))
        align_exit_dated(self.dates,self.scores,self.prices)
        self.assertEqual(saved,(self.dates,self.scores,self.prices))

    def test_zero_or_negative_entry_price_is_unknown(self):
        for price in (0.,-1.):
            self.prices[1]['A'] = price
            self.assertIsNone(align_exit_dated(self.dates,self.scores,self.prices)[0].returns['A'])
