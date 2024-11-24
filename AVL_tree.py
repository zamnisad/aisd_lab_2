from dop import Errors
from binary_search_tree import BST, Node, get_dependence


class AVLT(BST):
    def __init__(self, data):
        super().__init__(data)

    @staticmethod
    def get_height(node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left_kid) - self.get_height(node.right_kid) if node else 0

    def r_rotate(self, y):
        if not y or not y.left_kid:
            return y
        x = y.left_kid
        T = x.right_kid

        x.right_kid = y
        y.left_kid = T

        y.height = 1 + max(self.get_height(y.left_kid), self.get_height(y.right_kid))
        x.height = 1 + max(self.get_height(x.left_kid), self.get_height(x.right_kid))

        return x

    def l_rotate(self, x):
        if not x or not x.right_kid:
            return x
        y = x.right_kid
        T = y.left_kid

        y.left_kid = x
        x.right_kid = T

        x.height = 1 + max(self.get_height(x.left_kid), self.get_height(x.right_kid))
        y.height = 1 + max(self.get_height(y.left_kid), self.get_height(y.right_kid))

        return y

    def balancing(self, node):
        if not node:
            return None

        balance = self.get_balance(node)

        if balance > 1:
            if self.get_balance(node.left_kid) < 0:
                node.left_kid = self.l_rotate(node.left_kid)
            return self.r_rotate(node)

        if balance < -1:
            if self.get_balance(node.right_kid) > 0:
                node.right_kid = self.r_rotate(node.right_kid)
            return self.l_rotate(node)

        return node

    def push(self, data):
        def _insert(node, data):
            if not node:
                return Node(data)

            if node.data == data:
                print(Errors.equals_elements(data))
                return node

            if data < node.data:
                node.left_kid = _insert(node.left_kid, data)
            elif data > node.data:
                node.right_kid = _insert(node.right_kid, data)

            node.height = 1 + max(self.get_height(node.left_kid), self.get_height(node.right_kid))

            return self.balancing(node)

        self.root = _insert(self.root, data)
        self.size += 1
        self.update_height(self.root)
        self.height = self.root.height

    def _remove(self, node, node_to_remove):
        if not node:
            return None

        if node_to_remove.data < node.data:
            node.left_kid = self._remove(node.left_kid, node_to_remove)
        elif node_to_remove.data > node.data:
            node.right_kid = self._remove(node.right_kid, node_to_remove)
        else:
            if not node.left_kid and not node.right_kid:
                return None
            elif not node.left_kid:
                return node.right_kid
            elif not node.right_kid:
                return node.left_kid

            min_node = self._find_min(node.right_kid)
            node.data = min_node.data
            node.right_kid = self._remove(node.right_kid, min_node)

        node.height = 1 + max(self.get_height(node.left_kid), self.get_height(node.right_kid))

        return self.balancing(node)

    def print(self):
        def print_in_order(node, level=0, prefix="Root: "):
            if node is not None:
                print(" " * (level * 4) + prefix + str(node.data) + f" (H: {node.height})")
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

    def get_tree_balance(self):
        def check_balance(node):
            if node:
                balance = self.get_balance(node)
                print(f"Node {node.data} Balance: {balance}")
                check_balance(node.left_kid)
                check_balance(node.right_kid)

        check_balance(self.root)

