from typing import Generator, List, Tuple, Dict
from itertools import permutations, product
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


def find_changeable_subtrees(tree: Tree, label: str, path=()):
    """Find subtrees with provided label and return their paths"""
    if not isinstance(tree, Tree):
        return []

    if tree.label() == label:
        if is_changeable(tree):
            return [path]

    matches = []
    for i, subtree in enumerate(tree):
        matches.extend(find_changeable_subtrees(subtree, label, path=path+(i,)))
    return matches


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


def get_node_by_path(tree: Tree, path: Tuple[int]) -> Tree:
    """Get node in tree at specified path"""
    node = tree
    # Get the parent of the node to be changed
    for i in path:
        node = node[i]

    # Change the node at path to new one
    return node


def change_node_by_path(tree: Tree, path, new_node):
    """Get node in tree at specified path"""
    node = tree
    # Get the parent of the node to be changed
    for i in path[:-1]:
        node = node[i]

    # Change the node at path to new one
    node[path[-1]] = new_node
    return tree


def get_multiple_subtrees_perms(changeable_subtrees: List[Tuple[int]], syntax_tree: Tree) -> Dict[Tuple[int], List[Tree]]:
    """Get permutations of all NP subtrees
    Store them in dictionary where key is the path to the subtree and value is a list of permutations of this subtree
    Example:
    changeable_subtrees = [(2, 1, 1, 1, 1), (2, 1, 1, 1, 2)]
    multiple_node_perms = {
        (2, 1, 1, 1, 1): [
            Tree('NP', [Tree('NP', [Tree('NNS', ['bars'])]), Tree(',', [',']), Tree('NP', [Tree('NNS', ['clubs'])])])
            Tree('NP', [Tree('NP', [Tree('NNS', ['clubs'])]), Tree(',', [',']), Tree('NP', [Tree('NNS', ['bars'])])])
        ],
        (2, 1, 1, 1, 2): [
            Tree('NP', [Tree('NP', [Tree('NNS', ['restaurants'])]), Tree(',', [',']), Tree('NP', [Tree('NNS', ['clubs'])])])
            Tree('NP', [Tree('NP', [Tree('NNS', ['clubs'])]), Tree(',', [',']), Tree('NP', [Tree('NNS', ['restaurants'])])])
        ]
    }"""
    multiple_node_perms = {}
    for node_path in changeable_subtrees:
        # Get NP subtree and indexes of children NP subtrees
        changeable_node = get_node_by_path(syntax_tree, node_path)
        np_indexes = get_indexes(changeable_node, 'NP')

        # Get all permutations of NP subtree and store them in dictionary
        current_node_perms = permute_subtree(changeable_node, np_indexes)
        multiple_node_perms[node_path] = list(current_node_perms)

    return multiple_node_perms


def get_paraphrased_trees(subtrees_permutations: Dict[Tuple[int], List[Tree]], syntax_tree: Tree):
    """Get all possible paraphrased trees from permutations of subtrees"""

    # Generate all possible combinations of permutations of subtrees using itertools.product
    list_of_combinations = list(product(*subtrees_permutations.values()))

    # Generate a list of dictionaries - instructions for changing each subtree in the original tree
    list_of_dicts = []
    for combination in list_of_combinations:
        temp_dict = {}
        for path, node in zip(subtrees_permutations.keys(), combination):
            temp_dict[path] = node
        list_of_dicts.append(temp_dict)

    # Change every changeable subtree in the original tree and store them in a list
    paraphrased_trees = []
    for i, d in enumerate(list_of_dicts):
        tree = deepcopy(syntax_tree)
        for path, node in d.items():
            change_node_by_path(tree, path, node)
        if tree == syntax_tree:
            continue
        paraphrased_trees.append(tree)

    return paraphrased_trees


def main():
    with open('tree.txt', 'r') as f:
        input_tree = f.read()

    syntax_tree = Tree.fromstring(input_tree)
    syntax_tree.pretty_print()

    # Find subtrees with label 'NP', which have child NP's whose order can be changed, and return their paths
    changeable_subtrees = find_changeable_subtrees(syntax_tree, 'NP')

    if not changeable_subtrees:
        return [syntax_tree]

    # Get permutation for subtrees in positions got from previous step
    subtrees_permutations = get_multiple_subtrees_perms(changeable_subtrees, syntax_tree)

    # Get paraphrased trees
    paraphrased_trees = get_paraphrased_trees(subtrees_permutations, syntax_tree)

    print(*[str(t) for t in paraphrased_trees], sep='\n\n')


if __name__ == '__main__':
    main()
