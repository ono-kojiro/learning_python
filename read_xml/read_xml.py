import getopt
import re
import sys

from lxml import etree

def read_schema(filepath):
    #fp = open(filepath, mode="r", encoding="utf-8")
    #lines = fp.read()
    #fp.close()

    doc = etree.parse(filepath)
    doc.xinclude()
    schema = etree.XMLSchema(doc)
    return schema


def print_events(parser):
    for act, elem in parser.read_events():
        # print('{0} : {1}'.format(act, elem.tag))
        pass

def main() :
    ret = 0

    try:
        options, args = getopt.getopt(
            sys.argv[1:],
            "hvo:s:",
            [
              "help",
              "version",
              "schema=",
              "output="
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    output = None
    schema_xml = None

    for option, arg in options:
        if option in ("-v", "-h", "--help"):
            usage()
            sys.exit(0)
        elif option in ("-o", "--output"):
            output = arg
        elif option in ("-s", "--schema"):
            schema_xml = arg
        else:
            assert False, "unknown option"

    if output == None:
        print("no output option")
        ret += 1

    if schema_xml == None:
        print("no schema option")
        ret += 1

    if ret != 0:
        sys.exit(1)

    # xmlfiles = []
    # xsdfiles = []

    # for filepath in args :
    #    ext = os.path.splitext(filepath)[1]
    #    if ext == '.xsd' :
    #        xsdfiles.append(filepath)
    #    elif ext == '.xml' :
    #        xmlfiles.append(filepath)

    # lines = ''
    # for filepath in xsdfiles :
    #    print('parse {0}'.format(filepath))
    #    fp = open(filepath, mode='r', encoding='utf-8')
    #    lines += fp.read()
    #    fp.close()

    # print(lines.encode('utf-8'))
    # doc = etree.fromstring(lines)
    # doc.xinclude()
    # schema = etree.XMLSchema(doc)

    doc = etree.parse(schema_xml)
    doc.xinclude()
    schema = etree.XMLSchema(doc)

    for filepath in args:
        fp = open(filepath, encoding="utf-8")

        parser = etree.XMLPullParser(events=("start", "end"))

        while 1:
            line = fp.readline()
            if not line:
                break

            line = re.sub(r"\r?\n?$", "", line)
            line = re.sub(r"\t", "", line)
            parser.feed(line)
            print_events(parser)

        fp.close()
        root = parser.close()
        print(etree.tostring(root, pretty_print=True, encoding="unicode"))
        ret = schema.assertValid(root)
        print(ret)


if __name__ == "__main__":
    main()
