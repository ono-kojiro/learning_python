PYTHON = python3

all :
	$(PYTHON) json2db.py -o database.db input.json
	$(PYTHON) read_db.py -o output.txt database.db

clean :
	rm -f database.db

