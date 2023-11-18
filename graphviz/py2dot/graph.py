from subgraph import subgraph
from node import node

class graph():
  def __init__(self, name):
    self.name = name
    self.label = ""
    self.indent = 0
    self.subgraphs = []
    self.rankdir = "TB" # Top to Bottom

  def print(self, indent):
    idt = ' ' * indent
    print('{0}graph {1} {{'.format(idt, self.name))
    #print('{0}  label="{1}";'.format(idt, self.name))
    print('{0}  rankdir="{1}";'.format(idt, self.rankdir))
    print('{0}'.format(idt))

    for sg in self.subgraphs:
        sg.print(indent + 2)

    for sg in self.subgraphs:
        nodes = sg.get_node_all()
        for nd in nodes :
            names = nd.edges
            for name in names :
                print('{0}  {1} -- {2};'.format(idt, nd.name, name))                

    print('{0}}}'.format(idt))

  def add_subgraph(self, sg):
    self.subgraphs.append(sg)

if __name__ == '__main__' :
    main()

