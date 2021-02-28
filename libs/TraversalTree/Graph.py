import abc


class Graph(metaclass=abc.ABCMeta):
    """A class to represent a traversal tree

    Attributes:
        start (Node): The initial state
        scopes ([Node]): The scope states
    """

    @abc.abstractmethod
    def __init__(self, data):
        """
        Args:
            data (str): The data that should be parsed into the start state and scope states
        """
        pass

    @abc.abstractmethod
    def testScope(self, currentNode):
        """Check if the current node is a scope state.

        Args:
            currentNode (Node)

        Returns:
            bool: True if the current node is a scope state, False otherwise
        """
        pass

    @abc.abstractmethod
    def generateSuccessors(self, currentNode):
        """A method that generates all possible next states based on the current one

        Args:
            currentNode (Node)

        Returns:
            [Node]: A list containing all possible next states
        """
        pass
