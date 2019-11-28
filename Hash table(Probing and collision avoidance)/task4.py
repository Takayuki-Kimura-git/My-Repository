
from referential_array import build_array
import timeit


class HashTableQuadraticProbing:
  def __init__(self, size, basevalue):
    '''
    
    :param size: the size of array should be integer
    :param basevalue: base value should be integer 
    :return: no return
    :precondition: size and base value should be integer
    :time complexity: best and worst case O(1) 
    
    '''
    self.table_size = size
    self.count = 0
    self.array = build_array(self.table_size)
    self.basevalue = basevalue
    self.collision = 0
    self.totalprobe = 0
  def averageprobe(self):
    '''
    
    :param :
    :return: average probe needs to be numerical not string
    :precondition: self.totalprobe and self.count should be defined
    :time complexity: best and worst case O(1) 
    
    '''
    
    average = self.totalprobe / self.count
    return average
    
  def number_load(self):
    '''
    
    :param :
    :return: load needs to be numerical not string
    :precondition: self.table_size and self.count should be defined
    :time complexity: best and worst case O(1) 
    
    '''
    load = self.count / self.table_size
    return load

  
  def __len__(self):
    
    '''
    
    :param :
    :return: self.count, it returns the number of items in the table
    :precondition: self.count must be defined
    :time complexity: best and worst case O(1) 
    
    '''
    return self.count
  
  def hash(self, key):
    '''
    
    :param key: key can be string 
    :return: return hashed position
    :precondition: self.table_size needs to be defined
    :time complexity: best and worst case O(N) where N is the length of key 
    
    '''
    a = self.basevalue
    h = 0
    for c in key:
      h = ( h * a + ord(c)) % self.table_size 
    return h
  
  
  def __getitem__(self, key):
    '''
    
    :param key: the key can be string
    :return: return the value stored in the position
    :precondition: hash method must be prepared, array should be defined
    :time complexity: best case is O(1) where it is the case that no colision happend and directly insert
    worst case is O(N) where N is length of array when item is not found 
    
    '''
    position = self.hash(key)
    
    for _ in range(self.table_size):
      if self.array[position] is None:
        raise KeyError("key not found")
      elif self.array[position][0] == key:
        return self.array[position][1]
      else:
        position = (position+1) % self.table_size
    raise KeyError("key not found")


  def _resize_(self):
    '''
    this method is for resize when size exceeds 2/3, double the size
    
    :return: no return
    :precondition: hash method must be prepared, array should be defined
                   size should exceeds 2/3
                   
    :time complexity: best case and worst case is O(N) N is the number of item in array
    
    '''
    temp = self.array[:]
    
    double = (len(self.array) * 2) + 1
    
    self.array = build_array(double)
    self.count = 0
    
    self.table_size = len(self.array)
    
    for i in range(len(temp)):
      if temp[i] is not None:
        self[temp[i][0]] = temp[i][1]
    
  def collision_num(self, key):
    
    '''
    this method is to calculate or add the number of collisions 
    :param key: the key that is going to be hashed
    :return: return the number of collisions
    :precondition: self.collision must be defined, array should be defined
    :time complexity: best case and worst case is O(1) since this simply add 1 to the number of collisions
     
    
    '''
    
    position = self.hash(key)
    
    if self.array[position] is not None:
      if self.array[position][0] != key:
        self.collision +=1
    return self.collision  
  
  def __setitem__(self, key, value):
    '''
    
    :param key: the key that is going to be hashed
    :param value: the value that will be stored in hash table
    :return: no return
    :precondition: hash method must be prepared, array should be defined
    :time complexity: best case is O(1) where it is the case that no colision happend and directly insert
    worst case is O(N) where N is length of array when item is not found 
    
    '''
    position = self.hash(key)
    original = position

    S = 0



    if self.array[position] is not None:
      if self.array[position][0] != key:
        self.collision += 1
    
    for _ in range(self.table_size):
      if self.array[position] is None:
        
        self.array[position] = (key, value)
        self.count += 1
        load = self.number_load()
        if load > 2/3:
          self._resize_()
        return 
        
      elif self.array[position][0] == key:#set item
        self.array[position] = (key, value)
        return
##        return self.array[position][1] #if nessesary
      else:
        
        S += 1
        additional = S ** 2
        if additional > self.table_size:
          additional -= self.table_size
        position = (original + additional) % self.table_size
        self.totalprobe += 1
   
    raise KeyError("key not found")

  def __contains__(self, key):
    '''
    
    :param key: the key can be string
    :return: True if key item is in array, False if not
    :precondition: hash method must be prepared, array should be defined
    :time complexity: best case is O(1) where it is the case that no colision happend and directly insert
    worst case is O(N) where N is length of array when item is not found 
    
    '''
    position = self.hash(key)

      
    for _ in range(self.table_size):
      if self.array[position] is None:
        return False
      elif self.array[position][0] == key:
        return True
      else:
        position = (position+1) % self.table_size
    return False
      

    

if __name__ == '__main__':
    
    filenamelist = ['english_large.txt','english_small.txt','french.txt']
    valuesizelist = ['210000','209987','400000','399989','202361']
    basevaluelist = ['101','97','82','51','29']
##    filenamelist = ['english_large.txt']
##    valuesizelist = ['210000']
##    basevaluelist = ['97']
    for file in filenamelist:
        for valuesize in valuesizelist:
            for base in basevaluelist:
                print(file)
                print(valuesize,'table size')
                print(base, 'base value')
                basevalue = int(base)
                size = int(valuesize)

                start = timeit.default_timer()
                myhash = HashTableQuadraticProbing(size,basevalue)
                fname = str(file)
                f = open(fname, 'r', encoding = 'utf-8')
                for line in f:
                    tmp = line.strip()
                    myhash[tmp]=tmp #myhash[key] = [value]
                taken = (timeit.default_timer() - start)
                
                print(taken, 'the time taken')
                print(myhash.averageprobe(),'average probe')
                print(myhash.totalprobe, 'total probe')
                print(myhash.number_load(),'load')
                print(myhash.collision, 'the number of colision')
                print(myhash.table_size, 'table size')
                
##                mystring = str(base) + "," + str(taken) + "," +  str(myhash.averageprobe()) + "," + str(myhash.number_load()) + "," + str(myhash.collision)
##                print(mystring)
                





  
    
    
    
  
    
    
    
    
    
