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

all : json db

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

db : $(DATABASE)

$(DATABASE) : $(JSONFILES)
	rm -f $@
	python3 json2db.py -o $@ $(JSONFILES)
	sqlite3 $@ ".dump" > $(DATABASE:.db=.sql)

schema :
	sqlite3 $(DATABASE) ".schema"

check :
	$(MAKE) check-cisco
	$(MAKE) check-buffalo
	python3 oid2dict.py -o cisco.json cisco.log
	cat cisco.json
	python3 oid2dict.py -o buffalo.json buffalo.log
	cat buffalo.json

check-cisco :
	sh retrieve.sh \
		--agent 192.168.0.248 \
		--mibs $(MIBS) \
		--mibdirs $(MIBDIRS) \
  		--oids "SNMPv2-MIB::sysDescr" \
		--output cisco.log \
		--error  cisco.err

check-buffalo :
	sh retrieve.sh \
		--agent 192.168.11.252 \
		--mibs $(MIBS) \
		--mibdirs $(MIBDIRS) \
  		--oids "SNMPv2-MIB::sysDescr" \
		--output buffalo.log \
		--error  buffalo.err

clean :
	rm -f $(JSONFILES) $(DATABASE)

mclean :
	$(MAKE) clean
	rm -f $(LOGFILES)
