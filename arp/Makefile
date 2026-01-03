ARP_OPTS = \
 --localnet --ignoredups --plain \
 --ouifile=/usr/share/arp-scan/ieee-oui.txt \
 --macfile=/etc/arp-scan/mac-vendor.txt

all : arp

prepare :
	sudo apt -y install arp-scan

arp :
	rm -rf arpscan.log
	ssh -t abaoaqu "sudo -E arp-scan $(ARP_OPTS)" | tee -a arpscan.log
	ssh -t solomon "sudo -E arp-scan $(ARP_OPTS)" | tee -a arpscan.log
	python3 arp2json.py -o arpscan.json arpscan.log

clean :
	rm -f arpscan.log arpscan.json

