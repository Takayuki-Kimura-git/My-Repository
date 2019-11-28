from referential_array import build_array
from node import Node
import timeit


class HashTableSeparateChaining:
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
      position = self.hash(key)
    
      if self.array[position] is None:
        raise KeyError("key not found")
      else:
        current = self.array[position]
        while current is not None:
          if current.item[0] == key:
            return current.item[1]
          current = current.next
        raise KeyError("key not found")

  def collision_num(self, key):
    
    '''
    this method is to calculate or add the number of collisions 
    :param key: the key that is going to be hashed
    :return: return the number of collisions
    :precondition: self.collision must be defined, linkedlist should be defined
    :time complexity: best case and worst case is O(1) since this simply add 1 to the number of collisions
     
    
    '''
    position = self.hash(key)
    current = self.array[position]
    if current is not None:
      if current.item[0] != key:
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

    self.collision_num(key)
    
    
        
    if self.array[position] is None:#if position is empty
      head = Node((key, value), None)
      self.array[position] = head
      self.count += 1
      return
    else:
      current = self.array[position] # collision happened,
##      if current.item[0] != key:
##        self.collision +=1
      while current is not None: #search last node 
        if current.item[0] == key:#same key, then update
          current.item = (key, value)
          return

        tail = current
        self.totalprobe += 1
        current = current.next

      tail.next = Node((key, value), None)#new item
      self.count += 1
      return

  def __contains__(self, key):
    '''
    
    :param key: the key can be string
    :return: True if key item is in array, False if not
    :precondition: hash method must be prepared, array should be defined
    :time complexity: best case is O(1) where it is the case that no colision happend and directly insert
    worst case is O(N) where N is length of array when item is not found 
    
    '''
    position = self.hash(key)
      
    if self.array[position] is None:#if position is empty
      return False
    else:
      current = self.array[position] # collision happened,
      while current is not None: #search last node 
        if current.item[0] == key:#same key, then update
          return True

      return False

    




if __name__ == '__main__':
    
    filenamelist = ['english_large.txt','english_small.txt','french.txt']
    valuesizelist = ['210000','209987','400000','399989','202361']
    basevaluelist = ['101','97','82','51','29']
##    filenamelist = ['english_small.txt']
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
                myhash = HashTableSeparateChaining(size,basevalue)
                fname = str(file)
                f = open(fname, 'r', encoding = 'utf-8')
                for line in f:
                    tmp = line.strip()
                    myhash[tmp]=tmp #myhash[key] = [value]
                taken = (timeit.default_timer() - start)
                
                print(taken, 'the time taken')
                print(myhash.averageprobe(),'average probe')
                print(myhash.number_load(),'load')
                print(myhash.collision, 'the number of colision')

##                mystring = str(base) + "," + str(taken) + "," +  str(myhash.averageprobe()) + "," + str(myhash.number_load()) + "," + str(myhash.collision)
##                print(mystring)
  



  
    
    
    
  
    
    
    
    
    
