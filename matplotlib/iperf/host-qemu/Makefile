TARGET  = qemu
BUFLENS = 4K 8K 16K 32K 64K 128K 256K 512K 1024K
SERVER = 192.168.7.2

JSONFILES = $(addprefix $(TARGET)-,$(BUFLENS:=.json))

all : $(JSONFILES)

$(TARGET)-%.json :
	iperf3 -c $(SERVER) --length $* --get-server-output --json > $@
	sleep 1

clean :
	rm -f $(JSONFILES)

