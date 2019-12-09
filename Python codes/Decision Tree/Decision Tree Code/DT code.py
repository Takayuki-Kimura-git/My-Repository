import math
import copy
import argparse as ap
############## Kimura Takayuki 28575393  #################
def read_datafile(fname, attribute_data_type = 'integer'):
   inf = open(fname,'r')
   lines = inf.readlines()
   inf.close()
   #--
   X = []
   Y = []
   for l in lines:
      ss=l.strip().split(',')
      temp = []
      for s in ss:
         if attribute_data_type == 'integer':
            temp.append(int(s))
         elif attribute_data_type == 'string':
            temp.append(s)
         else:
            print("Unknown data type");
            exit();
      X.append(temp[:-1])
      Y.append(int(temp[-1]))
   return X, Y

#===
def getbestGain(usedattr,dataset,label):
   number_yes = 0
   number_no  = 0
   for i in range(len(label)):
      if(label[i] ==0):
         number_no +=1
      else:
         number_yes+=1


   array = [number_yes/len(label), number_no/len(label)]
   ##print(array,"the array")
   BaseEntropy = 0
   for i in range(len(array)):
      BaseEntropy += -1*array[i] * math.log2(array[i])


   bestgain =0
   best_attribute =0
  
   for col in range(len(dataset[0])): ##calculate each attribute's gain, if the attribute is already chosen, exclude
      if(col not in usedattr):
         ##print(col,"col")
         totalfirstnum = 0 ##attribute is in 0 group
         yesnum_first =0   ##label is yes(1) and attribute is 0
         nonum_first = 0   ##label is no(0) and attribute is 0

         totalsecondnum =0 ## attribute is in 1 group
         yesnum_second = 0 ##label is yes(1) and attribute is 1
         nonum_second = 0  ##label is no(0) and attribute is 1

         for row in range(len(dataset)): ##count the number of 0 or 1 by each attribute
            if(dataset[row][col] ==0): ##attribute group is 0
               totalfirstnum +=1
               if(label[row] ==0):
                  nonum_first +=1
               else:
                  yesnum_first +=1
            else:                  ##attribute group is 1
               totalsecondnum+=1
               if(label[row]==0):
                  nonum_second +=1
               else:
                  yesnum_second +=1

         if(yesnum_first ==0 and nonum_first==0):##to avoid value error of log2(0)
            FirstEnt = 0
         elif(yesnum_first==0):
            FirstEnt =0 + (-1* nonum_first/totalfirstnum * math.log2(nonum_first/totalfirstnum))
         elif(nonum_first ==0):
            FirstEnt =(-1* yesnum_first/totalfirstnum * math.log2(yesnum_first/totalfirstnum)) + 0
         else:
            FirstEnt =(-1* yesnum_first/totalfirstnum * math.log2(yesnum_first/totalfirstnum)) + (-1* nonum_first/totalfirstnum * math.log2(nonum_first/totalfirstnum))

         if(yesnum_second ==0 and nonum_second ==0):
            SecondEnt = 0
         elif(yesnum_second ==0):
            SecondEnt =0 + (-1* nonum_second/totalsecondnum * math.log2(nonum_second/totalsecondnum))
         elif(nonum_second == 0):
            SecondEnt =(-1* yesnum_second/totalsecondnum * math.log2(yesnum_second/totalsecondnum)) 
         else:
            SecondEnt =(-1* yesnum_second/totalsecondnum * math.log2(yesnum_second/totalsecondnum)) + (-1* nonum_second/totalsecondnum * math.log2(nonum_second/totalsecondnum))

         Gain = BaseEntropy - (totalfirstnum/len(dataset) * FirstEnt) - (totalsecondnum/len(dataset) * SecondEnt)
         if(Gain >= bestgain):
            bestgain = Gain
            best_attribute = col

   return best_attribute
         
      




