from bst.node  import _Node


class Tree:
    def __init__(self, root = None):
        self._root = root
        self._size = 0

    def __len__(self):
        return self._size

    def __contains__(self, item):
        return self._search(self._root, item) is not None

    def _search(self, subtree:_Node, target):
        if subtree is None:
            return None
        elif target < subtree.value:
            return self._search(subtree.left, target)
        elif target > subtree.value:
            return self._search(subtree.right, target)
        else:
            return subtree

    def _find_min(self, subtree):
        if subtree is None:
            return None
        elif subtree.left is None:
            return subtree
        else:
            return self._find_min(subtree.left)

    def _find_max(self, subtree):
        if subtree is None:
            return None
        elif subtree.right is None:
            return subtree
        else:
            return self._find_max(subtree.right)

    def insert(self, subtree, value):
        if subtree is None:
            subtree = _Node(value)
        elif subtree.value > value:
            subtree.left = self.insert(subtree.left, value)
        elif subtree.value < value:
            subtree.right = self.insert(subtree.right, value)
        return subtree

def preorder_traversal(subtree):
    if subtree is not None:
        print(subtree.value)
        preorder_traversal(subtree.left)
        preorder_traversal(subtree.right)

def inorder_traversal(subtree):
    if subtree is not None:
        inorder_travers(subtree.left)
        print(subtree.value)
        inorder_travers(subtree.right)
