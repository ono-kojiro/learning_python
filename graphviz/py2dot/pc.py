from node import node

class pc(node):
  def __init__(self, name):
    super().__init__(self)
    self.name = name

  def print(self, indent):
    idt = ' ' * indent
    print('{0}{1}['.format(idt, self.name))
    print('{0}  label=""'.format(idt))
    print('{0}  penwidth=0'.format(idt))
    print('{0}  image="icons/doc_jpg/pc.png"'.format(idt))
    print('{0}];'.format(idt))
    print('{0}'.format(idt))

