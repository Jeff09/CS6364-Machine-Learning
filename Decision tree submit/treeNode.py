# -*- coding: utf-8 -*-

class node:
    def __init__(self,attr=None, label=-1, leaf=-1, right=None,left=None, height=0):
        self.attr=attr #the name of the attributem.
        self.leaf = leaf
        self.label = label #The most common value in the targetAttribute {0, 1}.
        self.right=right
        self.left=left
        self.height = height#the height of the tree
    
    