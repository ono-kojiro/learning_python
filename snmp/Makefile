#
# write following lines in $HOME/.snmp/snmp.conf
#
#     mibdirs $HOME/.snmp/mibs
#     mibs    all
#
ZIPURL1 = https://www.cisco.com/content/dam/en_us/about/ac50/ac47/doc_jpg.zip
ZIPURL2 = https://www.cisco.com/content/dam/en_us/about/ac50/ac47/3015_jpeg.zip

ZIPFILE1 = $(shell basename $(ZIPURL1))
ZIPFILE2 = $(shell basename $(ZIPURL2))

#SNMP_AGENTS = 192.168.10.1 192.168.60.1
SNMP_AGENTS = 192.168.10.1
	
LOGFILES = $(addsuffix .log,$(SNMP_AGENTS))
JSONFILES =  $(LOGFILES:.log=.json)
DOTFILES  =  $(JSONFILES:.json=.dot)
PNGFILES  =  $(DOTFILES:.dot=.png)

MIBDIRS = $(HOME)/.snmp/mibs
MIBS    = ALL

all : log json dot png

prepare: fetch extract icon

fetch :
	curl -L -O $(ZIPURL1)
	curl -L -O $(ZIPURL2)

extract :
	mkdir -p orig/doc_jpg
	mkdir -p orig/3015_jpeg
	unzip $(ZIPFILE1) -d orig/doc_jpg
	unzip $(ZIPFILE2) -d orig/3015_jpeg

icon :
	mkdir -p icons/doc_jpg
	mkdir -p icons/3015_jpeg
	python3 jpeg2png.py -o icons/doc_jpg   orig/doc_jpg
	python3 jpeg2png.py -o icons/3015_jpeg orig/3015_jpeg


debug :
	echo $(JSONFILES)

sync :
	rsync -avz opnsense:/usr/local/share/snmp/mibs $(HOME)/.snmp/

system :
	snmpwalk -v 2c -c public $(SNMP_AGENT) system

net :
	snmpwalk -v 2c -c public $(SNMP_AGENT) IF-MIB::ifDescr
	snmpwalk -v 2c -c public $(SNMP_AGENT) IF-MIB::ifOutOctets
	snmpwalk -v 2c -c public $(SNMP_AGENT) IF-MIB::ifInOctets
	snmpwalk -v 2c -c public $(SNMP_AGENT) IF-MIB::ifTable

#debug :
#	snmpwalk -v 2c -c public $(SNMP_AGENT) IP-MIB::ipNetToPhysicalPhysAddress
disk :
	snmpwalk -v 2c -c public $(SNMP_AGENT) UCD-DISKIO-MIB::diskIOTable

log : $(LOGFILES)

%.log :
	snmpwalk  -v 2c -c public -OX $* . > $@

json : $(JSONFILES)

%.json : %.log
	python3 oid2dict.py -o $@ $<

dot : $(DOTFILES)

%.dot : %.json
	python3 summarize.py -o $@ $<

png : $(PNGFILES)

%.png : %.dot
	dot -Tpng -o $@ $<

translate:
	snmptranslate 1.3.6.1.4.1


#fetch :
#	curl -o RFC-1212.txt https://docs.sensu.io/sensu-enterprise/latest/files/RFC-1212-MIB.txt

test_old :
	SMIPATH=":$(HOME)/.snmp/mibs/:." \
		smidump --level=6 -k -f python RFC1213-MIB.txt > RFC1213-MIB.dic

clean :
	rm -f $(JSONFILES) $(DOTFILES) $(PNGFILES)

.PHONY : \
	all clean test walk log

