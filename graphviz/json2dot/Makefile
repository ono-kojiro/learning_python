TOPDIR = $(shell git rev-parse --show-toplevel)

DATABASE = $(TOPDIR)/snmp/buffalo/database.db

all : json dot pdf

debug :
	@echo $(TOPDIR)

json :
	python3 db2json.py -o output.json $(DATABASE)

dot :
	python3 json2dot.py -o output.dot output.json

pdf :
	dot -Tpdf -o output.pdf output.dot

check :
	python3 check.py output.json

schema :
	sqlite3 $(DATABASE) ".schema"

