class graph:
    def __init__(self):
        self.nodes = []
        self.edges = []
    
   


class Node:
    def __init__(self, up = None, down = None, left=None, right=None, key=None, button=None): 
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.key = key
        self.button = button


class connection:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
        self.access =True
    
    def __str__(self):
        return f"Connection({self.node1.key}, {self.node2.key})"
    
    def __repr__(self):
        return self.__str__()
        
    
    def __str__(self):
        return f"Connection({self.node1.key}, {self.node2.key})"
    
    def __repr__(self):
        return self.__str__()


    