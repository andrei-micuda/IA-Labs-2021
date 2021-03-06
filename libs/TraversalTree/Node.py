import abc


class Node(metaclass=abc.ABCMeta):
    """A class to represent a node in a traversal tree (NOT in the initial graph)

    Attributes:
        info (object): The information that the current state
        parent (Node): The parent of the current node (or None if the current node does not have a parent)
        cost (Int): The cost of the path from the start node to the current node
        heuristic (Int): The approximate cost from the current node to a scope state
        pathCost (Int): The approximate cost of the path from the start node to a scope state going through the current known path
    """

    def __init__(self, info, parent, cost=1, heuristic=1):
        """
        Args:
            info (object): The information to be stored in the new node
            parent (Node): Node to be assigned as the parent of the new node
            cost (int): The cost associated with the path to the current node in the traversal tree
        """
        self.info = info
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic
        self.pathCost = self.cost + self.heuristic

    def getPath(self):
        """Method that retrieves the path from the root to the current node

        Returns:
            [Node]: The path as a list of Node objects
        """
        path = [self]
        node = self
        while node.parent is not None:
            path.insert(0, node.parent)
            node = node.parent

        return path

    def printPath(self, printLength=False, printCost=False):
        """Method that prints the path from the root to the current node
        Args:
            printLength (bool): Whether to print the path's length or not

        Returns:
            int: The length of the path
        """
        lst = self.getPath()
        for node in lst:
            print(str(node))

        if printLength:
            print(f'Length: {len(lst) - 1}')

        if printCost:
            print(f'Cost: {self.cost}')

        return len(lst)

    def containsInPath(self, nodeInfo):
        """Method that checks if the given node is already part of the current path

        Args:
            nodeInfo (Node.info): The information of the node which we want to check against the path's nodes

        Returns:
            bool: True if a Node with the same info already exists in the path, False otherwise
        """
        pathNode = self
        while pathNode is not None:
            if pathNode.info == nodeInfo:
                return True
            pathNode = pathNode.parent
        return False

    def __repr__(self):
        return str(self.info)

    @abc.abstractmethod
    def __str__(self):
        pass
