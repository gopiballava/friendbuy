import unittest

from value_counter import ValueCounter

class ValueCounterTests(unittest.TestCase):
    def test_simple(self):
        vc = ValueCounter()
        self.assertEqual(vc.get_value_count('a'), 0)
        vc.increment_value('a')
        self.assertEqual(vc.get_value_count('a'), 1)
        vc.decrement_value('a')
        self.assertEqual(vc.get_value_count('a'), 0)

    def test_repeated(self):
        value_list = ['a', 'b', 'c']
        vc = ValueCounter()
        for value in value_list:
            self.assertEqual(vc.get_value_count(value), 0)

        for i in range(1200):
            for value in value_list:
                vc.increment_value(value)

        for value in value_list:
            self.assertEqual(vc.get_value_count(value), 1200)

        for i in range(1200):
            vc.decrement_value(value_list[0])

        for value in value_list[1:]:
            self.assertEqual(vc.get_value_count(value), 1200)
        self.assertEqual(vc.get_value_count(value_list[0]), 0)

        for i in range(1200):
            vc.decrement_value(value_list[0])

        self.assertEqual(vc.get_value_count(value_list[0]), -1200)


if __name__ == '__main__':
    unittest.main()
