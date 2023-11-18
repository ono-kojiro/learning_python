class node():
  def __init__(self, name):
    self.name = name
    self.label = ""
    self.indent = 1
    self.edges = []

  def connect(self, nd):
    self.edges.append(nd.name)

  def print(self, indent):
    idt = ' ' * indent
    print('{0}node ['.format(idt))
    print('{0}  label="{1}"'.format(idt, self.name))
    print('{0}] {1};'.format(idt, self.name))
    print('{0}'.format(idt))

