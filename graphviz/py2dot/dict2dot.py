
from node import node
from subgraph import subgraph
from graph import graph

def main() :
    g = graph('mygraph')
    sg1 = subgraph('mysubgraph1')
    g.add_subgraph(sg1)

    sg2 = subgraph('mysubgraph2')
    g.add_subgraph(sg2)
    
    sg3 = subgraph('mysubgraph3')
    g.add_subgraph(sg3)

    sg1.add_node(node('mynode10'))
    sg1.add_node(node('mynode11'))
    sg1.add_node(node('mynode12'))
    
    nd2 = node('mynode2')
    sg2.add_node(nd2)
    sg2.add_node(node('mynode20'))
    sg2.add_node(node('mynode21'))
    sg2.add_node(node('mynode22'))
    sg2.add_node(node('mynode23'))

    sg3.add_node(node('mynode30'))
    sg3.add_node(node('mynode31'))
    

    # node
    nd1 = sg1.get_node('mynode11')
    nd2 = sg2.get_node('mynode23')
    nd1.connect(nd2)

    nd2 = sg2.get_node('mynode21')
    nd3 = sg3.get_node('mynode30')
    nd2.connect(nd3)

    g.print(0)

if __name__ == '__main__' :
    main()

