LOGDIR=log/20220301-210116

JSONFILES = $(wildcard $(LOGDIR)/*.json)

DATABASE_DB  = database.db
DATABASE_SQL = database.sql

DATFILE = output.dat
PDFFILE = output.pdf

all : db dat pdf

db : $(DATABASE_DB)

$(DATABASE_DB) : $(JSONFILES) json2db.py
	rm -f $@
	python3 json2db.py -o $@ $(JSONFILES)
	sqlite3 $@ ".dump" > $(DATABASE_SQL)

dat :
	python3 db2dat.py -o output.dat $(DATABASE_DB)

pdf :
	gnuplot \
		-e "pdffile='$(PDFFILE)'" -e "datfile='$(DATFILE)'" \
		dat2pdf.plt

json : $(NORMAL_JSON)

out/%.json : out/%.txt
	python3 log2json.py -o $@ $<

test :
	sh measure.sh

clean :
	rm -f database.db database.sql output.dat
	rm -f $(DATFILE) $(PDFFILE)
	rm -f $(NORMAL_JSON)

