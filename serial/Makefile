BAUDRATE = 115200
PORT     = /dev/ttyS0

all :
	python3 example.py -b $(BAUDRATE) -p $(PORT)

pico :
	picocom -b $(BAUDRATE) --imap lfcrlf $(PORT)

test :
	python3 -m serial.tools.miniterm $(PORT) $(BAUDRATE)

help :
	python3 -m serial.tools.miniterm -h

login :
	python3 login.py -b $(BAUDRATE) -d $(PORT)

list :
	python3 -m serial.tools.list_ports

.PHONY : \
    all clean test pico

