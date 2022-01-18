from node_class import Node


class BinarySearchTree:
    def __init__(self, root: Node):
        self.root = root

    def find_min_node(self):
        min_node = self.root
        while min_node.get_left() is not None:
            min_node = min_node.get_left()
        return min_node

    def find_max_node(self):
        max_node = self.root
        while max_node.get_right() is not None:
            max_node = max_node.get_right()
        return max_node

    def find_by_value(self, key: int):
        root_value = self.root.get_value()
        if root_value == key:
            return self.root
        if key > root_value:
            root_right = self.root.get_right()
            root_right.self.find_by_value(key)
        else:
            root_left = self.root.get_left()
            root_left.self.find_by_value(key)
        return False

    def insert_node(self, subtree, value: int):
        if self.root is None:
            subtree = Node(value)
        elif value < self.root.get_value():
            subtree.left = self.insert_node(subtree.left, value)
        elif value > self.root.get_value():
            subtree.right = self.insert_node(subtree.right, value)
        return subtree


a = [60, 25, 100, 17, 35, 80]
root = Node(60)
tree = BinarySearchTree()
for el in a:
    tree.insert_node(root, el)
print(root)
print(root.left, root.right)
