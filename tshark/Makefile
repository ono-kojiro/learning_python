#OUTDIR = $(shell pwd)/output
OUTDIR = /home/tshark

INPUT_PCAP_XZ = /var/lib/pcapd/20260505/20260505-10/20260505-104435-ue0.pcap.xz

all :
	python3 pcap2json.py \
		-o $(OUTDIR)/ \
		/var/lib/pcapd/

debug :
	python3 pcap2json.py -o output /var/lib/pcapd/

test1 :
	xz -k -c -d $(INPUT_PCAP_XZ) \
		| tshark -T json -r - > output-json.json

test2:
	xz -k -c -d $(INPUT_PCAP_XZ) \
		| tshark -Y "tcp" -T fields -e frame.time_epoch -e frame.protocols -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e udp.srcport -e udp.dstport -e tcp.flags -E header=n -E separator=, -E quote=d -E occurrence=f -r -


