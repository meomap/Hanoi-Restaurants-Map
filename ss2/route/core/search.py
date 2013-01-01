'''
Created on May 29, 2012
    Path finding by uniform cost search
@author: meo map
'''
from utils import PriorityQueue
from searchAgents import *

def uniformCostSearch(problem):
    "** Search the node of least total cost first. **"   
    fringe = PriorityQueue()
    
    closed = {} # Bookeeping for visisted nodes
    fringe.push(Node(problem.initial))
    while fringe:
        node = fringe.pop()  # Choose a node to expand   
        if problem.goal_test(node.state):   # Check goal state
            return node
        if node.state not in closed:
            closed[node.state] = True       # Add state node to visited tree
            fringe.extend(node.expand(problem))  # Expanding node  
    return None