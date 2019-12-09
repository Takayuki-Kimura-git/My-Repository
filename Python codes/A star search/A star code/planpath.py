import argparse as ap
import re
import platform


######## RUNNING THE CODE ####################################################
#   You can run this code from terminal by executing the following command
#   python planpath.py <INPUT/input#.txt> <OUTPUT/output#.txt> <flag> <algorithm>
#   for example: python planpath.py INPUT/input2.txt OUTPUT/output2.txt 0 A
#   NOTE: THIS IS JUST ONE EXAMPLE INPUT DATA
###############################################################################


################## YOUR CODE GOES HERE ########################################
import decimal
from decimal import Decimal
import math
import time 
class Vertex:
    def __init__(self, initrow,initcol):
        self.row = initrow
        self.col = initcol
        self.edges = []      ##pointer to its children
        self.opened = False
        self.closed = False
        self.finalized = False
        self.g = float('inf') ## value g
        self.h = 0            ## heuristic value h
        self.f = float('inf') ## value f
        ##self.position = 0
        self.Op = ""           ##it is just direction "R" or "D" and so on
        self.Operators = ""    ##this is operators such as "S-RD-R"
        self.No = ""           ##this is id
        self.order = 1  ##oreder of expantion
        self.parent = 0 ##pointer to its parent
        self.depth = 0
        
        


    def add_neighbor(self,From,To,weight,Operator):
        self.edges.append(Edge(From,To,weight,Operator))
        

        
     
class Edge:
    def __init__(self,initFrom, initTo, initweight,initOperator):
        self.From = initFrom
        self.To = initTo
        self.weight = initweight
        self.Operator = initOperator

class Graph:
    def __init__(self):
        '''
        Functionality of the function
        this is a constructor of Graph class
        vertices contains the all vertices of the graph
        service contains service points
        
        Time complexity:  O(1)
        Space complexity: O(E) where E is the total number of edges in the road network
        Error handle: there is no error handle
        Return: no return
        Parameter: no param
        Pre-requisite: no Pre-requisite

        '''
        self.vertices =[]
    def getIndex(self,row,col):
        '''
        Functionality of the function
        this method is to get the index of the vertex in the self.vertices
        
        Time complexity:  O(V) where V is the total number of vertices in the road network;
        Space complexity: O(1)
        Error handle: there is no error handle
        Return: it returns the index, if the vertex does not exist, it returns false
        Parameter: vertex to be checked
        Pre-requisite: vertices list should contain the vertex

        '''
        for i in range(len(self.vertices)):
            if(self.vertices[i].row == row and self.vertices[i].col == col):
                return i
        return False

    def add_vertex(self,row,col):
        '''
        Functionality of the function
        this method is to add new vertex into self.vertices

        Time complexity:  O(1)
        Space complexity: O(1)
        Error handle: there is no error handle
        Return: it returns true if it adds correctly
        Parameter: node, the vertex to be added
        Pre-requisite: no Pre-requisite

        '''
        self.vertices.append(Vertex(row,col))
        return True

    def invertices(self,row,col):
        '''
        Functionality of the function
        this method is to check if the vertex is in self.vertices or not

        
        Time complexity:  O(V) where V is the total number of vertices in the road network;
        Space complexity: O(1)
        Error handle: there is no error handle
        Return: true if there exist the vertex already, false if not
        Parameter: vertex, the vertex to be checked
        Pre-requisite: no Pre-requisite

        '''
        for i in range(len(self.vertices)):
            if(self.vertices[i].row == row and self.vertices[i].col == col):
                return True
        return False

    def buildGraph(self,size,map):
        for row in range(size):
            for col in range(size):
                if self.invertices(row,col) == False:
                    self.add_vertex(row,col)
                v = self.vertices[self.getIndex(row,col)]

                if map[row][col] !="X":

                    ##checks LEFT UP direction
                    if col > 0 and map[row][col-1] != "X":
                        if row > 0 and map[row-1][col] != "X":
                            if map[row-1][col-1] !="X":
                            
                                if self.invertices(row-1,col-1) == False:
                                    self.add_vertex(row-1,col-1)
                                u = self.vertices[self.getIndex(row-1,col-1)]
                                v.add_neighbor(v,u,1,"LU")

                    ##checks UP direction
                    if row > 0 and map[row-1][col]!= "X":
                        if self.invertices(row-1,col) == False:
                            self.add_vertex(row-1,col)
                        u = self.vertices[self.getIndex(row-1,col)]
                        v.add_neighbor(v,u,2,"U")

                    ##checks RIGHT UP direction
                    if row > 0 and map[row-1][col]!= "X":
                        if col < size-1 and map[row][col+1] != "X":
                            if map[row-1][col+1] !="X":
                            
                                if self.invertices(row-1,col+1) == False:
                                    self.add_vertex(row-1,col+1)
                                u = self.vertices[self.getIndex(row-1,col+1)]
                                v.add_neighbor(v,u,1,"RU")

                    ##checks LEFT direction
                    if col > 0 and map[row][col-1] != "X":
                        if self.invertices(row,col-1) == False:
                            self.add_vertex(row,col-1)
                        u = self.vertices[self.getIndex(row,col-1)]
                        v.add_neighbor(v,u,2,"L")
                    ##checks RIGHT direction
                    if col < size-1 and map[row][col+1]!= "X":
                        if self.invertices(row,col+1) == False:
                            self.add_vertex(row,col+1)
                        u = self.vertices[self.getIndex(row,col+1)]
                        v.add_neighbor(v,u,2,"R")
                    ##checks  LEFT DOWN direction
                    if col > 0 and map[row][col-1] != "X":
                        if row < size-1 and map[row+1][col] != "X":
                            if map[row+1][col-1] !="X":
                            
                                if self.invertices(row+1,col-1) == False:
                                    self.add_vertex(row+1,col-1)
                                u = self.vertices[self.getIndex(row+1,col-1)]
                                v.add_neighbor(v,u,1,"LD")
                    ##checks DOWN direction
                    if row < size-1 and map[row+1][col] != "X":
                        if self.invertices(row+1,col) == False:
                            self.add_vertex(row+1,col)
                        u = self.vertices[self.getIndex(row+1,col)]
                        v.add_neighbor(v,u,2,"D")
                    ##checks RIGHT DOWN direction
                    if col < size-1 and map[row][col+1] != "X":
                        if row < size-1 and map[row+1][col] != "X":
                            if map[row+1][col+1] !="X":                        
                                if self.invertices(row+1,col+1) == False:
                                    self.add_vertex(row+1,col+1)
                                u = self.vertices[self.getIndex(row+1,col+1)]
                                v.add_neighbor(v,u,1,"RD")


                            



