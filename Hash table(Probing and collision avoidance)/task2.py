from referential_array import build_array
import timeit


class HashTableLinearProbing:
  def __init__(self, size):
    '''
    
    :param size: the size of array 
    :return: no return
    :precondition: size should be integer
    :time complexity: best and worst case O(1) 
    
    '''
    self.table_size = size
    self.count = 0
    self.array = build_array(self.table_size)
  
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
    a = 101 
    h = 0
    for c in key:
      h = ( h * a + ord(c)) % self.table_size 
    return h
  
  
  def __getitem__(self, key):
    '''
    
    :param key: the key can be string
    :return: return the value stored in the position
    :precondition: hash method must be prepared, array should be defined
    :time complexity: best case is O(1) where position is first place
    worst case is O(N) where position  is last index 
    
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
    
  def __setitem__(self, key, value):
    
    '''
    
    :param key: the key that is going to be hashed
    :param value: the value that will be stored in hash table
    :return: no return
    :precondition: hash method must be prepared, array should be defined
    :time complexity: best case is O(1) where position is first place
    worst case is O(N) where position  is last index 
    
    '''
    position = self.hash(key)

    for _ in range(self.table_size):
      if self.array[position] is None:
        self.array[position] = (key, value)
        self.count += 1
        return
      elif self.array[position][0] == key:#set item
        self.array[position] = (key, value)
        return self.array[position][1]
      else:
        position = (position+1) % self.table_size
    raise KeyError("key not found")

  def __contains__(self, key):
    '''
    
    :param key: the key can be string
    :return: True if key item is in array, False if not
    :precondition: hash method must be prepared, array should be defined
    :time complexity: best case is O(1) where position is first place
    worst case is O(N) where position  is last index 
    
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
      
def time_hash():
  '''
    
    :param : 
    :return: the time taken by creating the hash table
    :precondition: class hash should be defined
    :time complexity: best case and worst case is O(N)
     where N is the number of lines of file
    
    
    '''
    
    
    fname = 'french.txt'
    size = int(202361)
    start = timeit.default_timer()
    f = open(fname, 'r')


    myhash = HashTableLinearProbing(size)

    for line in f:

        tmp = line.strip()
        myhash[tmp] = tmp
    
    taken = (timeit.default_timer() - start)
    return taken 

print(time_hash())




  
    
    
    
  
    
    
    
    
    
