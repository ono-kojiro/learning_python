PCAPXZ = /var/lib/pcapd/20251031-210323-ue0.pcap.xz
#PCAPXZ = $(wildcard /var/lib/pcapd/*.pcap.xz)
NDJSON = $(PCAPXZ:.pcap.xz=.ndjson)
		
$(shell cp bulk2ndjson.py /tmp/)

all : ndjson

ndjson : $(NDJSON)

%.ndjson : %.pcap.xz
	xz -d -k -c $< | editcap -d - - | \
		HOME=/var/lib/pcapd tshark -T ek -P -V -N dmN -r - | \
		/tmp/bulk2ndjson.py - | tee $@ >/dev/null