##                
##def DLS(node,depth,map,OPEN,CLOSE,OpNo):
##    OpNo +=1
##    if(map[node.row][node.col] =="G" ):
##        #CLOSE.append(node)
##        node.finalized = True
##        node.opened = True
##        #OPEN.append([N+str(OpNo),edge.Operator,child,child.distance,0,child.distance])
##        return node
##
##    if(depth > 0):
##        for edge in node.edges: ##Edge(From,To,weight)
##            child = edge.To
##            parent = edge.From
##            if (child.opened == True):
##                continue
##            else:
##                
##                child.opened = True
##                child.distance = parent.distance + edge.weight
##                OPEN.append(["N"+str(OpNo),edge.Operator,child.distance,0,child.distance])
##                print("-------------------------------")
##                print("N"+str(OpNo),edge.Operator,child.distance,0,child.distance)
##                ##print("children: ",node.edges)
##                print("OPEN: ",OPEN)
##                print("CLOSED: ",CLOSE)
##                print("-------------------------------")
##                result = DLS(child,depth-1,map,OPEN,CLOSE,OpNo)
##                if result!= None:
##                    CLOSE.append(["N"+str(OpNo),edge.Operator,child.distance,0,child.distance])
##                    ##print("found")
##                    return result
##    print("null")
##    return None

def Eucledian(X1,Y1,X2,Y2):
    '''
    this function calculates the euclidean distance point A to point B
    if the points are in the same row or column, it does not divide it by 2
    '''
    
    if X1 ==X2 or Y1 == Y2:
        S = (X1,Y1)
        G = (X2, Y2)
    else:        
        S = (X1/2,Y1/2)
        G = (X2/2, Y2/2)
    distance = math.sqrt(sum([(m - n) ** 2 for m, n in zip(S, G)]))
    ##print("Euclidean distance from x to y: ",distance)
    
    return round(distance,2)



def swapElements(myList, i, j):
        temp = myList[i]
        myList[i] = myList[j]
        myList[j] = temp
