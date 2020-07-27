# -*- coding: utf-8 -*-
"""
Created on Sept. 2016

@author: nb, gd
"""

from . import queue
from .queue import Queue

class TreeAsBin:
    """
    Simple class for (General) Trees 
    represented as Binary Trees (first child - right sibling)
    """

    def __init__(self, key, child=None, sibling=None):
        """
        Init Tree
        """
        self.key = key
        self.child = child
        self.sibling = sibling


def tutoEx1():
    C1 = TreeAsBin(3, TreeAsBin(-6, None, TreeAsBin(10)))
    C2 = TreeAsBin(8, TreeAsBin(11, TreeAsBin(0, None, TreeAsBin(4)), 
                                TreeAsBin(2, None, TreeAsBin(5))))
    C3 = TreeAsBin(9)
    C1.sibling = C2
    C2.sibling = C3
    return TreeAsBin(15, C1, None)
    