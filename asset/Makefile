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
	python3 yml2db.py -o $(DATABASE) example.yml

