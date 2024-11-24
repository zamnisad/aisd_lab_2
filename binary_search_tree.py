import os.path
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


class BST:
    def __init__(self, data):
        self.root = Node(data)
        self.size = 1
        self.height = 1

    def search(self, data, to_print=False):
        w_node = self.root

        if not data:
            print(Errors.empty_data())
            return

        while w_node:
            if data == w_node.data:
                if to_print:
                    print(f"Searched: {data}")
                return w_node
            w_node = w_node.right_kid if w_node.data < data else w_node.left_kid

        print(Errors.not_search(data))
        return None

    @staticmethod
    def update_height(node):
        if not node:
            return

        stack = [node]
        while stack:
            current = stack[-1]

            l_height = current.left_kid.height if current.left_kid else 0
            r_height = current.right_kid.height if current.right_kid else 0
            current.height = max(l_height, r_height) + 1

            stack.pop()

            if current.right_kid:
                stack.append(current.right_kid)
            if current.left_kid:
                stack.append(current.left_kid)

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
        self.update_height(self.root)
        self.height = self.root.height

    def remove(self, data):
        node_to_remove = self.search(data)
        if not node_to_remove:
            return

        self.root = self._remove(self.root, node_to_remove)
        if self.root:
            self.update_height(self.root)
            self.height = self.root.height
        self.size -= 1

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

            if not node.left_kid:
                return node.right_kid
            elif not node.right_kid:
                return node.left_kid

            min_node = self._find_min(node.right_kid)
            node.data = min_node.data
            node.right_kid = self._remove(node.right_kid, min_node)

        self.update_height(node)
        return node

    @staticmethod
    def _find_min(node):
        current = node
        while current.left_kid:
            current = current.left_kid
        return current

    def print(self):
        def print_in_order(node, level=0, prefix="Root: "):
            if node is not None:
                print(" " * (level * 4) + prefix + str(node.data))
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


def get_dependence(rand, file, model, maximum=20001, stride=1000):
    def _generate_arr(maxi):
        if rand:
            arr = random.sample(range(0, maxi), maxi)
        else:
            arr = list(range(maxi))
        return arr

    print(f"Random: {rand}, File: {file}, Model: {model.__name__}")

    with open(os.path.join(r"TXT/", file), "w") as f:
        for i in range(stride, maximum, stride):
            arr = _generate_arr(i)
            tree = model(arr[0])
            for j in range(1, i):
                tree.push(arr[j])
            f.write(f"Size: {i}\tHeight: {tree.height}\n")
            print(f"Size: {i}\tHeight: {tree.height}")


get_dependence(True, "BST.txt", BST)
# tree = BST(50)
# for i in [30, 70, 20, 40, 60, 80]:
#     tree.push(i)
#
# print("Tree before removal:")
# tree.print()
#
# tree.remove(70)  # Удаляем элемент 70
# print("\nTree after removal of 70:")
# tree.print()
#
# tree.remove(50)  # Удаляем корень
# print("\nTree after removal of 50:")
# tree.print()
