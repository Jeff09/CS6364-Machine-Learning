# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import csv
from treeNode import node
import copy
import random
from collections import deque
import sys
class ID3:
    def __init__(self, data, fixed_classfier):
        self.data = data
        #self.classfier = classfier
        self.fixed_classfier = fixed_classfier
        
    def getMostCommonValue(self, subdata):
        classTag = [row[-1] for row in subdata]
        #count the frequence of values in classTag
        count = {}
        for tag in classTag:
            if tag not in count.keys():
                count[tag] = 0
            count[tag] += 1
            
        comValuefreq = -1
        comValue = -1
        for key in count.keys():
            if count[key]>comValuefreq:
                comValuefreq = count[key]
                comValue = key
        return comValue
    
    def VarianceImprity(self, subdata):
        classTag = [row[-1] for row in subdata]
        #count the frequence of values in classTag
        count = {}
        for tag in classTag:
            if tag not in count.keys():
                count[tag] = 0
            count[tag] += 1     
    
        # Now calculate the entropy
        vi=1.0
        for r in count.keys():
            p=float(count[r])/len(classTag)
            if p == 0:
                break
            vi=vi*p
        return vi
    
    def entropy(self, subdata):
        classTag = [row[-1] for row in subdata]
        #count the frequence of values in classTag
        count = {}
        for tag in classTag:
            if tag not in count.keys():
                count[tag] = 0
            count[tag] += 1     
        
        from math import log
        log2=lambda x:log(x)/log(2) 
    
        # Now calculate the entropy
        ent=0.0
        for r in count.keys():
            p=float(count[r])/len(classTag)
            if p == 0:
                break
            ent=ent-p*log2(p)
        return ent
    
    def divideSet(self, subdata, attr):
        i = 0
        for each in self.fixed_classfier:
            if each == attr:
                break
            i+=1
            
        split_function=lambda row:row[i]==1
        # Divide the rows into two sets and return them
        set1=[]
        set2=[]
        for row in subdata:
            if split_function(row):
                set1.append(row)
            else:
                set2.append(row)
    #set1=[row for row in data if split_function(row)]
    #set2=[row for row in data if not split_function(row)]
        return (set1, set2)
    
    def buildtree(self, subdata, dynmaic_classfier):
        # Create a root node for the tree
        root = node()
        
        #calculate the entropy
        classTag = [row[-1] for row in subdata]
        # If all Examples are positive, Return the single-node tree Root, with label = +
        # If all Examples are negative, Return the single-node tree Root, with label = -
        if classTag.count(classTag[0]) == len(classTag):
            root.label = classTag[0]  
            root.leaf = 1
            return root
        root.label = self.getMostCommonValue(subdata)             
        # If Attributes is empty, Return the single-node tree Root, with label = most common value 
        # of Target_Attribute in Examples
        if len(dynmaic_classfier) == 0:
            #root.label = self.getMostCommonValue(subdata)
            root.leaf = 1 
            return root
            
        cur_entropy = self.entropy(subdata) 
        
        best_gain = 0.0
        best_attr = None
        best_set = None
        
        for attr in dynmaic_classfier:
            (posSet, negSet) = self.divideSet(subdata, attr)
            
            #information gain
            p = float(len(posSet))/len(subdata)#p is the size of a child set relative to its parent
            gain = cur_entropy - p*self.entropy(posSet) - (1-p)*self.entropy(negSet)
        
            if gain>best_gain:
                best_gain = gain
                best_attr = attr
                best_set = (negSet, posSet)
        
        if best_gain>0:
            root.attr = best_attr
            dynmaic_classfier.remove(best_attr)
        #print classfier
        #print len(classfier)
            sub_classfier1 = copy.deepcopy(dynmaic_classfier)
            sub_classfier2 = copy.deepcopy(dynmaic_classfier)
            root.left = self.buildtree(best_set[0], sub_classfier1)
        #sub_classfier = classfier[:]
            root.right = self.buildtree(best_set[1], sub_classfier2)
        
        return root
    
    def buildtree2(self, subdata, dynmaic_classfier):
        # Create a root node for the tree
        root = node()
        
        #calculate the entropy
        classTag = [row[-1] for row in subdata]
        # If all Examples are positive, Return the single-node tree Root, with label = +
        # If all Examples are negative, Return the single-node tree Root, with label = -
        if classTag.count(classTag[0]) == len(classTag):
            root.label = classTag[0]  
            root.leaf = 1
            return root
        root.label = self.getMostCommonValue(subdata)             
        # If Attributes is empty, Return the single-node tree Root, with label = most common value 
        # of Target_Attribute in Examples
        if len(dynmaic_classfier) == 0:
            #root.label = self.getMostCommonValue(subdata)
            root.leaf = 1 
            return root
            
        cur_entropy = self.VarianceImprity(subdata) 
        
        
        best_gain = 0.0
        best_attr = None
        best_set = None
        
        for attr in dynmaic_classfier:
            (posSet, negSet) = self.divideSet(subdata, attr)
            
            #information gain
            p = float(len(posSet))/len(subdata)#p is the size of a child set relative to its parent
            gain = cur_entropy - p*self.VarianceImprity(posSet) - (1-p)*self.VarianceImprity(negSet)
        
            if gain>best_gain:
                best_gain = gain
                best_attr = attr
                best_set = (negSet, posSet)
        
        if best_gain>0:
            root.attr = best_attr
            dynmaic_classfier.remove(best_attr)
        #print classfier
        #print len(classfier)
            sub_classfier1 = copy.deepcopy(dynmaic_classfier)
            sub_classfier2 = copy.deepcopy(dynmaic_classfier)
            root.left = self.buildtree(best_set[0], sub_classfier1)
        #sub_classfier = classfier[:]
            root.right = self.buildtree(best_set[1], sub_classfier2)
        
        return root
    
    def printTree(self, root, level):
        string = ''
        
        if root == None:
            return ''
        if root.leaf == 1:
            string += str(root.label) + '\n'
            return string
        
        levelBars = ''
        for i in range(0, level):
            levelBars += '|'
            
        string += levelBars
        
        if root.left!=None and root.left.left == None and root.left.right == None:
            string +=  str(root.attr) + "= 0 :"
        else:
            string +=  str(root.attr) + "= 0 :\n"
            
        string += self.printTree(root.left, level+1)
        
        string += levelBars
        if root.left!=None and root.right.left == None and root.right.right == None:
            string += str(root.attr) + "= 1 :"
        else:
            string += str(root.attr) + "= 1 :\n"
        string += self.printTree(root.right, level + 1)
        
        return string
   
    def getPredictedValue(self, row, root):
        if root.right == None and root.left == None:
       
            return root.label

        i=0
        for attr in self.fixed_classfier:
            
            if str(attr) == str(root.attr):
                break;
            i+=1
    
        if row[i]== 0:
            return self.getPredictedValue(row, root.left)
    # If an attribute value is 1, search in the right subtree        
        else:
            return self.getPredictedValue(row, root.right)

    def calculateAccuracy(self, data, root):
    #calculate the prediction accuracy of a given decision tree on the data set    
    # If the decision tree or the data set is empty, return accuracy as 0
        if root == None or len(data) == 0:
            return 0
    # Count the total number of correct predictions made by the decision tree
        count = 0
        target = [row[-1] for row in data]
        i=0
        for row in data:
        #print target[i]
        #print type(target[i])
            if int(self.getPredictedValue(row, root)) == int(target[i]):
                #print self.getPredictedValue(row, root)
                count +=1
        #print(getPredictedValue(row, root), target[i])
            i+=1
        accuracy = float(count)/len(target)
        #print(count)
        return accuracy  
        
    def post_pruning(self,data,root,l,k):
        bestroot=copy.deepcopy(root)
        for i in range(1,l):
            curroot=copy.deepcopy(root)
            m=random.randint(1,k)
            for j in range(1,m):
                #n=self.non_leaf_number(curroot)
                ordered_node=self.inorder(curroot)
                n = len(ordered_node)-1
                if n<=0:
                    return bestroot
                p=random.randint(1,n)
                
                nodep=ordered_node[p]
                nodep.leaf=1
                nodep.left=None
                nodep.right=None
            oldAccurancy=self.calculateAccuracy(data,bestroot)
            newAccurancy=self.calculateAccuracy(data,curroot)
            #print oldAccurancy, newAccurancy
            if newAccurancy>oldAccurancy:
                bestroot=curroot
        return bestroot
    def non_leaf_number(self,root):
        if root.right==None and root.left==None:
            return 0
        else:
            return(self.non_leaf_number(root.left)+self.non_leaf_number(root.right)+1)

    def inorder(self,root):
        
        arr = []
        
        if root == None or root.leaf == 1:
            return root
        
        queue = deque([root])
        while len(queue)>0:
            curr=queue.popleft()
            #arr.append(curr.attr)u
            arr.append(curr)
            #print curr.left.leaf, curr.right.leaf
            if curr.left!=None and curr.left.leaf==-1:
                queue.append(curr.left)
            if curr.right!=None and curr.right.leaf==-1:
                queue.append(curr.right)
        return arr
        
