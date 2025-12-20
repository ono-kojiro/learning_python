MIBS = ALL
MIBDIRS := /usr/share/snmp/cisco-mibs/v2
AGENT = 192.168.0.252

OUTFILE = $(AGENT).log
ERRFILE  = $(AGENT).err
JSONFILE = $(AGENT).json

all : parse

test : retrieve

retrieve :
	sh retrieve.sh \
		--agent $(AGENT) \
		--mibs $(MIBS) \
		--mibdirs $(MIBDIRS) \
		--output $(OUTFILE) \
		--error  $(ERRFILE)

parse :
	python3 oid2dict.py -o $(JSONFILE) $(OUTFILE)

debug :
	prove translate.sh
