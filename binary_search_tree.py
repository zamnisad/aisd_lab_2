import random
from dop import Errors


class Node:
    def __init__(self, data):
        self.data = data
        self.right_kid = None
        self.left_kid = None
        self.height = 1
        self.color = "r"
        self.parent = None

    @staticmethod
    def find_min(node):
        while node.left_kid:
            node = node.left_kid
        return node

    def remove_node(self, node, data):
        if not node:
            return None

        if data < node.data:
            node.left_kid = self.remove_node(node.left_kid, data)
        elif data > node.data:
            node.right_kid = self.remove_node(node.right_kid, data)
        else:
            if not node.left_kid:
                return node.right_kid
            elif not node.right_kid:
                return node.left_kid

            temp = self.find_min(node.right_kid)
            node.data = temp.data
            node.right_kid = self.remove_node(node.right_kid, temp.data)

        return node


class BST:
    def __init__(self, data):
        self.root = Node(data)
        self.size = 1

    def search(self, data):
        w_node = self.root

        if not data:
            print(Errors.empty_data())
            return

        while w_node:
            if data == w_node.data:
                print(f"Searched: {data}")
                return w_node
            w_node = w_node.right_kid if w_node.data < data else w_node.left_kid

        print(Errors.not_search(data))
        return None

    def push(self, data):
        w_node = self.root
        while True:
            if data == w_node.data:
                print(Errors.equals_elements(data))
                return
            if data > w_node.data:
                if not w_node.right_kid:
                    w_node.right_kid = Node(data)
                    break
                w_node = w_node.right_kid
            else:
                if not w_node.left_kid:
                    w_node.left_kid = Node(data)
                    break
                w_node = w_node.left_kid
        self.size += 1

    def print(self):
        def in_order(node):
            return in_order(node.left_kid) + [node.data] + in_order(node.right_kid) if node else []

        print("Tree (in-order):", in_order(self.root))

    def remove(self, data):
        self.root = self.root.remove_node(self.root, data)
        self.size -= 1


# tree = BST(10)
#
# arr = [int(random.randint(1, 200)) for _ in range(20)]
# random.shuffle(arr)
#
# print(arr)
#
# for i in arr:
#     tree.push(i)
# tree.print()
#
# tree.remove(167)
# tree.remove(31)
#
# tree.print()
