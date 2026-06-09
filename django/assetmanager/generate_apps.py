#!/usr/bin/env python3

import sys
import getopt

def usage():
    print(f"Usage: {sys.argv[0]} -o <output> -n <appname>")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:n:", ["help", "output=", "name="])
    except getopt.GetoptError as e:
        print(str(e))
        usage()
        sys.exit(1)

    output = None
    appname = None

    for opt, val in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif opt in ("-o", "--output"):
            output = val
        elif opt in ("-n", "--name"):
            appname = val

    if not output or not appname:
        usage()
        sys.exit(1)

    class_name = appname.capitalize() + "Config"

    with open(output, "w", encoding="utf-8") as fp:
        fp.write("from django.apps import AppConfig\n\n")
        fp.write(f"class {class_name}(AppConfig):\n")
        fp.write(f"    default_auto_field = 'django.db.models.BigAutoField'\n")
        fp.write(f"    name = '{appname}'\n\n")
        fp.write(f"    def ready(self):\n")
        fp.write(f'        print("### MyappConfig.ready() CALLED ###")\n')
        fp.write(f"        import {appname}.admin_loader\n")

if __name__ == "__main__":
    main()

