from node import node

class switch(node):
  def __init__(self, name):
    super().__init__(self)
    self.name = name
    self.port_num = 4

  def set_port_number(self, num):
    self.port_num = num

  def print(self, indent):
    idt = ' ' * indent
    print('{0}{1} ['.format(idt, self.name))
    print('{0}  shape=record'.format(idt))
    print('{0}  label="{{{1}|{{'.format(idt, self.name))
    b_first = 1
    for i in range(self.port_num):
        print('{0}'.format(idt), end='')
        if b_first == 1:
            b_first = 0
        else :
            print('|', end='')

        print('<port{1}>port{1}'.format(idt, i))
    print('') # newline

    print('{0}  }}}}"'.format(idt))
    print('{0}];'.format(idt))
    print('{0}'.format(idt))



