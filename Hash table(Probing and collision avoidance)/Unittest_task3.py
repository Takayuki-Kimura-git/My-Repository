import unittest
from task3 import HashTableLinearProbing

class Test_task3(unittest.TestCase):
    def test__len__(self):
        myhash = HashTableLinearProbing(210000,101)
        myhash.__setitem__("FIT1008",'Intro to CS')
        self.assertEqual(myhash.__len__(), 1)
        myhash.__setitem__("FIT1049",'IT pro')
        self.assertEqual(myhash.__len__(), 2)

    def test_averageprobe(self):
        myhash = HashTableLinearProbing(210000,101)
        myhash.__setitem__("FIT1008",'Intro to CS')
        myhash.__setitem__("FIT1009",'Intro')
        average = myhash.totalprobe / myhash.count
        self.assertEqual(average,myhash.averageprobe())
        myhash.__setitem__("FIT1010",'Int')
        average = myhash.totalprobe / myhash.count
        self.assertEqual(average,myhash.averageprobe())
        
    def test_number_load(self):
        myhash = HashTableLinearProbing(210000,101)
        myhash.__setitem__("FIT1008",'Intro to CS')
        myhash.__setitem__("FIT1009",'Intro')
        load = myhash.count / myhash.table_size
        self.assertEqual(load,myhash.number_load())
        myhash.__setitem__("FIT1010",'Int')
        load = myhash.count / myhash.table_size
        self.assertEqual(load,myhash.number_load())
        
        
    
    def test_hash(self):
        myhash = HashTableLinearProbing(210000,101)
        tmp = myhash.hash('FIT')
        a =101
        h = 0
        key = 'FIT'
        for c in key:
            h = ( h * a + ord(c)) % myhash.table_size
        self.assertEqual(h,tmp)
        tmp = myhash.hash('INTRO')
        a =101
        h = 0
        key = 'INTRO'
        for c in key:
            h = ( h * a + ord(c)) % myhash.table_size
        self.assertEqual(h,tmp)

    def test__getitem__(self):
        myhash = HashTableLinearProbing(210000,101)
        myhash.__setitem__("FIT1008",'Intro to CS')
        tmp = myhash.__getitem__("FIT1008")
        self.assertEqual(tmp,"Intro to CS")
        myhash.__setitem__("FIT1049",'IT Pro')
        tmp = myhash.__getitem__("FIT1049")
        self.assertEqual(tmp,"IT Pro")

    def test__setitem__(self):
        myhash = HashTableLinearProbing(210000,101)
        self.assertEqual(myhash.__setitem__("FIT1008",'Intro to CS'),'Intro to CS')
        self.assertEqual(myhash.__setitem__("FIT1049",'IT Pro'),'IT Pro')

    def test__contains__(self):
        myhash = HashTableLinearProbing(210000,101)
        myhash.__setitem__("FIT1008",'Intro to CS')
        self.assertTrue(myhash.__contains__("FIT1008"))
        self.assertFalse(myhash.__contains__("FIT1049"))
        
        
        
        
        
        
        
        

    

if __name__ == '__main__':
    unittest.main()
