class Node:
    def __init__(self, value=None, right=None, left=None):
        self.right = right
        self.left = left
        self.value = value

    def get_right(self):
        return self.right

    def get_left(self):
        return self.left

    def get_value(self):
        return self.value

    def set_right(self, new_right):
        self.right = new_right

    def set_left(self, new_left):
        self.left = new_left

    def set_value(self, new_value):
        self.value = new_value

    def __repr__(self):
        return f"Node: {self.value}, {self.left}, {self.right}"
