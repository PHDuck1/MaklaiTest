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


def get_indexes(tree: Tree, label: str) -> List[int]:
    """Find indexes of a label in direct children of a tree"""
    indexes = []
    for index, child in enumerate(tree):
        if child.label() == label:
            indexes.append(index)
    return indexes


def permute_subtree(tree: Tree, indexes_to_permute: List) -> Generator[Tree, None, None]:
    """Generate alternative permutations of the subtree"""
    perms = permutations(indexes_to_permute)

    for perm in perms:
        new_tree = deepcopy(tree)
        for old_index, new_index in zip(indexes_to_permute, perm):
            new_tree[old_index] = tree[new_index]
        yield new_tree


def change_node_by_path(tree: Tree, path, new_node):
    """Get node in tree at specified path"""
    node = tree
    # Get the parent of the node to be changed
    for i in path[:-1]:
        node = node[i]

    # Change the node at path to new one
    node[path[-1]] = new_node
    return tree


def find_subtrees(tree: Tree, label: str, path=()):
    """Find subtrees with provided label and return their paths"""
    if not isinstance(tree, Tree):
        return []

    if tree.label() == label:
        if is_changeable(tree):
            return [(tree, path)]

    matches = []
    for i, subtree in enumerate(tree):
        matches.extend(find_subtrees(subtree, label, path=path+(i,)))
    return matches


def main():
    with open('tree.txt', 'r') as f:
        input_tree = f.read()

    syntax_tree = Tree.fromstring(input_tree)
    syntax_tree.pretty_print(unicodelines=True, nodedist=4)

    node_to_change, path = find_subtrees(syntax_tree, 'NP')[0]
    np_indexes = get_indexes(node_to_change, 'NP')

    perms = permute_subtree(node_to_change, np_indexes)

    changed_trees = []
    for perm in perms:
        tree = deepcopy(syntax_tree)

        new_tree = change_node_by_path(tree, path,  perm)
        if new_tree == syntax_tree:
            continue

        changed_trees.append(new_tree)

    for tree in changed_trees:
        tree.pretty_print(unicodelines=True, nodedist=4)
    print(syntax_tree == new_tree)
    print(len(changed_trees))


if __name__ == '__main__':
    main()
