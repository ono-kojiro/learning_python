TOPDIR = ..

PYTHONPATH = $(TOPDIR)
PDFFILES = $(wildcard $(HOME)/doc/linuc/latest/*.pdf)

PYTHON = PYTHONPATH=$(PYTHONPATH) python3

CONFIG = $(TOPDIR)/config.shrc
API_KEY = $(TOPDIR)/api_key.shrc

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