class Node:##linked binary tree
   def __init__(self,initlabel):
      self.attr = -1
      self.label = initlabel
      self.TrueNode = False  ##true node
      self.FalseNode  = False  ##false node

   def addAttr(self,initattr):
      self.attr = initattr

   def addTrueNode(self,initTrue):
      self.TrueNode = initTrue
      
   def addFalseNode(self,initFalse):
      self.FalseNode = initFalse
            

   

class DecisionTree:
   def __init__(self):
      #self.split_random = split_random # if True splits randomly, otherwise splits based on information gain 
      self.depth_limit = 0
      self.Tree = False

   def train(self, initdepth, X_train, Y_train ): ##examples, label, parent_data, current depth, used attributes
      self.depth_limit = initdepth
      self.Tree = self.train_aux(X_train, Y_train, Y_train,0,[])##pass the arguments to recursive decision tree function

      

   def Plurality(self,label):
      Truenum =0
      Falsenum = 0
      for i in range(len(label)):
         if (label[i]==0):
            Falsenum+=1
         else:
            Truenum+=1

      if(Truenum>=Falsenum):
         return True
      else:
         return False

   def Allsame(self,labels):
      label = labels[0]
      checker = True
      for i in range(len(labels)):
         if(labels[i] !=label):
            checker = False
      return checker

##   def printTree(self):
##      current=self.Tree
##      self.printTree_aux(current)
##      
##   def printTree_aux(self,current):
##      
##      TNode = current.TrueNode
##      FNode = current.FalseNode
##      ##print(current.attr,current.label,current.TrueNode,current.FalseNode,"-attr -label -Truenode-Falsenode")
##      
##      if(TNode !=False):
##         #print(current.attr,current.label,"Tnode is not false")
##         self.printTree_aux(TNode)
##      if(FNode !=False):
##         #print(current.attr,current.label,"Fnode is node false")
##         self.printTree_aux(FNode)
         
      
      
	## recursive training DT function
   def train_aux(self, X_train, Y_train, parent_dataset,cur_depth,usedAttr):##examples, label, parent_label, current depth, a list of chosen attributes
         
      if len(X_train) <1:                          ##if the current examples are empty, take the plurarity value of the parent data
         ##print(usedAttr,cur_depth,"usedAttr and depth  ---cur examples empty")
         newNode=Node(self.Plurality(parent_dataset))
         newNode.addAttr(copy.copy(usedAttr))     
         return newNode 
      
      elif (self.Allsame(Y_train)):                           ##if all examples are same classification, take any label out of the data since all are same
         ##print(usedAttr,cur_depth,"usedAttr and depth---all same value")
         if(Y_train[0] ==1):
            newNode=Node(True)
         else:
            newNode=Node(False)
         newNode.addAttr(copy.copy(usedAttr))     
         return newNode

      elif cur_depth >= self.depth_limit:            ##if depth exceeds, take the plurarity value of the current data
         ##print(usedAttr,cur_depth,"usedAttr and depth  ---depth limit")
         
         if len(X_train) <1:                       ##if the current data are empty, take the plurarity value of the parent data
            newNode=Node(self.Plurality(parent_dataset))
            newNode.addAttr(copy.copy(usedAttr))     
            return newNode 
         else:                                     ##if not, it is based on the current data
            newNode=Node(self.Plurality(Y_train))
            newNode.addAttr(copy.copy(usedAttr))     
            return newNode
         
      elif ((len(X_train[0])-len(usedAttr)) < 1):                    ## if no attribute is left to classify, return plurarity value 
         ##print(usedAttr,cur_depth,"usedAttr and depth---no attribute to use")
         newNode=Node(self.Plurality(Y_train))
         newNode.addAttr(copy.copy(usedAttr))     
         return newNode
      
      else:
         
         chosen_attr = getbestGain(usedAttr,X_train,Y_train)
         usedAttr.append(chosen_attr)
         newNode = Node(self.Plurality(Y_train)) ##add label based on the current data
         newNode.addAttr(copy.copy(usedAttr))            ##add attributes of the current node
         
         
         ##split examples 
         XFalse =[] #split Xtrain whose selected attribute is false 
         YFalse =[]  #split Ytrain whose selected attribute is false
         XTrue =[]  #split Xtrain whose selected attribute is True
         YTrue =[] #split Ytrain whose selected attribute is True
         for i in range(len(X_train)):
            if(X_train[i][chosen_attr] ==0):## the attribute is 0
               XFalse.append(X_train[i])
               YFalse.append(Y_train[i])
            else:                           ## the attribute is 1
               XTrue.append(X_train[i])
               YTrue.append(Y_train[i])
         
         trueNode_usedAttr = copy.copy(usedAttr)
         falseNode_usedAttr = copy.copy(usedAttr)
         newNode.addTrueNode(self.train_aux(XTrue,YTrue,Y_train, cur_depth+1,trueNode_usedAttr))
         newNode.addFalseNode(self.train_aux(XFalse,YFalse,Y_train, cur_depth+1,falseNode_usedAttr))

         return newNode
         
      
      
      
      


   def predict(self, X_train):
      current = self.Tree
      return self.predict_aux(current,X_train) ## call the recursive predict function

   def predict_aux(self,current,testdata):
      
      TNode = current.TrueNode
      FNode = current.FalseNode
      attr = current.attr
      if(attr ==[]):
         return current.label
      value=testdata[attr[-1]]
      if(value==0):
         if(FNode !=False):
            return self.predict_aux(FNode,testdata)
         else:
            return current.label
      else:
         if(TNode !=False):
            return self.predict_aux(TNode,testdata)
         else:
            return current.label
         
         
      

