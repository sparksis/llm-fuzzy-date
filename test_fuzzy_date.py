import unittest
import datetime
from fuzzy_date import FuzzyDate, parse_user_input, get_timeline

class TestFuzzyDateParsing(unittest.TestCase):

    def test_parses_absolute_date(self):
        fd = parse_user_input("2024-01-15")
        self.assertEqual(fd.canonical_date, "2024-01-15")
        self.assertEqual(fd.sort_start_date, datetime.date(2024, 1, 15))
        self.assertEqual(fd.sort_end_date, datetime.date(2024, 1, 15))
        self.assertEqual(fd.confidence_score, 1.0)

    def test_parses_year(self):
        fd = parse_user_input("1999")
        self.assertEqual(fd.canonical_date, "1999")
        self.assertEqual(fd.sort_start_date, datetime.date(1999, 1, 1))
        self.assertEqual(fd.sort_end_date, datetime.date(1999, 12, 31))

    def test_parses_decade(self):
        fd = parse_user_input("199X")
        self.assertEqual(fd.canonical_date, "199X")
        self.assertEqual(fd.sort_start_date, datetime.date(1990, 1, 1))
        self.assertEqual(fd.sort_end_date, datetime.date(1999, 12, 31))

    def test_parses_approximate_year(self):
        fd = parse_user_input("1995~")
        self.assertEqual(fd.canonical_date, "1995~")
        # Approximate dates are treated like regular dates for sorting
        self.assertEqual(fd.sort_start_date, datetime.date(1995, 1, 1))
        self.assertEqual(fd.sort_end_date, datetime.date(1995, 12, 31))

    def test_parses_range(self):
        fd = parse_user_input("1990/1992")
        self.assertEqual(fd.canonical_date, "1990/1992")
        self.assertEqual(fd.sort_start_date, datetime.date(1990, 1, 1))
        self.assertEqual(fd.sort_end_date, datetime.date(1992, 12, 31))

    def test_unparsable_date_raises_error(self):
        with self.assertRaises(ValueError):
            parse_user_input("not a date")

class TestFuzzyDateSorting(unittest.TestCase):

    def test_sorts_correctly(self):
        # These are out of order
        fd1 = FuzzyDate("2000")
        fd2 = FuzzyDate("1990/1995")
        fd3 = FuzzyDate("1990-06-15")
        fd4 = FuzzyDate("199X") # same start as fd2, but longer end
        fd5 = FuzzyDate("2000", confidence=0.8) # same dates as fd1, lower confidence

        timeline = [fd1, fd2, fd3, fd4, fd5]

        sorted_timeline = get_timeline(timeline)

        expected_order = [
            fd2, # 1990/1995 -> start 1990-01-01, end 1995-12-31
            fd4, # 199X (1990/1999) -> start 1990-01-01, end 1999-12-31
            fd3, # 1990-06-15 -> start 1990-06-15
            fd1, # 2000 (confidence 1.0) -> start 2000-01-01
            fd5, # 2000 (confidence 0.8) -> start 2000-01-01
        ]

        self.assertEqual([d.original_input for d in sorted_timeline],
                         [d.original_input for d in expected_order])

if __name__ == '__main__':
    unittest.main()
