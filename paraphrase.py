from nltk.tree import *

with open('tree.txt', 'r') as f:
    tree_input = f.read()

tree = Tree.fromstring(tree_input)
tree.pretty_print(unicodelines=True, nodedist=4)
