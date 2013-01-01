'''
Useful data structures & functions to implement search algorithms
    Data structures are obtained from Pacman AI projects (John DeNero & Dan Klein)
        [http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html]
    Utilities functions are from aima-python
        [...]
'''
import heapq, math, copy
from route.models import Edge

#______________________________________________________________________________
# Data structures

class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.

      Note that this PriorityQueue does not allow you to change the priority
      of an item.  However, you may insert the same item multiple times with
      different priorities.
    """
    def  __init__(self):
        self.heap = []

    def push(self, item):
        priority = item.path_cost
        pair = (priority,item)
        heapq.heappush(self.heap,pair)

    def extend(self, collection):
        """Extend from a collection of nodes."""
        for item in collection:
            self.push(item)

    def pop(self):
        (priority,item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

infinity = 1.0e400

def Dict(**entries):  
    """Create a dict out of the argument=value arguments. 
    >>> Dict(a=1, b=2, c=3)
    {'a': 1, 'c': 3, 'b': 2}
    """
    return entries

class DefaultDict(dict):
    """Dictionary with a default value for unknown keys."""
    def __init__(self, default):
        self.default = default

    def __getitem__(self, key):
        if key in self: return self.get(key)
        return self.setdefault(key, copy.deepcopy(self.default))
    
    def __copy__(self):
        copy = DefaultDict(self.default)
        copy.update(self)
        return copy

#______________________________________________________________________________
# Utility functions

def distance((ax, ay), (bx, by)):
    "The distance between two (x, y) points."
    return math.hypot((ax - bx), (ay - by))

def distance2((ax, ay), (bx, by)):
    "The square of the distance between two (x, y) points."
    return (ax - bx)**2 + (ay - by)**2
    
def update(x, **entries):
    """Update a dict; or an object with slots; according to entries.
    >>> update({'a': 1}, a=10, b=20)
    {'a': 10, 'b': 20}
    >>> update(Struct(a=1), a=10, b=20)
    Struct(a=10, b=20)
    """
    if isinstance(x, dict):
        x.update(entries)   
    else:
        x.__dict__.update(entries) 
    return x 

def argmin(seq, fn):
    """Return an element with lowest fn(seq[i]) score; tie goes to first one.
    >>> argmin(['one', 'to', 'three'], len)
    'to'
    """
    best = seq[0]; best_score = fn(best)
    for x in seq:
        x_score = fn(x)
        if x_score < best_score:
            best, best_score = x, x_score
    return best

def getEdge(A, B):
    """ Return the edge contains two vertexs """
    edge = None

    edges = Edge.objects.filter(vertex_start__id=A).filter(vertex_end__id=B)
    if len(edges) > 0:
        edge = edges[0]
    else:
        edge = \
            Edge.objects.filter(vertex_start__id=B).filter(vertex_end__id=A)[0]
            
    return edge