def insertionSort(aList):##this is to sort the OPEN list
    n = len(aList)
    for k in range(1, n):    # insert aList[k] in aList[0:k] in sortedorder
        j = k 
        while aList[j - 1][6] <= aList[j][6] and j > 0:
            if aList[j - 1][6] == aList[j][6]:          ## tie breaking happens, it uses g value as second option for the comparison
                if aList[j - 1][4] < aList[j][4]:
                    swapElements(aList, j - 1, j)
                    j = j - 1
                else:
                    j = j -1
            else:
                swapElements(aList, j - 1, j)
                j = j - 1
        
           
        
        
def graphsearch(map, flag, procedure_name):
##-------------------------------DLS algorithm-------------------------------------------------------    
    if procedure_name == "D":
        starttime = time.time() ##start measuring the run time
        flagbound = flag
        flag = 1

        size = int(map.pop(0))
        
        bound = (size*size)//2 ## bound should not be so samll or so large as compared to the size of map
        print(bound,"bound")
        print(size,map)
        g = Graph()
        g.buildGraph(size,map)


        ##-------------------start DLS ----------------------------------
        for i in range(len(map)):
            for j in range(len(map)):
                if map[i][j] == "S":
                    StartRow = i
                    StartCol = j
        
        ind = g.getIndex(StartRow,StartCol)
        start = g.vertices[ind]
        start.g = 0
        start.f = 0
        OpNo = 0
        start.opened = True
        start.Op = "S"
        start.Operators = "S"
        start.No = "N"+str(OpNo)
        ##start.finalized = True
        OPEN = []
        
        OPEN.append([start,start,"N"+str(OpNo),"S",0,0,0])
        CLOSED= []


        while len(OPEN)>0:
            new = OPEN.pop()
            node = new[0]
            node.order = flag
            ##print(node.row,node.col,node.depth,"depth")

            if node.depth <= bound:
            
                if(map[node.row][node.col] =="G" ):##if the current node is goal 
                    new[3]= new[3] +"-"+"G"
                    CLOSED.append(new)
                    temp = []
                    if(flag<flagbound ):  
                        print("-----------------------------------------------")
                        print(new[2],new[3],node.order,new[4],new[5],new[6])
                        print("Children   ",end="")
                        for item in temp:
                            print(item[0] + " : " + item[1],end ="  ")
                        print()
                        print("OPEN   ",end="")
                        for i in range(len(OPEN)):
                            print(OPEN[i][2],OPEN[i][3],OPEN[i][4],OPEN[i][5],OPEN[i][6],end ="  ")
                        print()
                        print("CLOSED   ",end="")
                        for i in range(len(CLOSED)):
                            print(CLOSED[i][2],CLOSED[i][3],CLOSED[i][4],CLOSED[i][5],CLOSED[i][6],end ="  ")
                        print()
                        print("-----------------------------------------------")
                        
                    node.closed = True
                    break

                CLOSED.append(new)
                node.closed = True
                node.order = flag ##order of expantion 
                temp = []         ##this temp is for children list for diagnostic mode
                for edge in node.edges:
                    child = edge.To
                    parent = edge.From
                    
                    if child.opened != True:
                        
                        OpNo +=1
                        child.opened = True
                        child.g = parent.g + edge.weight
                        child.f = child.g
                        child.Operators = new[3]+"-"+edge.Operator
                        child.No = "N"+str(OpNo)##this is operators
                        child.parent = parent
                        child.depth = parent.depth + 1
                        temp.append([child.No,child.Operators])
                        OPEN.append([child,parent,child.No,child.Operators,child.g,0,child.f])

                        
                if(flag <flagbound):  
                    print("-----------------------------------------------")
                    print(new[2],new[3],node.order,new[4],new[5],new[6])
                    print("Children   ",end="")
                    for item in temp:
                        print(item[0] + " : " + item[1],end ="  ")
                    print()
                    print("OPEN   ",end="")
                    for i in range(len(OPEN)):
                        print(OPEN[i][2],OPEN[i][3],OPEN[i][4],OPEN[i][5],OPEN[i][6],end ="  ")
                    print()
                    print("CLOSED   ",end="")
                    for i in range(len(CLOSED)):
                        print(CLOSED[i][2],CLOSED[i][3],CLOSED[i][0].order,CLOSED[i][4],CLOSED[i][5],CLOSED[i][6],end ="  ")
                    print()
                    print("-----------------------------------------------")
                flag += 1
        
        
            

        
        
                    
        if map[CLOSED[-1][0].row][CLOSED[-1][0].col]=="G":
            solution = CLOSED[len(CLOSED)-1][3]
            solution += (" " + str(CLOSED[len(CLOSED)-1][4]))
            print(solution)

        else:
            solution = "NO-PATH"
            print(solution)
        endtime = time.time() - starttime
        print(endtime,"the run time")

        
        
            
                        
            
        

