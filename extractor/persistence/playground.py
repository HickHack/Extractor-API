import networkx as nx

data = '''* list item 1
* list item 2
** list item 3
** list item 4
*** list item 5
* list item 6'''.splitlines()

class Node(object):

  def __init__(self, payload):
    self.payload = payload
    self.children = []

  def show(self, indent):
    print(' '*indent, self.payload)
    for c in self.children:
      c.show(indent+2)

def makenest(linelist):
  rootnode = Node(None)
  stack = [(rootnode, 0)]
  for line in linelist:
    for i, c in enumerate(line):
      if c != '*': break
    stars, payload = line[:i], line[i:].strip()
    curlev = len(stars)
    curnod = Node(payload)
    while True:
      parent, level = stack[-1]
      if curlev > level: break
      del stack[-1]
    # a child node of the current top-of-stack
    parent.children.append(curnod)
    stack.append((curnod, curlev))
  rootnode.show(0)

makenest(data)