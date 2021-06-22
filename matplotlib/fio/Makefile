JSONFILES = $(sort $(wildcard *.json))
DATABASE_DB  = database.db
DATABASE_SQL = database.sql

DATFILE = output.dat
PDFFILE = output.pdf

all : db dat graph

db : $(DATABASE_DB)

$(DATABASE_DB) : $(JSONFILES) json2db.py
	python3 json2db.py -o $(DATABASE_DB) $(JSONFILES)
	sqlite3 $(DATABASE_DB) ".dump" > $(DATABASE_SQL)

dat :
	python3 db2dat.py -o output.dat $(DATABASE_DB)

graph :
	gnuplot \
		-e "epsfile='$(PDFFILE)'" -e "datfile='$(DATFILE)'" \
		dat2eps.plt

test :
	sh measure.sh

clean :
	rm -f database.db database.sql output.dat
	rm -f $(DATFILE) $(PDFFILE)