##----------------------------A* search algorithm -------------------------------------------------  
        
    elif procedure_name == "A":
        starttime = time.time() ## start measuring the run time
        flagbound = flag+1
        flag = 1
        
        size = int(map.pop(0))
        print(size,map)
        g = Graph()
        g.buildGraph(size,map)

        
        for i in range(len(map)):
            for j in range(len(map)):
                if map[i][j]=="G":
                    GoalX = i
                    GoalY = j
                elif map[i][j]=="S":
                    StartRow = i
                    StartCol = j
        
        ##------------Start  A* search-------------------------------------

        
        ind = g.getIndex(StartRow,StartCol)
        start = g.vertices[ind]
        start.g = 0
        OpNo = 0
        start.Operators = "S"
        start.No = "N"+str(OpNo)
        
        OPEN = []
        h = Eucledian(start.row,start.col,GoalX,GoalY)##calculate the heuristic value h(n)
        start.h = h
        start.f = h
        OPEN.append([start,start,"N"+str(OpNo),"S",0,h,h])
        CLOSED = []

        while len(OPEN) > 0 :

            
            new = OPEN.pop()
            
            

            new[0].finalized = True #vertex in graph.vertices is finalized
            new[0].order = flag
            if(map[new[0].row][new[0].col]=="G"):
                new[3]= new[3] +"-"+"G"
                
                CLOSED.append(new)
                if(flag <flagbound):  
                    print("-----------------------------------------------")
                    print(new[2],new[3],new[0].order,new[4],new[5],new[6])
                    print("Children   ",end="")
                    for item in temp:
                        print(item[0] + " : " + item[1],end ="  ")
                    print()
                    print("OPEN   ",end="")
                    for i in range(len(OPEN)):
                        print(OPEN[i][2],OPEN[i][3],OPEN[i][4],OPEN[i][5],OPEN[i][6],end ="  ")
                    print()
                    
                    print("CLOSED   ",end="")
                    
                    for i in range(len(CLOSED)):
                        print(CLOSED[i][2],CLOSED[i][3],CLOSED[i][0].order,CLOSED[i][4],CLOSED[i][5],CLOSED[i][6],end ="  ")
                    print()
                    print("-----------------------------------------------")
                    
                
                break
            
            CLOSED.append(new)
            temp = []##this is for children list in diagnostic mode
            
            for edge in new[0].edges:
                u = edge.From
                v = edge.To
                w = edge.weight

                if v.finalized == True:
                    pass
                else:
                    if v.opened == False:
                        OpNo+=1
                        g = Decimal(str(u.g)) + Decimal(str(w))

                        
                        v.g = g
                        
                        h = Decimal(str(Eucledian(v.row,v.col,GoalX,GoalY)))
                        v.h = h
                        v.f = g+h
                        v.parent = u
                        v.Operators = new[3]+"-"+edge.Operator
                        v.No = "N"+str(OpNo)
                        temp.append([v.No,v.Operators])

                        OPEN.append([v,u,v.No,v.Operators,v.g,v.h,v.f])

                        insertionSort(OPEN)##sort the open list in descending order

                        v.opened = True
                    else:
                        g = Decimal(str(u.g)) + Decimal(str(w))
                        h = Decimal(str(Eucledian(v.row,v.col,GoalX,GoalY)))
                        f = g+h
                        if v.f == f: ## tie breaking rule happen using g values as second option
                            if v.g > g: 
                                for m in range(len(OPEN)):
                                    if OPEN[m][1].row==v.row and OPEN[m][1].col == v.col:
                                        v.Operators = new[3]+"-"+edge.Operator
                                        OPEN[m][0] = u
                                        OPEN[m][3] = v.Operators
                                        OPEN[m][4] = g
                                        OPEN[m][5] = h
                                        OPEN[m][6] = f
                                    
                                v.g = g
                                v.h = h
                                v.f = f
                                v.parent = u
                                insertionSort(OPEN)
                        if v.f > f:
                            
                            for m in range(len(OPEN)):
                                if OPEN[m][1].row==v.row and OPEN[m][1].col == v.col:
                                    v.Operators = new[3]+"-"+edge.Operator
                                    OPEN[m][0] = u
                                    OPEN[m][3] = v.Operators
                                    OPEN[m][4] = g
                                    OPEN[m][5] = h
                                    OPEN[m][6] = f
                                    
                            v.g = g
                            v.h = h
                            v.f = f
                            v.parent = u
                            insertionSort(OPEN)
                            
                            

            if(flag <flagbound):  
                print("-----------------------------------------------")
                print(new[2],new[3],flag,new[4],new[5],new[6])
                print("Children   ",end="")
                for item in temp:
                    print(item[0] + " : " + item[1],end ="  ")
                print()
                print("OPEN   ",end="")
                for i in range(len(OPEN)):
                    print(OPEN[i][2],OPEN[i][3],OPEN[i][4],OPEN[i][5],OPEN[i][6],end ="  ")
                print()
                print("CLOSED   ",end="")
                for i in range(len(CLOSED)):
                    print(CLOSED[i][2],CLOSED[i][3],CLOSED[i][0].order,CLOSED[i][4],CLOSED[i][5],CLOSED[i][6],end ="  ")
                print()
                print("-----------------------------------------------")
            flag +=1

        if map[CLOSED[-1][0].row][CLOSED[-1][0].col]=="G":##if path has goal
            
            solution = CLOSED[len(CLOSED)-1][3]
            solution += (" " + str(CLOSED[len(CLOSED)-1][4]))##if there is no path
            print(solution)
        else:
            solution = "NO-PATH"
            print(solution)
        endtime = time.time() - starttime
        print(endtime,"the run time")

        

        
        
    else:
        print("invalid procedure name")
    
    return solution

