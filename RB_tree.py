from binary_search_tree import Node, BST
from dop import Errors


class RBT(BST):
    def __init__(self, data):
        super().__init__(data)
        self.root.color = "b"

    def rotate_left(self, node):
        right_kid = node.right_kid
        node.right_kid = right_kid.left_kid

        if right_kid.left_kid:
            right_kid.left_kid.parent = node

        right_kid.parent = node.parent

        if node.parent is None:
            self.root = right_kid
        elif node == node.parent.left_kid:
            node.parent.left_kid = right_kid
        else:
            node.parent.right_kid = right_kid

        right_kid.left_kid = node
        node.parent = right_kid

    def rotate_right(self, node):
        left_kid = node.left_kid
        node.left_kid = left_kid.right_kid

        if left_kid.right_kid:
            left_kid.right_kid.parent = node

        left_kid.parent = node.parent

        if node.parent is None:
            self.root = left_kid
        elif node == node.parent.right_kid:
            node.parent.right_kid = left_kid
        else:
            node.parent.left_kid = left_kid

        left_kid.right_kid = node
        node.parent = left_kid

    def insert_fix(self, node):
        while node.parent and node.parent.color == "r":
            if node.parent == node.parent.parent.left_kid:
                uncle = node.parent.parent.right_kid
                if uncle and uncle.color == "r":
                    node.parent.color = "b"
                    uncle.color = "b"
                    node.parent.parent.color = "r"
                    node = node.parent.parent
                else:
                    if node == node.parent.right_kid:
                        node = node.parent
                        self.rotate_left(node)
                    node.parent.color = "b"
                    node.parent.parent.color = "r"
                    self.rotate_right(node.parent.parent)
            else:
                uncle = node.parent.parent.left_kid
                if uncle and uncle.color == "r":
                    node.parent.color = "b"
                    uncle.color = "b"
                    node.parent.parent.color = "r"
                    node = node.parent.parent
                else:
                    if node == node.parent.left_kid:
                        node = node.parent
                        self.rotate_right(node)
                    node.parent.color = "b"
                    node.parent.parent.color = "r"
                    self.rotate_left(node.parent.parent)
        self.root.color = "b"

    def push(self, data):
        w_node = Node(data)
        w_node.color = "r"
        parent = None
        current = self.root

        while current:
            parent = current
            if data < current.data:
                current = current.left_kid
            elif data > current.data:
                current = current.right_kid
            else:
                print(Errors.equals_elements(data))
                return

        w_node.parent = parent

        if parent is None:
            parent = self.root
        elif parent.data > data:
            parent.left_kid = w_node
        else:
            parent.right_kid = w_node

        self.size += 1

        self.insert_fix(w_node)

    def print(self):
        def print_in_order(node, level=0, prefix="Root: "):
            if node is not None:
                print(" " * (level * 4) + prefix + str(node.data) + f" (С: {node.color})")
                if node.left_kid or node.right_kid:
                    if node.left_kid:
                        print_in_order(node.left_kid, level + 1, "L--- ")
                    else:
                        print(" " * ((level + 1) * 4) + "L--- None")
                    if node.right_kid:
                        print_in_order(node.right_kid, level + 1, "R--- ")
                    else:
                        print(" " * ((level + 1) * 4) + "R--- None")

        print_in_order(self.root)

    def remove(self, data):
        node = self.search(data)
        if node is None:
            print(Errors.not_search(data))
            return

        if node.left_kid and node.right_kid:
            successor = self._find_min(node.right_kid)
            node.data = successor.data
            node = successor

        replacement = node.left_kid if node.left_kid else node.right_kid

        if replacement:
            replacement.parent = node.parent
            if node.parent is None:
                self.root = replacement
            elif node == node.parent.left_kid:
                node.parent.left_kid = replacement
            else:
                node.parent.right_kid = replacement
            if node.color == "b":
                self._remove_fix(replacement)
        elif node.parent is None:
            self.root = None
        else:
            if node.color == "b":
                self._remove_fix(node)
            if node.parent:
                if node == node.parent.left_kid:
                    node.parent.left_kid = None
                else:
                    node.parent.right_kid = None

        self.size -= 1

    def _remove_fix(self, node):
        while node != self.root and (node is None or node.color == "b"):
            if node == node.parent.left_kid:
                sibling = node.parent.right_kid
                if sibling.color == "r":
                    sibling.color = "b"
                    node.parent.color = "r"
                    self.rotate_left(node.parent)
                    sibling = node.parent.right_kid
                if (sibling.left_kid is None or sibling.left_kid.color == "b") and \
                        (sibling.right_kid is None or sibling.right_kid.color == "b"):
                    sibling.color = "r"
                    node = node.parent
                else:
                    if sibling.right_kid is None or sibling.right_kid.color == "b":
                        if sibling.left_kid:
                            sibling.left_kid.color = "b"
                        sibling.color = "r"
                        self.rotate_right(sibling)
                        sibling = node.parent.right_kid
                    sibling.color = node.parent.color
                    node.parent.color = "b"
                    if sibling.right_kid:
                        sibling.right_kid.color = "b"
                    self.rotate_left(node.parent)
                    node = self.root
            else:
                sibling = node.parent.left_kid
                if sibling.color == "r":
                    sibling.color = "b"
                    node.parent.color = "r"
                    self.rotate_right(node.parent)
                    sibling = node.parent.left_kid
                if (sibling.left_kid is None or sibling.left_kid.color == "b") and \
                        (sibling.right_kid is None or sibling.right_kid.color == "b"):
                    sibling.color = "r"
                    node = node.parent
                else:
                    if sibling.left_kid is None or sibling.left_kid.color == "b":
                        if sibling.right_kid:
                            sibling.right_kid.color = "b"
                        sibling.color = "r"
                        self.rotate_left(sibling)
                        sibling = node.parent.left_kid
                    sibling.color = node.parent.color
                    node.parent.color = "b"
                    if sibling.left_kid:
                        sibling.left_kid.color = "b"
                    self.rotate_right(node.parent)
                    node = self.root
        if node:
            node.color = "b"

    @staticmethod
    def _find_min(node):
        while node.left_kid:
            node = node.left_kid
        return node
