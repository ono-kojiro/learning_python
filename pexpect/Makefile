BAUDRATE = 115200
DEVICE   = /dev/ttyS0

all : run

login :
	./login.py -b $(BAUDRATE) -d $(DEVICE) --config config.json

run :
	./run.py -b $(BAUDRATE) -d $(DEVICE) \
		expr.sh  quote.sh  subshell.sh \
		return_false.sh

expr :
	./run.py -b $(BAUDRATE) -d $(DEVICE) expr.sh
	sh expr.sh

adv :
	./run.py quote.sh expr.sh subshell.sh

logout :
	./logout.py -b $(BAUDRATE) -d $(DEVICE)

install :
	sudo apt -y install lrzsz

.PHONY : \
	all clean test \
	login run logout install