def read_from_file(file_name):
    # You can change the file reading function to suit the way
    # you want to parse the file
    file_handle = open(file_name,'r')
    map = file_handle.read().splitlines()
    for i in range(1,len(map)):
        map[i] = list(map[i])
    return map
############# my code ends here ###############################

###############################################################################
########### DO NOT CHANGE ANYTHING BELOW ######################################
###############################################################################

def write_to_file(file_name, solution):
    file_handle = open(file_name, 'w')
    file_handle.write(solution)

def main():
    # create a parser object
    parser = ap.ArgumentParser()

    # specify what arguments will be coming from the terminal/commandline
    parser.add_argument("input_file_name", help="specifies the name of the input file", type=str)
    parser.add_argument("output_file_name", help="specifies the name of the output file", type=str)
    parser.add_argument("flag", help="specifies the number of steps that should be printed", type=int)
    parser.add_argument("procedure_name", help="specifies the type of algorithm to be applied, can be D, A", type=str)


    # get all the arguments
    arguments = parser.parse_args()

##############################################################################
# these print statements are here to check if the arguments are correct.
#    print("The input_file_name is " + arguments.input_file_name)
#    print("The output_file_name is " + arguments.output_file_name)
#    print("The flag is " + str(arguments.flag))
#    print("The procedure_name is " + arguments.procedure_name)
##############################################################################

    # Extract the required arguments

    operating_system = platform.system()

    if operating_system == "Windows":
        input_file_name = arguments.input_file_name
        input_tokens = input_file_name.split("\\")
        if not re.match(r"(INPUT\\input)(\d)(.txt)", input_file_name):
            print("Error: input path should be of the format INPUT\input#.txt")
            return -1

        output_file_name = arguments.output_file_name
        output_tokens = output_file_name.split("\\")
        if not re.match(r"(OUTPUT\\output)(\d)(.txt)", output_file_name):
            print("Error: output path should be of the format OUTPUT\output#.txt")
            return -1
    else:
        input_file_name = arguments.input_file_name
        input_tokens = input_file_name.split("/")
        if not re.match(r"(INPUT/input)(\d)(.txt)", input_file_name):
            print("Error: input path should be of the format INPUT/input#.txt")
            return -1

        output_file_name = arguments.output_file_name
        output_tokens = output_file_name.split("/")
        if not re.match(r"(OUTPUT/output)(\d)(.txt)", output_file_name):
            print("Error: output path should be of the format OUTPUT/output#.txt")
            return -1

    flag = arguments.flag
    procedure_name = arguments.procedure_name


    try:
        map = read_from_file(input_file_name) # get the map
    except FileNotFoundError:
        print("input file is not present")
        return -1
    # print(map)
    solution_string = "" # contains solution
    write_flag = 0 # to control access to output file

    # take a decision based upon the procedure name
    if procedure_name == "D" or procedure_name == "A":
        solution_string = graphsearch(map, flag, procedure_name)
        write_flag = 1
    else:
        print("invalid procedure name")

    # call function write to file only in case we have a solution
    if write_flag == 1:
        write_to_file(output_file_name, solution_string)

if __name__ == "__main__":
    main()
