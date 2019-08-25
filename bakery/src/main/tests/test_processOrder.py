import unittest
from bakery.src.main.python.processOrder import *


class TestProcessOrder(unittest.TestCase):
    """Basic test cases."""

    def test_findProduct(self):
        self.assertEqual(findProduct("CF"), True)

    def test_validQty(self):
        orderedQty=19
        packSizes=[2, 5, 8]
        result=['3:5', '2:2']
        self.assertListEqual(calculateMinPacks(orderedQty, packSizes), result)

    def test_inValidQty(self):
        orderedQty=1
        packSizes=[3, 5]
        result=[]
        self.assertListEqual(calculateMinPacks(orderedQty, packSizes), result)


if __name__ == '__main__':
    unittest.main()
