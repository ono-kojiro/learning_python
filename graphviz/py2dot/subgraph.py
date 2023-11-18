from node import node

class subgraph():
  def __init__(self, name):
    self.name = name
    self.label = ""
    self.indent = 1
    self.nodes = []
    self.cluster = True

  def set_indent(self, indent):
    self.indent = indent

  def print(self, indent):
    idt = ' ' * indent
    print('{0}subgraph {1} {{'.format(idt, self.name))
    print('{0}  label="{1}"'.format(idt, self.name))
    print('{0}  '.format(idt))
    if self.cluster:
      is_cluster = "True"
    else:
      is_cluster = "False"

    print('{0}  cluster={1};'.format(idt, is_cluster))
    for node in self.nodes:
        node.print(indent + 2)
    print('{0}}}'.format(idt))
    print('{0}'.format(idt))

  def add_node(self, node):
    self.nodes.append(node)

  def get_node(self, name):
    for node in self.nodes :
        if node.name == name :
            return node
    return None

  def get_node_all(self):
    return self.nodes

if __name__ == '__main__' :
    main()

