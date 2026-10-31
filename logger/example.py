import sys
import getopt

import logging
logger = logging.getLogger(__name__)

from mymodule import myfunc

def setup_logging(logfile, debug):

    fmt = logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s: %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S%z",
    )

    # FileHandler
    handler = logging.FileHandler(
            logfile,
            mode='w',
    )
    handler.setFormatter(fmt)

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    
    if debug :
        root.setLevel(logging.DEBUG)
    else :
        root.setLevel(logging.INFO)

def usage():
    msg = '''usage: python3 example.py [OPTIONS]

  options:
    -h, --help               show help
    -v, --version            show version
    -d, --debug              enable debug
    -o, --output FILE        output file
    -l, --logfile FILE       logfile
'''
    print(msg, file=sys.stderr)

def main() :
    ret = 0

    try:
        opts, args = getopt.gnu_getopt(
            sys.argv[1:],
            "hvdo:l:",
            [
                "help",
                "version",
                "debug",
                "output=",
                "logfile=",
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    output = None
    debug = False
    logfile = '/tmp/example.log'

    for o, a in opts:
        if o in ("-v", "--version"):
            print('example 0.0.1')
            sys.exit(0)
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-o", "--output"):
            output = a
        elif o in ("-d", "--debug"):
            debug = True
        elif o in ("-l", "--logfile"):
            logfile = a
        else:
            assert False, "unknown option"

    setup_logging(logfile, debug)
    
    logger.info('check output option')

    if output is not None :
        fp = open(output, mode='w', encoding='utf-8')
    else :
        fp = sys.stdout

    fp.write('This is example\n')

    if ret != 0:
        sys.exit(1)

    logger.debug('This is debug log in main')
    myfunc()
    
    if output is not None :
        fp.close()

if __name__ == '__main__':
    sys.exit(main())
