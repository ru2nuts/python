# 
from binarytree import tree, bst, heap, Node

my_tree = tree(height=3, is_perfect=False)
my_bst = bst(height=3, is_perfect=True)
my_heap = heap(height=3, is_max=True, is_perfect=False)

print(my_tree)
print(my_bst)
print(my_heap)


# ======================================================================================================================

def build_from_middle(vals: list):
    if len(vals) == 0:
        return None
    mid_index = len(vals) // 2
    root = Node(vals[mid_index])
    root.left = build_from_middle(vals[:mid_index])
    root.right = build_from_middle(vals[mid_index + 1:])
    return root


sorted_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

b1 = build_from_middle(sorted_list)

print(b1)


# ======================================================================================================================


def build_bst(vals: list) -> Node:
    if (len(vals) == 0):
        return None
    root = Node(vals[0])
    for v in vals[1:]:
        root = add_bst_val(root, v)
    return root


def add_bst_val(tree: Node, v: int) -> Node:
    if (v < tree.value):
        tree.left = Node(v) if (tree.left == None) else add_bst_val(tree.left, v)
    else:
        tree.right = Node(v) if (tree.right == None) else add_bst_val(tree.right, v)
    return tree


sorted_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

b1 = build_bst(sorted_list)
print(b1)

# ======================================================================================================================


sorted_list = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

b1 = build_bst(sorted_list)
print(b1)

# ======================================================================================================================


import random

print(build_bst(random.sample(range(1, 101), 50)))

print(build_bst(random.sample(range(1, 101), 50)))

print(build_bst(random.sample(range(1, 101), 50)))

print(build_bst(random.sample(range(1, 101), 50)))


# ======================================================================================================================

class rint(int):
    is_r: bool = False

    def __new__(cls, x, is_r, *args, **kwargs):
        ii = super(rint, cls).__new__(cls, x)
        # ii = 0
        ii.is_r = is_r
        return ii

    def __str__(self):
        return super().__str__() + ('-r' if self.is_r else '')


class RBNode(Node):

    def __init__(self, value, left=None, right=None, is_red=False):
        cn = rint(value, is_red)
        super().__init__(cn, left, right)


def build_rb_bst(vals: list) -> RBNode:
    if (len(vals) == 0):
        return None
    root = RBNode(vals[0])
    for v in vals[1:]:
        root = add_rb_bst_val(root, v)
    return root


def add_rb_bst_val(tree: RBNode, v: rint) -> RBNode:
    if (v < tree.value):
        tree.left = RBNode(v, is_red=not tree.value.is_r) if (tree.left == None) else add_rb_bst_val(tree.left, v)
    else:
        tree.right = RBNode(v, is_red=not tree.value.is_r) if (tree.right == None) else add_rb_bst_val(tree.right, v)
    return tree


sorted_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

b1 = build_rb_bst(sorted_list)
print(b1)



z = rint(7, True)
print(z < 8)
print(z + 8)

print(z - 8)

print(z < 8)

bb: bool = True
aa: bool = 0
print(aa)

