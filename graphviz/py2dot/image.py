from node import node

class image(node):
  def __init__(self, name, path):
    super().__init__(self)
    self.name = name
    self.path = path

  def print(self, indent):
    idt = ' ' * indent
    print('{0}{1}['.format(idt, self.name))
    print('{0}  label="{1}"'.format(idt, self.name))
    print('{0}  penwidth=0'.format(idt))
    print('{0}  image="{1}"'.format(idt, self.path))
    print('{0}];'.format(idt))
    print('{0}'.format(idt))

