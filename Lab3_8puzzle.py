import copy

from libs.TraversalTree.Node import Node as AbstractNode
from libs.TraversalTree.Graph import Graph as AbstractGraph

'''
Node.info = [[a, b, c], [d, e, 0], [g, h, i]]
          = -------
            |a|b|c|
            -------
            |d|e| |
            -------
            |g|h|i|
            -------
'''


class Node(AbstractNode):
    def __str__(self):
        s = ""
        for line in self.info:
            line = [x if x != '0' else ' ' for x in line]
            s += '-------\n'
            s += f'|{"|".join(line)}|\n'
        s += '-------\n'
        s += f"Heuristic cost: {self.heuristic}"
        return s


def getPosInMatrix(mat, elem):
    for i, line in enumerate(mat):
        for j, e in enumerate(line):
            if e == elem:
                return i, j
    return - 1


class Graph(AbstractGraph):
    def __init__(self, data):
        self.start = [line.split() for line in data.split('\n')]
        self.scopes = [[["1", "2", "3"], ["4", "5", "6"], ["7", "8", "0"]]]

    def testScope(self, currentNode):
        return currentNode.info in self.scopes

    def existsSolution(self, nodeInfo):
        """Returneaza True sau False daca starea data de infoNod corespunde
        unui joc care poate fi rezolvat.

        1 2 3
        4 5 8
        0 6 7

        Ne formam permutarea celor 8 placute citite de sus in jos si de st la dr:
        1 2 3 4 5 8 6 7

        Existenta solutiei depinde de nr. de inversiuni ale permutarii.

        DE CE?
        """
        lst = []
        for line in nodeInfo:
            for elem in line:
                lst.append(elem)

        lst = [x for x in lst if x != '0']

        inversionCount = 0
        for i, x in enumerate(lst):
            for y in lst[i + 1:]:
                if x > y:
                    inversionCount += 1

        if inversionCount % 2 == 0:
            return True
        return False

    def generateSuccessors(self, currentNode, heuristicType):
        lstSucc = []
        dir = [[-1, 0], [1, 0], [0, -1], [0, 1]]

        emptyLine, emptyCol = getPosInMatrix(currentNode.info, '0')
        for dl, dc in dir:
            newLine, newCol = (emptyLine + dl, emptyCol + dc)
            try:
                if newLine < 0 or newCol < 0:
                    continue
                newInfo = copy.deepcopy(currentNode.info)
                newInfo[emptyLine][emptyCol] = newInfo[newLine][newCol]
                newInfo[newLine][newCol] = '0'

                if not currentNode.containsInPath(newInfo):
                    lstSucc.append(
                        Node(
                            newInfo,
                            currentNode,
                            currentNode.cost + 1,
                            self.calcHeuristic(newInfo, heuristicType)
                        )
                    )
            except IndexError:
                pass
        return lstSucc

    def calcHeuristic(self, nodeInfo, heuristicType):
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

    def admissibleHeuristic1(self, nodeInfo):
        cost = 0
        for i in range(3):
            for j in range(3):
                if nodeInfo[i][j] != '0' and (nodeInfo[i][j] != self.scopes[0][i][j]):
                    cost += 1
        return cost

    def admissibleHeuristic2(self, nodeInfo):
        cost = 0
        for i in range(3):
            for j in range(3):
                if nodeInfo[i][j] == '0':
                    continue
                iInScope, jInScope = getPosInMatrix(
                    self.scopes[0], nodeInfo[i][j])
                cost += abs(i - iInScope) + abs(j - jInScope)
        return cost

    def __repr__(self):
        s = ""
        s += f"Start state:\n{self.start.__repr__()}\n"

        s += "Scope states:\n"
        for scope in self.scopes:
            s += scope.__repr__() + "\n"
        return s


def aStar(graph, numOfSolutions, heuristicType):
    if not graph.existsSolution(graph.start):
        return

    queue = [Node(graph.start, None, 0)]

    while len(queue) > 0:
        currentNode = queue.pop(0)

        if graph.testScope(currentNode):
            print("Solution!")
            currentNode.printPath(printLength=True, printCost=True)
            print("================================\n")
            numOfSolutions -= 1
            input()

            if numOfSolutions == 0:
                return

        succ = graph.generateSuccessors(currentNode, heuristicType)

        # we insert each new node in the correct position in order to keep the queue sorted
        for s in succ:
            i = 0
            foundPos = False
            for i in range(len(queue)):
                if queue[i].pathCost > s.pathCost:
                    foundPos = True
                    break

            if foundPos:
                queue.insert(i, s)
            else:
                queue.append(s)


with open("8puzzle.txt") as fin:
    data = fin.read()

g = Graph(data)
aStar(g, 3, "euristica_admisibila_2")
