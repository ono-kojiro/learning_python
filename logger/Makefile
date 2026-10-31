LOGFILE = /tmp/example.log

all : test

test : version debug warning

version :
	python3 example.py --version

warning :
	python3 example.py -l $(LOGFILE)
	cat $(LOGFILE)

debug :
	python3 example.py -d -l $(LOGFILE)
	cat $(LOGFILE)


old :
	#LANG=C journalctl -q -o short-iso SYSLOG_IDENTIFIER=example.py

mclean :
	rm -f $(LOGFILE)

