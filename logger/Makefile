all : test check

test :
	python3 example.py

check :
	LANG=C journalctl -q -o short-iso SYSLOG_IDENTIFIER=example.py

