import unittest

from mem_stackable import MemStackable

class MemStackableTests(unittest.TestCase):
    def test_single(self):
        ms = MemStackable(None)
        self.assertEqual(ms.get('a'), None)
        self.assertEqual(ms.num_equal_to('first'), 0)
        self.assertEqual(ms.num_equal_to('second'), 0)

        ms.set('a', 'first')
        self.assertEqual(ms.get('a'), 'first')
        self.assertEqual(ms.num_equal_to('first'), 1)
        self.assertEqual(ms.num_equal_to('second'), 0)

        ms.set('a', 'second')
        self.assertEqual(ms.get('a'), 'second')
        self.assertEqual(ms.num_equal_to('first'), 0)
        self.assertEqual(ms.num_equal_to('second'), 1)

        ms.unset('a')
        self.assertEqual(ms.get('a'), None)
        self.assertEqual(ms.num_equal_to('first'), 0)
        self.assertEqual(ms.num_equal_to('second'), 0)

    def test_simple_stacked(self):
        base = MemStackable(None)
        ms = MemStackable(base)

        self.assertEqual(ms.get('a'), None)
        self.assertEqual(ms.num_equal_to('first'), 0)
        self.assertEqual(ms.num_equal_to('second'), 0)

        ms.set('a', 'first')
        self.assertEqual(ms.get('a'), 'first')
        self.assertEqual(ms.num_equal_to('first'), 1)
        self.assertEqual(ms.num_equal_to('second'), 0)

        ms.set('a', 'second')
        self.assertEqual(ms.get('a'), 'second')
        self.assertEqual(ms.num_equal_to('first'), 0)
        self.assertEqual(ms.num_equal_to('second'), 1)

        ms.unset('a')
        self.assertEqual(ms.get('a'), None)
        self.assertEqual(ms.num_equal_to('first'), 0)
        self.assertEqual(ms.num_equal_to('second'), 0)

    def test_override_base(self):
        base = MemStackable(None)
        base.set('a', 'first')
        self.assertEqual(base.get('a'), 'first')
        self.assertEqual(base.num_equal_to('first'), 1)
        self.assertEqual(base.num_equal_to('second'), 0)

        ms = MemStackable(base)

        self.assertEqual(ms.get('a'), 'first')
        self.assertEqual(ms.num_equal_to('first'), 1)
        self.assertEqual(ms.num_equal_to('second'), 0)

        ms.set('a', 'second')
        self.assertEqual(ms.get('a'), 'second')
        self.assertEqual(ms.num_equal_to('first'), 0)
        self.assertEqual(ms.num_equal_to('second'), 1)

        ms.unset('a')

        self.assertEqual(ms.get('a'), None)
        self.assertEqual(ms.num_equal_to('first'), 0)
        self.assertEqual(ms.num_equal_to('second'), 0)

        # Verify the base is still the same
        self.assertEqual(base.get('a'), 'first')
        self.assertEqual(base.num_equal_to('first'), 1)
        self.assertEqual(base.num_equal_to('second'), 0)

    def test_application_override(self):
        base = MemStackable(None)
        base.set('a', 'first')
        self.assertEqual(base.get('a'), 'first')
        self.assertEqual(base.num_equal_to('first'), 1)
        self.assertEqual(base.num_equal_to('second'), 0)

        ms = MemStackable(base)
        ms.set('a', 'second')
        ms.commit_to_parent()
        self.assertEqual(base.get('a'), 'second')
        self.assertEqual(base.num_equal_to('first'), 0)
        self.assertEqual(base.num_equal_to('second'), 1)

    def test_application_unset(self):
        base = MemStackable(None)
        base.set('a', 'first')
        self.assertEqual(base.get('a'), 'first')
        self.assertEqual(base.num_equal_to('first'), 1)
        self.assertEqual(base.num_equal_to('second'), 0)

        ms = MemStackable(base)
        ms.unset('a')
        ms.commit_to_parent()
        self.assertEqual(base.get('a'), None)
        self.assertEqual(base.num_equal_to('first'), 0)
        self.assertEqual(base.num_equal_to('second'), 0)


if __name__ == '__main__':
    unittest.main()
