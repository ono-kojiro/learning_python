#PCAPXZ = /var/lib/pcapd/20251031-210323-ue0.pcap.xz
PCAPXZ = $(wildcard /var/lib/pcapd/*.pcap.xz)
NDJSON = $(PCAPXZ:.pcap.xz=.ndjson)
		
$(shell cp bulk2ndjson.py /tmp/)

all : ndjson

ndjson : $(NDJSON)

%.ndjson : %.pcap.xz
	@while [ true ]; do \
	  lsof 2>&1 | grep "$<" >/dev/null; \
	  if [ "$$?" -eq 0 ]; then \
	    echo "file '$<' is opened now. wait 5sec"; \
		sleep 5; \
	  else \
	    break; \
	  fi; \
	done
	
	xz -d -k -c $< | editcap -d - - | \
		HOME=/var/lib/pcapd tshark -T ek -P -V -N dmN -r - | \
		/tmp/bulk2ndjson.py - | tee $@ >/dev/null

