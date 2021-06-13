JSONFILES = $(wildcard *.json)
DATABASE = database.db

all :

start :
	iperf3 -s --json -D

test :
	sh iperf_test.sh

db : $(DATABASE)

$(DATABASE) : $(JSONFILES) json2db.py Makefile
	python3 json2db.py -o $@ $(JSONFILES)
	sqlite3 $@ ".dump" > $(DATABASE:.db=.sql)

stop :
	-pkill iperf3

clean :
	rm -f *.json