#===	   
def compute_accuracy(dt_classifier, X_test, Y_test):
   numRight = 0
   for i in range(len(Y_test)):
      x = X_test[i]
      y = Y_test[i]
      if y == dt_classifier.predict(x) :
         numRight += 1
   return (numRight*1.0)/len(Y_test)

def plotResults(X_train,Y_train,X_test,Y_test):
   import numpy as np
   import matplotlib.pyplot as plt
   ##0 to 30
   x_array = []
   y_array = []
   DT = DecisionTree()   
   for i in range(31):
      DT.train(i,X_train,Y_train)
      x_array.append(i)
      prediction = compute_accuracy(DT,X_test,Y_test)
      print(prediction,i,"  prediction and i")
      y_array.append(prediction)

   left = np.array(x_array)
   height = np.array(y_array)
   plt.plot(left, height)
   plt.show()
   return 0
   
#==============================================
#==============================================
if __name__ == '__main__':
   ##this parser code is given in assignment 1 part 1
   parser = ap.ArgumentParser()

   # specify what arguments will be coming from the terminal/commandline
   parser.add_argument("train_file", help="specifies the name of the train file", type=str)
   parser.add_argument("depth", help="specifies the depth limited", type=int)
   parser.add_argument("test_file", help="specifies test_file", type=str)
   parser.add_argument("output_file", help="specifies output_file", type=str)


    
   arguments = parser.parse_args()
   print("The train file is " + arguments.train_file)
   print("The depth limit is " + str(arguments.depth))
   print("The test file is " + arguments.test_file)
   print("The output file is " + arguments.output_file)

   
   ##X_train, Y_train = read_datafile('train.txt')
   X_train, Y_train = read_datafile(arguments.train_file)
   X_test, Y_test = read_datafile(arguments.test_file)
   # TODO: write your code


   DT = DecisionTree()
   DT.train(arguments.depth,X_train,Y_train)
   result = compute_accuracy(DT,X_test,Y_test)
   print(result)

   file = open(arguments.output_file,'a')
   file.write("input train_file: "+arguments.train_file+" input test_file: "+arguments.test_file+" depth is "+ str(arguments.depth)+ " the accuracy rate:" +str(result))
   file.write('\n')
   file.close()
   
##   X_train, Y_train = read_datafile("train.txt")
##   X_test, Y_test = read_datafile("train.txt")
##   ## this plotResults() is to plot the results as a line graph. uncomment it out if you want to see the graph
##   plotResults(X_train,Y_train,X_test,Y_test)

   

