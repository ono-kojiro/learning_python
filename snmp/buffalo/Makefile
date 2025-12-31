MIBS = ALL
MIBDIRS := /usr/share/snmp/mibs

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
AGENTS += 192.168.11.252
AGENTS += 192.168.0.248

LOGFILES = $(AGENTS:=.log)
ERRFILES  = $(LOGFILES:.log=.err)
JSONFILES = $(LOGFILES:.log=.json)

DATABASE = database.db

ARP_OPTS = --localnet --ignoredups --plain --ouifile=/usr/share/arp-scan/ieee-oui.txt --macfile=/etc/arp-scan/mac-vendor.txt

all : json analyze db

prepare :
	sudo apt -y install snmp net-tools

snmp : presnmp $(LOGFILES)

presnmp :
	rm -rf $(LOGFILES)

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
	rm -rf arpscan.log
	ssh -t abaoaqu "sudo -E arp-scan $(ARP_OPTS)" | tee -a arpscan.log
	ssh -t solomon "sudo -E arp-scan $(ARP_OPTS)" | tee -a arpscan.log
	python3 arp2json.py -o arpscan.json arpscan.log

db :
	rm -f $(DATABASE)
	python3 arp2db.py -o $(DATABASE) arpscan.json
	python3 json2db.py -o $(DATABASE) $(JSONFILES)
	python3 createview.py -o $(DATABASE)
	sqlite3 $(DATABASE) ".dump" > $(DATABASE:.db=.sql)

test :
	cat $(DATABASE:.db=.sql)
	sqlite3 $(DATABASE) ".schema"
	@echo ""
	sqlite3 $(DATABASE) "select * from connections_view;"
	@echo ""
	sqlite3 $(DATABASE) "select * from agents_view;"
	@echo ""
	sqlite3 $(DATABASE) "select * from a2a_view;"
	@echo ""
	sqlite3 $(DATABASE) "select * from a2t_view;"

schema :
	sqlite3 $(DATABASE) ".schema"

check :
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

