import sys
from numpy import positive
import math

instances = []
instancesObj = []
attributes = []
remaining_attributes = []
testing_instancesObj = []
classes = []

#NODE CLASS
class Node:
       pass  

class Leaf(Node):
    def __init__(self, catagory=None, probability=None):
        self.catagory = catagory
        self.probability = probability
    
    
    def toString(self, indent):
        if(self.probability == 0):
            print(indent + "unknown")
        else:
            print(indent + self.catagory + " " + str(self.probability/100))

class Branch(Node):
    def __init__(self, attribute=None, Lvalue=None, Rvalue=None):
        self.attribute = attribute
        self.Lvalue = Lvalue
        self.Rvalue = Rvalue
        
    def toString(self,indent):
        print(indent + self.attribute + " = true" + " : ")
        self.Lvalue.toString(indent + "  ")
        print(indent + self.attribute + " =  False" + " : ")
        self.Rvalue.toString(indent + "  ")

        
           
class Instance:
    def __init__(self, classification=None, T_F_list=None):
        self.classification = classification
        self.T_F_list = T_F_list 
        
    def getByattribute(self, index):
       # print("index: ", index)
        return self.T_F_list[index]
         
    def getCurAttResult(self, index):
        return attributes[index]
         
def loadTrainingData():
    with open(sys.argv[1], 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                line = line.split(' ')
                if line[0] == 'Class':
                    for t in range(1, len(line)):
                        attributes.append(line[t])
                else:
                    classification = line[0]
                    if not classes.__contains__(classification):
                        classes.append(classification)
                    
                    T_F_list = []
                    for i in range(1, len(line)):
                        T_F_list.append(line[i])
                   
                    instancesObj.append(Instance(classification, T_F_list))

    
    

    
def loadTestingData():
  with open(sys.argv[2], 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                line = line.split(' ')
                if not line[0] == 'Class':
                    classification = line[0]
                    T_F_list = []
                    for i in range(1, len(line)):
                        T_F_list.append(line[i])
                    testing_instancesObj.append(Instance(classification, T_F_list))

    
 
        
def getTotalLive():
    totalA = 0
    for i in instancesObj:
        if str(i.classification) == str(classes[0]):
            totalA += 1
            
    return totalA

def getTotalDie():
    totalB = 0
    for i in instancesObj:
        if str(i.classification) == str(classes[1]):
            totalB += 1
    return totalB
    
def findBestAttribute(remaining_Instances):
   
    bestImpurity = math.inf 
    bestAttribute = None
    bestinstTrue = None
    bestinstFalse = None
    
    for i in range(len(remaining_attributes)):
        trueList = []
        falseList = []
        newDex = attributes.index(remaining_attributes[i])
        for j in remaining_Instances:
                
                if j.getByattribute(newDex) == "true":
                    trueList.append(j)
                else:
                    falseList.append(j)
        impurity = calcInPurity(trueList, falseList)
        if impurity < bestImpurity:
            
            bestImpurity = impurity
            bestAttribute = remaining_attributes[i]
            bestinstTrue = trueList
            bestinstFalse = falseList
           
    newList = remaining_attributes.copy()
    newList.remove(bestAttribute)
                

    left = BuildTree(bestinstTrue, newList)
    right = BuildTree(bestinstFalse, newList)
    N = Branch(bestAttribute, left, right)
    return N 
        

    

def calcInPurity(trueList, falseList):
    dt = len(trueList) / (len(trueList) + len(falseList))
    df = 1.0 - dt
    return dt * calcAttrRatio(trueList) + df * calcAttrRatio(falseList)
    
    
def calcAttrRatio(list):
    if not list: 
        return 0
    count = [0,0]
    for i in list:
        if(i.classification == classes[0]):
            count[0] += 1
        else:
            count[1] += 1
  
    return (count[0]/len(list)) * (count[1]/len(list))
 
def calcPure(remaining_Insatnces):
    countA = 0
    countB = 0
    for i in remaining_Insatnces:
        if i.classification == classes[0] :
            countA += 1
        else: 
            countB += 1
            
    if countA == len(remaining_Insatnces):
        return True
    elif countB == len(remaining_Insatnces):
        return True
    else:
        return False
        
    
def BuildTree(remaining_Instances, Attributes):
   
    if not remaining_Instances:
       
        prob = getTotalLive() / getTotalDie()
        
        return Leaf(catagory=classes[0] if prob >= 1 else classes[1], probability=prob)
    
    elif calcPure(remaining_Instances):
       
        prob = 100
        return Leaf(catagory=remaining_Instances[0].classification , probability=prob)
        
    elif not Attributes:
       
        prob = getTotalLive() / getTotalDie()
        return Leaf(catagory=classes[0] if prob >= 1 else classes[1], probability=prob)
    else:
        cur_Node =  findBestAttribute(remaining_Instances)
        
        return cur_Node

def computeCorrectnessProbability(DT, testing_instances):
    count = 0
    for i in testing_instances:
        cur = DT
        while isinstance(cur, Branch):
            if i.T_F_list[attributes.index(cur.attribute)] == "true":
                cur = cur.Lvalue
            else:
                cur = cur.Rvalue
        if cur.catagory == i.classification:
            count += 1
    return count/len(testing_instances)
  
def computeBaseLine():
    live = getTotalLive()
    die = getTotalDie()
    if live > die:
        return "baseLine: live"
    else: 
        return "baseLine: die"
    

def setPredictA(test_instancesObj):
    count = 0
    for i in testing_instancesObj:
      if classes[0] == i.classification:
            count += 1
    return count/len(testing_instancesObj)
    
def setPredictB(test_instancesObj):
    count = 0
    for i in testing_instancesObj:
      if classes[1] == i.classification:
            count += 1
    return count/len(testing_instancesObj)

if __name__ == '__main__':
    loadTrainingData()
    loadTestingData()
    
    for i in attributes:
        remaining_attributes.append(i)
        
    Finaltree = BuildTree(instancesObj, remaining_attributes)
    Finaltree.toString(" ")
    print("Corretness: ", computeCorrectnessProbability(Finaltree, testing_instancesObj) * 100, "%")
    print(setPredictA(testing_instancesObj)*100, "%", computeBaseLine())
    print(setPredictB(testing_instancesObj)*100, "%" , "baseLine: die")