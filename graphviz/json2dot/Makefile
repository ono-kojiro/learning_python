TOPDIR = $(shell git rev-parse --show-toplevel)

ARP_DATABASE_SQL  = $(TOPDIR)/arp/database.sql
SNMP_DATABASE_SQL = $(TOPDIR)/snmp/database.sql

DATABASE = database.db

all : db json dot pdf

arp :
	$(MAKE) -C $(TOPDIR)/arp clean
	$(MAKE) -C $(TOPDIR)/arp

snmp :
	$(MAKE) -C $(TOPDIR)/snmp clean
	$(MAKE) -C $(TOPDIR)/snmp

db :
	rm -f $(DATABASE)
	sqlite3 $(DATABASE) < $(ARP_DATABASE_SQL)
	sqlite3 $(DATABASE) < $(SNMP_DATABASE_SQL)
	python3 createview.py -o $(DATABASE)
	sqlite3 $(DATABASE) ".dump" > $(DATABASE:.db=.sql)

test :
	cat $(DATABASE:.db=.sql)
	sqlite3 $(DATABASE) ".schema"
	@echo ""
	sqlite3 $(DATABASE) "select * from connections_view;"
	@echo ""
	sqlite3 $(DATABASE) "select * from agents_view;"
	@echo ""
	sqlite3 $(DATABASE) "select * from a2a_view;"
	@echo ""
	sqlite3 $(DATABASE) "select * from a2t_view;"

schema :
	sqlite3 $(DATABASE) ".schema"

json :
	python3 db2json.py -o output.json $(DATABASE)

dot :
	python3 json2dot.py -o output.dot output.json

pdf :
	dot -Tpdf -o output.pdf output.dot

check :
	python3 check.py output.json

