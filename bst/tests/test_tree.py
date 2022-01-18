import pytest, random
from bst.tree import Tree
from bst.node import _Node


@pytest.mark.parametrize("values", [[random.randint(1, 1000) for _ in range(100000)]])
def test_tree_find_max(values):
    correct_res = max(values)
    root = _Node(values[0])
    tree = Tree(root)
    for el in values[1:]:
        tree.insert(root, el)

    result = tree._find_max(root).value
    assert result == correct_res


@pytest.mark.parametrize("values", [[random.randint(1, 1000) for _ in range(100000)]])
def test_tree_find_min(values):
    correct_res = min(values)
    root = _Node(values[0])
    tree = Tree(root)
    for el in values[1:]:
        tree.insert(root, el)

    result = tree._find_min(root).value
    assert result == correct_res


@pytest.mark.parametrize("values", [[random.randint(1, 1000) for _ in range(100000)]])
def test_search(values):
    root = _Node(values[0])
    tree = Tree(root)
    for el in values[1:]:
        tree.insert(root, el)
    node_val = random.randint(1, 1000)
    result = tree._search(root, node_val) is not None
    assert result


