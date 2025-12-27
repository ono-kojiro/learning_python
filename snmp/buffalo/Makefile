MIBS = ALL
MIBDIRS := /usr/share/snmp/cisco-mibs/v2

OIDS = \
  SNMPv2-MIB::sysDescr \
  IF-MIB::ifDescr \
  IF-MIB::ifOutOctets \
  IF-MIB::ifInOctets \
  IF-MIB::ifTable \
  IF-MIB::interfaces \
  IP-MIB::ip \
  BRIDGE-MIB::dot1dBridge

AGENTS =
AGENTS += 192.168.0.252
AGENTS += 192.168.0.248

LOGFILES = $(AGENTS:=.log)
ERRFILES  = $(LOGFILES:.log=.err)
JSONFILES = $(LOGFILES:.log=.json)

DATABASE = database.db

all : json analyze

snmp : $(LOGFILES)

%.log :
	sh retrieve.sh \
		--agent $(@:.log=) \
		--mibs $(MIBS) \
		--mibdirs $(MIBDIRS) \
		--oids "$(OIDS)" \
		--output $(@:.log=).log \
		--error  $(@:.log=).err

json : $(JSONFILES)

%.json : %.log
	python3 oid2dict.py -o $@ $<

analyze :
	python3 analyze.py -o result.log $(JSONFILES)

arp :
	#sudo arp-scan --localnet --quiet --plain --ignoredups | tee arpscan.log
	sudo arp-scan --localnet --plain --ignoredups | tee arpscan.log
	python3 arp2json.py -o arpscan.json arpscan.log

db :
	rm -f $(DATABASE)
	python3 arp2db.py -o $(DATABASE) arpscan.json
	python3 json2db.py -o $(DATABASE) $(JSONFILES)
	python3 createview.py -o $(DATABASE)
	sqlite3 $(DATABASE) ".dump" > $(DATABASE:.db=.sql)
	cat $(DATABASE:.db=.sql)
	sqlite3 $(DATABASE) ".schema"
	sqlite3 $(DATABASE) "select * from macaddrs_view;"

debug :
	sh retrieve.sh \
		--agent 192.168.0.248 \
		--mibs $(MIBS) \
		--mibdirs $(MIBDIRS) \
		--oids "$(OIDS)" \
		--output cisco.log \
		--error  cisco.err
	python3 oid2dict.py -o cisco.json cisco.log

clean :
	rm -f $(LOGFILES) $(JSONFILES)

