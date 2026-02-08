DATABASE = database.db
SCHEMA   = schema.yml

all : test

init :
	rm -f $(DATABASE)
	python3 createdb.py -o $(DATABASE) $(SCHEMA)

test : init db yaml

db :
	python3 yml2db.py -o $(DATABASE) example.yml

yaml: 
	python3 db2yml.py $(DATABASE)

schema :
	sqlite3 $(DATABASE) ".schema"

dump :
	sqlite3 $(DATABASE) ".dump"

