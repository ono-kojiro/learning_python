#
# write following lines in $HOME/.snmp/snmp.conf
#
#     mibdirs $HOME/.snmp/mibs
#     mibs    all
#

SNMP_AGENT = 192.168.10.1

MIBDIRS = $(HOME)/.snmp/mibs
MIBS    = ALL

all : test

sync :
	rsync -avz opnsense:/usr/local/share/snmp/mibs $(HOME)/.snmp/

system :
	snmpwalk -v 2c -c public $(SNMP_AGENT) system

net :
	snmpwalk -v 2c -c public $(SNMP_AGENT) IF-MIB::ifDescr
	snmpwalk -v 2c -c public $(SNMP_AGENT) IF-MIB::ifOutOctets
	snmpwalk -v 2c -c public $(SNMP_AGENT) IF-MIB::ifInOctets
	snmpwalk -v 2c -c public $(SNMP_AGENT) IF-MIB::ifTable

debug :
	snmpwalk -v 2c -c public $(SNMP_AGENT) IP-MIB::ipNetToPhysicalPhysAddress
disk :
	snmpwalk -v 2c -c public $(SNMP_AGENT) UCD-DISKIO-MIB::diskIOTable

walk :
	snmpwalk  -v 2c -c public -OX $(SNMP_AGENT) . > snmp-$(SNMP_AGENT).log

test :
	python3 oid2dict.py -o snmp-$(SNMP_AGENT).yml snmp-$(SNMP_AGENT).log

translate:
	snmptranslate 1.3.6.1.4.1


fetch :
	curl -o RFC-1212.txt https://docs.sensu.io/sensu-enterprise/latest/files/RFC-1212-MIB.txt

test_old :
	SMIPATH=":$(HOME)/.snmp/mibs/:." \
		smidump --level=6 -k -f python RFC1213-MIB.txt > RFC1213-MIB.dic

.PHONY : \
	all clean test

