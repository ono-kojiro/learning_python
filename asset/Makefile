DATABASE = database.db

SCHEMA = schema.yml

all : test

init :
	rm -f $(DATABASE)
	python3 createdb.py -o $(DATABASE) $(SCHEMA)

	$(MAKE) dump

dump :
	sqlite3 $(DATABASE) ".dump"

schema :
	sqlite3 $(DATABASE) ".schema"

test :
	$(MAKE) init
	$(MAKE) insert
	$(MAKE) debug
	$(MAKE) show

insert :
	python3 yml2db.py -o $(DATABASE) example.yml

debug :
	sqlite3 $(DATABASE) "select * from assets_view;"
	sqlite3 $(DATABASE) "select * from interfaces_view;"

show :
	python3 show_list.py $(DATABASE) > output.yml

