import unittest

from task4 import HashTableQuadraticProbing
from task6 import findmaxnum
from task6 import ranking

class Test_task6(unittest.TestCase):
    def test_findmaxnum(self):
        myhash = HashTableQuadraticProbing(210000,101)
        myhash.__setitem__("temp",6)
        myhash.__setitem__("whatever",3)

        self.assertEqual(findmaxnum(myhash), 6)
        myhash.__setitem__("last",10)
        self.assertEqual(findmaxnum(myhash), 10)

    def test_ranking(self):
        myhash = HashTableQuadraticProbing(210000,101)
        myhash.__setitem__("temp",6000)
        myhash.__setitem__("whatever",3)
        myhash.__setitem__("last",1000)

        ranking(myhash, 6000)
        self.assertEqual(myhash.__getitem__('whatever'), 'rare')
       
        self.assertEqual(myhash.__getitem__('last'), 'common')
        
        
        
        
        





if __name__ == '__main__':
    unittest.main()
