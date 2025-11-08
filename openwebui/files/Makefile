PYTHONPATH = ..
PDFFILES = \
	$(wildcard $(HOME)/doc/linuc/*.pdf)

PYTHON = PYTHONPATH=$(PYTHONPATH) python3

CONFIG = ../config.shrc
API_KEY = ../api_key.shrc

all : help

debug :
	echo $(PDFFILES)

help :
	@echo "usage: make TARGET"
	@echo ""
	@echo "target:"
	@echo "  add"
	@echo "  list"
	@echo "  delete"

add :
	$(PYTHON) add_files.py -a $(API_KEY) -c $(CONFIG) $(PDFFILES)

list :
	$(PYTHON) list_files.py -a $(API_KEY) -c $(CONFIG)

delete:
	$(PYTHON) delete_files.py -a $(API_KEY) -c $(CONFIG)

