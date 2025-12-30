ARP_OPTS = \
 --localnet --ignoredups --plain \
 --ouifile=/usr/share/arp-scan/ieee-oui.txt \
 --macfile=/etc/arp-scan/mac-vendor.txt

all : test

prepare :
	sudo apt -y install arp-scan

test :
	LANG=C sudo -E arp-scan $(ARP_OPTS)

