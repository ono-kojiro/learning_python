
LOGFILES  = arpscan.log
JSONFILES = $(LOGFILES:.log=.json)
DATABASE  = database.db

ARP_OPTS = \
 --localnet --ignoredups --plain \
 --ouifile=/usr/share/arp-scan/ieee-oui.txt \
 --macfile=/etc/arp-scan/mac-vendor.txt

all : log json db

prepare :
	sudo apt -y install arp-scan

log : $(LOGFILES)

$(LOGFILES) :
	rm -rf $@
	ssh -t abaoaqu "sudo -E arp-scan $(ARP_OPTS)" | tee -a $@
	ssh -t solomon "sudo -E arp-scan $(ARP_OPTS)" | tee -a $@

json : $(JSONFILES)

%.json : %.log
	python3 arp2json.py -o $@ $<

db : $(DATABASE)

$(DATABASE) : $(JSONFILES)
	rm -f $@
	python3 arp2db.py -o $@ $(JSONFILES)
	sqlite3 $@ ".dump" > $(DATABASE:.db=.sql)

clean :
	rm -f $(JSONFILES) $(DATABASE)

mclean :
	$(MAKE) clean
	rm -f $(LOGFILES)

