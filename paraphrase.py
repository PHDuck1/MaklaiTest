from typing import Generator, List
from itertools import permutations
from nltk.tree import *
from copy import deepcopy


def is_divided(labels: List[str]) -> bool:
    """Check if NP's in the node is divided by CC or ','"""
    previous_label = None

    for label in labels:
        if label == 'NP' and previous_label == 'NP':
            return False

        elif label in ('CC', ',') and previous_label in ('CC', ','):
            return False

        previous_label = label
    return True


def is_changeable(tree:  Tree) -> bool:
    """Check the NP subtree to determine if order of subtrees can be changed"""

    child_labels = [child.label() for child in tree]
    if child_labels.count('NP') < 2:
        return False

    if not is_divided(child_labels):
        return False

    return True


def get_np_indexes(tree: Tree) -> List[int]:
    """Find indexes of NP's in the tree"""
    indexes = []
    for index, child in enumerate(tree):
        if child.label() == 'NP':
            indexes.append(index)
    return indexes


def permute_subtree(tree: Tree, np_indexes: List) -> Generator[Tree, None, None]:
    """Generate alternative permutations of the subtree"""
    perms = permutations(np_indexes)

    for perm in perms:
        new_tree = deepcopy(tree)
        for old_index, new_index in zip(np_indexes, perm):
            new_tree[old_index] = tree[new_index]
        yield new_tree


def main():
    with open('tree.txt', 'r') as f:
        input_tree = f.read()

    syntax_tree = Tree.fromstring(input_tree)
    syntax_tree.pretty_print(unicodelines=True, nodedist=4)

    for subtree in syntax_tree.subtrees(filter=lambda s: s.label() == 'NP'):
        if is_changeable(subtree):
            for changed_tree in permute_subtree(subtree, get_np_indexes(subtree)):
                changed_tree.pretty_print()


if __name__ == '__main__':
    main()
