BAUDRATE = 115200
PORT     = /dev/ttyS0

all :
	python3 send_cmd.py -b $(BAUDRATE) -p $(PORT) -- ps

pico :
	picocom -b $(BAUDRATE) --imap lfcrlf $(PORT)

test :
	python3 -m serial.tools.miniterm $(PORT) $(BAUDRATE)

help :
	python3 -m serial.tools.miniterm -h

list :
	python3 -m serial.tools.list_ports

.PHONY : \
    all clean test pico

