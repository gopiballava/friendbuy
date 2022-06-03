import unittest

from memred import MemRed, NoTransactionException


class TestSuppliedCases(unittest.TestCase):
    def test_simple_one(self):
        mr = MemRed()
        mr.set('x', '10')
        self.assertEqual(mr.get('x'), '10')
        mr.unset('x')
        self.assertEqual(mr.get('x'), None)

    def test_simple_two(self):
        mr = MemRed()
        mr.set('a', '10')
        mr.set('b', '10')
        self.assertEqual(mr.num_equal_to('10'), 2)
        self.assertEqual(mr.num_equal_to('20'), 0)
        mr.set('b', '30')
        self.assertEqual(mr.num_equal_to('10'), 1)

    def test_transactions_one(self):
        mr = MemRed()

        mr.begin()
        mr.set('a', '10')
        self.assertEqual(mr.get('a'), '10')

        mr.begin()
        mr.set('a', '20')
        self.assertEqual(mr.get('a'), '20')
        mr.rollback()

        self.assertEqual(mr.get('a'), '10')
        mr.rollback()

        self.assertEqual(mr.get('a'), None)

    def test_transactions_two(self):
        mr = MemRed()

        mr.begin()
        mr.set('a', '30')

        mr.begin()
        mr.set('a', '40')

        mr.commit()

        self.assertEqual(mr.get('a'), '40')
        with self.assertRaises(NoTransactionException):
            mr.rollback()

    def test_transactions_three(self):
        mr = MemRed()
        mr.set('a', '50')

        mr.begin()
        self.assertEqual(mr.get('a'), '50')
        mr.set('a', '60')

        mr.begin()
        mr.unset('a')
        self.assertEqual(mr.get('a'), None)
        mr.rollback()

        self.assertEqual(mr.get('a'), '60')
        mr.commit()

        self.assertEqual(mr.get('a'), '60')

    def test_transactions_four(self):
        mr = MemRed()
        mr.set('a', '10')

        mr.begin()
        self.assertEqual(mr.num_equal_to('10'), 1)

        mr.begin()
        mr.unset('a')
        self.assertEqual(mr.num_equal_to('10'), 0)
        mr.rollback()

        self.assertEqual(mr.num_equal_to('10'), 1)
        mr.commit()

if __name__ == '__main__':
    unittest.main()
