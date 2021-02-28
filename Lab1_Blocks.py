import copy
import sys
sys.path.append("..")

from libs.TraversalTree.Node import Node as AbstractNode
from libs.TraversalTree.Graph import Graph as AbstractGraph


class Node(AbstractNode):
    def __str__(self):
        s = ""

        maxHeight = max([len(stack) for stack in self.info])
        for h in range(maxHeight, 0, -1):
            for stack in self.info:
                if len(stack) < h:
                    s += "  "
                else:
                    s += stack[h - 1] + " "
            s += "\n"
        s += "-" * (2 * len(self.info) - 1)
        return s


class Graph(AbstractGraph):
    def __init__(self, data):
        """We will represent a configuration of the stacks as a list of lists.
        The outer list represents the current configuration of the stacks and each inner list represents the block contained in each stack

        Args:
            data (str): The data that should be parsed into the start state and scope states

        Example:
            The input:
                a
                c b
                stari_finale
                b c a
                #
                ---
                b a
                c
            Will be parsed into:
                start: [['a'], ['c', 'b']]
                scopes: [[['b', 'c', 'a'], []], [['b', 'a'], ['c']]]
        """

        [start, scopes] = data.strip().split("stari_finale")
        scopes = scopes.strip().split("---")
        self.start = self.parseStack(start)
        self.scopes = []
        for scope in scopes:
            self.scopes.append(self.parseStack(scope))

    def parseStack(self, data):
        """A method that parses a string into a list of lists

        Args:
            data (str): The data that should be parsed into a state

        Example:
            The input:
                a
                c b
            Will be parsed into: [['a'], ['c', 'b']]
        """
        stacksStr = data.strip().split("\n")
        stacks = [stackStr.strip().split(" ") if stackStr != "#" else []
                  for stackStr in stacksStr]

        return stacks

    def testScope(self, currentNode):
        """Check if the current node's info (i.e. the current configuration of the stacks) is part of the scope configurations.

        Args:
            currentNode (Node)

        Returns:
            bool: True if the current node is a scope state, False otherwise
        """
        return currentNode.info in self.scopes

    def generateSuccessors(self, currentNode):
        """A method that generates all possible next states based on the current one.
        We take each block that is on top of a stack and we move it on top of all the other stacks.

        Args:
            currentNode (Node)

        Returns:
            [Node]: A list containing all possible next states
        """
        lstSucc = []
        currentStacks = currentNode.info
        for i in range(len(currentStacks)):
            # if the current stack is empty we can't do anything
            if len(currentStacks[i]) == 0:
                continue
            tempStacks = copy.deepcopy(currentStacks)
            blockToMove = tempStacks[i].pop()

            for j in range(len(currentStacks)):
                # we don't want to add the block back on the same stack
                if i == j:
                    continue

                newStacks = copy.deepcopy(tempStacks)
                newStacks[j].append(blockToMove)
                if not currentNode.containsInPath(newStacks):
                    newNode = Node(newStacks, currentNode)
                    lstSucc.append(newNode)

        return lstSucc

    def __repr__(self):
        s = ""
        s += f"Start state:\n{self.start.__repr__()}\n"

        s += "Scope states:\n"
        for scope in self.scopes:
            s += scope.__repr__() + "\n"
        return s


def breadthFirst(graph, numOfSolutions):
    queue = [Node(graph.start, None)]

    while len(queue) > 0:
        currentNode = queue.pop(0)

        if graph.testScope(currentNode):
            print("Solution!")
            currentNode.printPath(printLength=True)
            print("================================\n")
            numOfSolutions -= 1
            input()

            if numOfSolutions == 0:
                return

        succ = graph.generateSuccessors(currentNode)
        queue.extend(succ)


def iterativeDepthFirst(graph, maxDepth, numOfSolutions):
    for d in range(1, maxDepth + 1):
        if numOfSolutions == 0:
            return
        numOfSolutions = depthFirst(graph, Node(
            graph.start, None), d, numOfSolutions)


def depthFirst(graph, currentNode, depth, numOfSolutions):
    if depth == 1 and graph.testScope(currentNode):
        print("Solution!")
        currentNode.printPath(printLength=True)
        print("================================\n")
        numOfSolutions -= 1
        input()

        if numOfSolutions == 0:
            return 0

    if depth > 1:
        succ = graph.generateSuccessors(currentNode)
        for nextNode in succ:
            if numOfSolutions != 0:
                numOfSolutions = depthFirst(
                    graph, nextNode, depth - 1, numOfSolutions)

    return numOfSolutions


with open("lab1.txt") as fin:
    data = fin.read()

g = Graph(data)
print(g)
# breadthFirst(g, numOfSolutions=3)
# iterativeDepthFirst(g, maxDepth=5, numOfSolutions=4)
