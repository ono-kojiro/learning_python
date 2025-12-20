MIBS = ALL
MIBDIRS := /usr/share/snmp/cisco-mibs/v2

AGENTS =
AGENTS += 192.168.0.252
AGENTS += 192.168.0.248

LOGFILES = $(AGENTS:=.log)
ERRFILES  = $(LOGFILES:.log=.err)
JSONFILES = $(LOGFILES:.log=.json)

all : snmp json

test : retrieve

snmp : $(LOGFILES)

$(LOGFILES) : Makefile retrieve.sh

debug :
	@echo logfiles are $(LOGFILES)

%.log :
	sh retrieve.sh \
		--agent $(@:.log=) \
		--mibs $(MIBS) \
		--mibdirs $(MIBDIRS) \
		--output $(@:.log=).log \
		--error  $(@:.log=).err

json : $(JSONFILES)

%.json : %.log Makefile oid2dict.py
	python3 oid2dict.py -o $@ $<

translate :
	prove translate.sh