if __name__ == "__main__":
    
    L = int(sys.argv[1])
    K = int(sys.argv[2])
    training_file_path = sys.argv[3]
    validation_file_path = sys.argv[4]
    test_file_path = sys.argv[5]
    willPrint =True if sys.argv[6]=='yes' else False
    
    with open(training_file_path) as f:
        reader = csv.reader(f)
        data = list(reader)
    classfier = data[0][:-1]
    #clas_fixed = copy.deepcopy(classfier)
    data = data[1:]  
    dataset = []
    for row in data:
        dataset.append([int(i) for i in row])
    #data = [int(row) for row in data]
    fixed_classfier = copy.deepcopy(classfier)
    id3 = ID3(dataset, fixed_classfier)
    #print id3.fixed_classfier
    dynmaic_classfier = copy.deepcopy(classfier)
    root = id3.buildtree(dataset, dynmaic_classfier)
    
    #tree=buildtree(data, classfier, clas_fixed)
    root2=id3.buildtree2(dataset,dynmaic_classfier)
    
    with open(validation_file_path) as f:
        reader = csv.reader(f)
        data = list(reader)
    classfier = data[0][:-1]
    #clas_fixed = copy.deepcopy(classfier)
    data = data[1:]  
    dataset = []
    for row in data:
        dataset.append([int(i) for i in row])
    
    with open(test_file_path) as f:
        test_reader = csv.reader(f)
        test_data = list(test_reader)
    test_classfier = test_data[0][:-1]
    #clas_fixed = copy.deepcopy(classfier)
    test_data = test_data[1:]  
    test_dataset = []
    for row in test_data:
        test_dataset.append([int(i) for i in row])
    
    print 'The accurancy of info_gain before post_pruning is: ',id3.calculateAccuracy(test_dataset, root)
    print 'The accurancy of vi before post_pruning is: ',id3.calculateAccuracy(test_dataset,root2)
    
    bestroot=id3.post_pruning(dataset, root, L, K)
    bestroot2=id3.post_pruning(dataset,root2,L, K)
    print 'The accurancy of info_gain after post_pruning is: ',id3.calculateAccuracy(test_dataset, bestroot)
    print 'The accurancy of vi after post_pruning is: ',id3.calculateAccuracy(test_dataset,bestroot2)
    if willPrint==True:
        before_prun_info = file(r'G:\python\machine_learning\data_sets1\before_prun_info.txt', 'w')
        before_prun_info.write(id3.printTree(root, 0))
        before_prun_info.close()
        print id3.printTree(root, 0)
        before_prun_vi = file(r'G:\python\machine_learning\data_sets1\before_prun_vi.txt', 'w')
        before_prun_vi.write(id3.printTree(root2, 0))
        before_prun_vi.close()
        print id3.printTree(root2, 0)
        after_prun_info = file(r'G:\python\machine_learning\data_sets1\after_prun_info.txt', 'w')
        after_prun_info.write(id3.printTree(bestroot, 0))
        after_prun_info.close()
        print id3.printTree(bestroot, 0)
        after_prun_vi = file(r'G:\python\machine_learning\data_sets1\after_prun_vi.txt', 'w')
        after_prun_vi.write(id3.printTree(bestroot2, 0))
        after_prun_vi.close()
        print id3.printTree(bestroot2, 0)
