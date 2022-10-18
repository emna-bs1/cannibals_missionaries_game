"""
    missionaries and cannibals game
"""
import colorama
from colorama import Fore

# -- global variables

# repeated nodes / used for the tree construction
repeated = []
# possible actions
actions = [
    # adding or retrieving 1 missionary / boat direction
    (1, 0, 1),
    # adding or retrieving 1 missionary + 1 cannibal / boat direction
    (1, 1, 1),
    # adding or retrieving 1 cannibal / boat direction
    (0, 1, 1),
    # adding or retrieving 2 missionaries / boat direction
    (2, 0, 1),
    # adding or retrieving 2 cannibals / boat direction
    (0, 2, 1)
]
# holds node's level / used for tree display
modification = 0
# used for tree display
modifications = []
# contains the problem's solution
solution = [False,]


class Node:
    def __init__(self, state=(3, 3, 1), rep=False, m_eaten=False, level=0):
        # state represents the parameters of the game as follows
        # (missionaries_nb, cannibals_nb, boat) : on one side of the river (ex: right)

        # a state is redundant
        self.__rep = rep
        # cannibals outnumber missionaries
        self.__m_eaten = m_eaten

        self.__state = state
        self.__children = []
        self.__level = level

    @property
    def state(self):
        return self.__state

    @property
    def children(self):
        return self.__children

    @property
    def malicious(self):
        # missionaries are eaten or node is repeated
        return self.__m_eaten or self.__rep

    @property
    def repeated(self):
        return self.__rep

    @property
    def level(self):
        return self.__level

    def add_node(self, node):
        self.__children.append(node)

    def set_rep(self):
        self.__rep = True

    def set_m_eaten(self):
        self.__m_eaten = True


# an object of type tree holds a pointer on the root element (node)
class Tree:
    def __init__(self):
        # initialisation: 3 missionaries, 3 cannibals, boat is on the right side
        self.__root = Node()

    @property
    def root(self):
        return self.__root


# the queue is used for the tree construction
class Queue:
    def __init__(self):
        self.__elements = []

    def enqueue(self, node):
        self.__elements.append(node)

    def dequeue(self):
        return self.__elements.pop(0)

    def is_empty(self):
        return len(self.__elements) == 0


# recursive function that outputs the tree
# initially called by passing root as a parameter
def print_node(node):
    # print(modifications)get
    if node:
        seq = '  |' * node.level

        if len(modifications) > 0:
            for level in modifications:
                if node.level > level:
                    seq = seq[:level * 3 - 1] + ' ' + seq[level*3:]
                pass

        print(Fore.GREEN, seq, end='')
        color = Fore.GREEN if not node.malicious else (Fore.YELLOW if node.repeated else Fore.RED)
        print(color, '__ parent: ', node.state, ' ,level: ', node.level, sep='')
        # node is parent because it's not malicious
        if not solution[0] and not node.malicious:
            solution.append(node.state)
            if len(node.children) == 0:
                if node.state == (0, 0, 0):
                    solution[0] = True
                else:
                    solution.pop()

        print_tree(node.children)


# children
def print_tree(tr):
    global modification
    if tr:
        ind = 0
        for node in tr:
            if ind == len(tr) - 1:
                modification = node.level
            ind += 1
            if ind == 1 and modification != 0:
                modifications.append(modification)
                modification = 0
            print_node(node)
    else:
        pass


def construct_tree(root):
    global repeated
    q = Queue()
    q.enqueue(root)
    repeated.append(root.state)

    while not q.is_empty():
        node = q.dequeue()
        if node.state == (0, 0, 0):
            break
        elif not node.malicious:
            # determine whether the operation is an addition or a subtraction
            boat = node.state[2]
            op = -1 if boat == 1 else 1
            # state of current node
            state = node.state
            print()
            print(Fore.GREEN, "parent: ", node.state, node.level)
            for action in actions:
                result = tuple(map(lambda x, y: x + op * y if 3 >= x + op * y >= 0 else '*', state, action))
                # print(result, node.level + 1)
                if '*' in result:
                    # test
                    continue
                else:
                    # node creation
                    child = Node(result, level=node.level + 1)
                    malicious = False

                    if result in repeated:
                        malicious = True
                        child.set_rep()

                    m, c, b = result

                    if not malicious and m < c and m != 0 or m > c and m != 3:
                        malicious = True
                        child.set_m_eaten()
                    if not malicious:
                        repeated.append(result)

                    color = Fore.GREEN if not child.malicious else (Fore.YELLOW if child.repeated else Fore.RED)
                    print(color, child.state, 'lev:', child.level)
                    q.enqueue(child)
                    node.add_node(child)

    print(repeated)


def determine_color():
    pass


if __name__ == '__main__':

    # the whole tree (with malicious nodes)
    tree = Tree()

    """
    tree.root.add_node(Node((1, 1, 1)))
    tree.root.children[0].add_node(Node())
    tree.root.children[0].add_node(Node((10, 10, 10)))
    tree.root.children[0].children[0].add_node(Node((8, 8, 8)))

    tree.root.add_node(Node((1, 1, 1)))
    """

    # print_node(tree.root)

    construct_tree(tree.root, )

    print("\n\n\nTree:")
    print_node(tree.root)

    print()
    print(Fore.BLUE, 'Solution To The Riddle', solution[1:])
