
from task4 import HashTableQuadraticProbing
import timeit

def findmaxnum(myhash):
  
  '''
  this function is to find most frequent word's occurrence
  
  :param myhash: myhash is hashtable of QuadraticProbing 
  :return: return the most frequent word's occurrence 
  :precondition: myhash should be created and item should be set before this 
  :time complexity: best and worst case O(N), N is the length of the table
    
  '''  
  maxnum = 0
  for i in range(myhash.table_size):
    if myhash.array[i] is not None:
      if maxnum < myhash.array[i][1]:
        maxnum = myhash.array[i][1]

  return maxnum
      

def ranking(myhash, maxnum):
  '''
  this function is calculate the occurrence for each word,
  and replace the number of the frequency to the type such as common, uncommon and rare.
  
  :param myhash: myhash is hashtable of QuadraticProbing
  :param maxnum: the number of how many times most frequent word appears 
  :return: return the hashtable
  :precondition: myhash should be created and item should be set before this , maxnum should be calculated
  :time complexity: best and worst case O(N), N is the length of the table
    
  '''  
  assert type(maxnum) == int, 'max number is not integer'
  for i in range(myhash.table_size):

    if myhash.array[i] is not None:
      temp = myhash.array[i][0]
      if myhash.array[i][1] > maxnum/100:
        myhash[temp] = 'common'
        
      elif myhash.array[i][1] > maxnum / 1000:
        myhash[temp] = 'uncommon'
      else:
        myhash[temp] = 'rare'
  return myhash
  



if __name__ == '__main__':
    filenamelist = []
    filenamelist.append(str(input('what is your file name: ')))
    
    valuesizelist = ['400000']
    basevaluelist = ['97']
    for file in filenamelist:
        for valuesize in valuesizelist:
            for base in basevaluelist:
                print(file)
                assert int(valuesize) > 0, 'table size should be more than 0'
                print(valuesize,'table size')
                assert int(base) > 0, 'base value should not be 0'
                print(base, 'base value')
                basevalue = int(base)
                size = int(valuesize)


                #read file
                start = timeit.default_timer()
                myhash = HashTableQuadraticProbing(size,basevalue)
                fname = str(file)
                f = open(fname, 'r', encoding = 'utf-8')

                punctuation = "!@#$%^&*()_+=-{}[]:;'<>,./?\|~`"
                
                for line in f:
                  strings = line.strip()
                  for p in punctuation:
                    strings = strings.replace(p,'')
                
                  for word in strings.split():
                    word = word.lower()
                    if word in myhash:
                      count = myhash[word] + 1
                      myhash[word] = count
                    else:
                      myhash[word] = 1

                taken = (timeit.default_timer() - start)

                
                print(taken, 'the time taken')
                print(myhash.averageprobe(),'average probe')
                print(myhash.totalprobe, 'total probe')
                print(myhash.number_load(),'load')
                print(myhash.collision, 'the number of colision')
                print(myhash.table_size, 'table size')



                


                #finf max frequency
                max_num = findmaxnum(myhash)
                print(max_num, 'max')
##                 decide which is common, uncommon, rare
                ranking(myhash, max_num)
##                print(myhash.array[:10])

                quit = 0
                while quit == 0:
                  target = str(input('what word do you want to search ?: '))
                  assert type(target) == str, 'target is not string'
                  if target in myhash:
                    print(myhash.__getitem__(target))
                    quit = 1
                  else:
                    print('the word is not in the list. Try other word')
                  
                
                
##                mystring = str(base) + "," + str(taken) + "," +  str(myhash.averageprobe()) + "," + str(myhash.number_load()) + "," + str(myhash.colision)
##                print(mystring)
                





  
    
    
    
  
    
    
    
    
    
