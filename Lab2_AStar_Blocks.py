import copy

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
        The cost for each move is the alphabetical index associated with the block's label

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
                    newNode = Node(
                        newStacks, currentNode, currentNode.cost + ord(blockToMove) - ord('a') + 1)
                    lstSucc.append(newNode)

        return lstSucc

    def __repr__(self):
        s = ""
        s += f"Start state:\n{self.start.__repr__()}\n"

        s += "Scope states:\n"
        for scope in self.scopes:
            s += scope.__repr__() + "\n"
        return s

    def getBlocksLabels(self):
        blocks = []
        for st in self.start:
            blocks.extend(st)
        return blocks

    def calcHeuristics(self, nodeInfo, heuristicType):
        """Given a node's info and an heuristic type we calculate the heuristic for the current node

        Args:
            nodeInfo (Node.info)
            heuristicType (String): The heuristic to be used for calculations

        Returns:
            Int: The heuristic value for the current node
        """
        if heuristicType == "euristica_banala":
            return self.basicHeuristic(nodeInfo)
        elif heuristicType == "euristica_admisibila_1":
            return self.admissibleHeuristic1(nodeInfo)
        elif heuristicType == "euristica_admisibila_2":
            return self.admissibleHeuristic2(nodeInfo)
        else:
            raise Exception("Unknown heuristic type")

    def basicHeuristic(self, nodeInfo):
        return 0 if nodeInfo in self.scopes else 1

    def calculateHeuristicCost1(self, nodeInfo, scopeInfo):
        heuristicCost = 0

        for block in self.getBlocksLabels():
            foundIndexInNode = False
            indexInNode = 0
            while not foundIndexInNode:
                if block in nodeInfo[indexInNode]:
                    foundIndexInNode = True
                    break
                indexInNode += 1

            foundIndexInScope = False
            indexInScope = 0
            while not foundIndexInScope:
                if block in scopeInfo[indexInScope]:
                    foundIndexInScope = True
                    break
                indexInScope += 1

            if indexInNode != indexInScope:
                heuristicCost += 1

        return heuristicCost

    def admissibleHeuristic1(self, nodeInfo):
        """Comparam configuratia nodeInfo cu fiecare dintre starile finale,
        numarand cate blocuri din starea curenta nu se afla la locul lor din
        starea finala. Astfel numarul de blocuri care vor trebui mutate cel putin
        o data reprezinta estimarea costului de a ajunge in acea stare finala.

        Dintre toate estimarile calculate pentru fiecare stare finala, alegem
        drept euristica estimarea minima.
        """

        heuristicCost = self.calculateHeuristicCost1(
            nodeInfo, self.scopes[0].info)

        for scope in self.scopes:
            heuristicCost = min(heuristicCost, self.calculateHeuristicCost1(
                nodeInfo, scope.info))

    def calculateHeuristicCost2(self, nodeInfo, scopeInfo):
        heuristicCost = 0

        for block in self.getBlocksLabels():
            foundIndexInNode = False
            indexInNode = 0
            while not foundIndexInNode:
                if block in nodeInfo[indexInNode]:
                    foundIndexInNode = True
                    break
                indexInNode += 1

            foundIndexInScope = False
            indexInScope = 0
            while not foundIndexInScope:
                if block in scopeInfo[indexInScope]:
                    foundIndexInScope = True
                    break
                indexInScope += 1

            if indexInNode != indexInScope:
                heuristicCost += ord(block) - ord('a') + 1

        return heuristicCost

    def admissibleHeuristic2(self, nodeInfo):
        """Asemanator cu 1. De aceasta data pentru fiecare bloc care nu se
        afla la locul lui, in loc sa adunam 1 la estimare, vom aduna costul
        de a muta blocul respectiv (stim ca blocul acela trebuie mutat cel putin
        o data, deci pentru a ajunge la starea finala vom face la un moment dat
        un pas de costul respectiv).
        """
        heuristicCost = self.calculateHeuristicCost2(
            nodeInfo, self.scopes[0].info)

        for scope in self.scopes:
            heuristicCost = min(heuristicCost, self.calculateHeuristicCost2(
                nodeInfo, scope.info))


def aStar(graph, heuristicType):
    open = [Node(graph.start, None, 0)]
    closed = []

    while len(open) > 0:
        currentNode = open.pop(0)
        closed.append(currentNode)

        if graph.testScope(currentNode):
            print("Solution!")
            currentNode.printPath(printLength=True, printCost=True)
            print("================================\n")
            return

        succ = graph.generateSuccessors(currentNode)
        succCopy = succ.copy()

        # we insert each new node in the correct position in order to keep the open queue sorted, based on the minimum approximate cost of the path to a scope
        for s in succCopy:
            foundInOpenQueue = False
            for el in open:
                if s.info == el.info:
                    foundInOpenQueue = True

                    # if the new found path has a better approximation, we want to replace the node already in the open queue
                    if s.pathCost < el.pathCost:
                        open.remove(el)
                    # else we dont want to add the current successor to the open queue, since we already have it with a better approximation
                    else:
                        succ.remove(s)
                    break

            # if we haven't found the node in the open queue, we are going to look for it in the closed queue
            if not foundInOpenQueue:
                for el in closed:
                    if s.info == el.info:
                        # if the new found path has a better approximation, we want to remove the node from the closed queue since we want to recalculate the paths
                        if s.pathCost < el.pathCost:
                            closed.remove(el)
                        # else we dont want to add the current node to the open queue, since we already have it with a better approximation
                        else:
                            succ.remove(s)
                        break

        for s in succ:
            i = 0
            while i < len(open):
                if open[i].pathCost >= s.pathCost:
                    break
                i += 1
            open.insert(i, s)


with open("blocks.txt") as fin:
    data = fin.read()

g = Graph(data)

aStar(g, "euristica_admisibila_2")
