MIBS = ALL
MIBDIRS := /usr/share/snmp/cisco-mibs/v2

AGENTS =
AGENTS += 192.168.0.252
AGENTS += 192.168.0.248

LOGFILES = $(AGENTS:=.log)
ERRFILES  = $(LOGFILES:.log=.err)
JSONFILES = $(LOGFILES:.log=.json)

all : json analyze

snmp : $(LOGFILES)

%.log :
	sh retrieve.sh \
		--agent $(@:.log=) \
		--mibs $(MIBS) \
		--mibdirs $(MIBDIRS) \
		--output $(@:.log=).log \
		--error  $(@:.log=).err

json : $(JSONFILES)

%.json : %.log
	python3 oid2dict.py -o $@ $<

analyze :
	python3 analyze.py -o result.txt $(JSONFILES)

arp :
	#sudo arp-scan --localnet --quiet --plain --ignoredups | tee arpscan.log
	sudo arp-scan --localnet --plain --ignoredups | tee arpscan.log
	python3 arp2json.py -o arpscan.json arpscan.log
