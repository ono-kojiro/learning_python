DEBUG = 1

REQUESTS_REDMINE = \
  REQUESTS_CA_BUNDLE=`pwd`/mylocalca.pem \
  python3 requests-redmine.py --debug $(DEBUG)

URL_ROOT = https://192.168.0.98/redmine

URL_MYPAGE = $(URL_ROOT)/my/page
URL_PNG = $(URL_ROOT)/projects/myproject/issues/gantt.png?month=10&months=6&year=2023&zoom=2
URL_PDF = $(URL_ROOT)/issues/gantt.pdf?month=9&months=6&year=2023&zoom=2
URL_C = $(URL_ROOT)/attachments/download/1/main.c

all : test

test :
	python3 html2txt.py -o page.txt page.html

help :
	@echo "usage: make target"
	@echo ""
	@echo "  target"
	@echo "    root"
	@echo "    c"
	@echo "    pdf"
	@echo "    mypage"

pdf :
	rm -f gantt.pdf
	$(REQUESTS_REDMINE) -o gantt.pdf "$(URL_PDF)"

png :
	rm -f gantt.png
	$(REQUESTS_REDMINE) -o gantt.png "$(URL_PNG)"

c :
	rm -f main.c
	$(REQUESTS_REDMINE) -o main.c "$(URL_C)"

root :
	rm -f root.html
	$(REQUESTS_REDMINE) -o root.html "$(URL_ROOT)"

mypage :
	rm -f mypage.html
	$(REQUESTS_REDMINE) -o mypage.html "$(URL_MYPAGE)"

install :
	python3 -m pip install -r requirements.txt

