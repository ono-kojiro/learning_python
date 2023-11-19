
from node import node
from subgraph import subgraph
from graph import graph

from switch import switch
from pc import pc
from image import image

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
    
    sw1 = switch('myswitch1')
    sg3.add_node(sw1)

    # node
    nd1 = sg1.get_node('mynode11')
    nd2 = sg2.get_node('mynode23')
    nd1.connect(nd2)

    nd2 = sg2.get_node('mynode21')
    nd3 = sg3.get_node('mynode30')
    nd2.connect(nd3)

    pc1 = pc('mypc')
    sg3.add_node(pc1)

    image1 = image('myimage', 'icons/doc_jpg/small_hub.png')
    sg3.add_node(image1)

    nd2.connect(pc1)
    nd2.connect(image1)
    
    ws1    = image('myws', 'icons/doc_jpg/workstation.png')
    sg2.add_node(ws1)

    g.print(0)

if __name__ == '__main__' :
    main()

