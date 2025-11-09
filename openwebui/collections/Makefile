TOPDIR = ..
PYTHONPATH = $(TOPDIR)
PDFFILES = $(wildcard $(HOME)/doc/linuc/latest/*.pdf)

PYTHON = PYTHONPATH=$(PYTHONPATH) python3

CONFIG = $(TOPDIR)/config.shrc
API_KEY = $(TOPDIR)/api_key.shrc

NAME = myknowledge

all : help

debug :
	echo $(PDFFILES)

help :
	@echo "usage: make TARGET"
	@echo ""
	@echo "target:"
	@echo "  add"
	@echo "  list"

add:
	$(PYTHON) add_file_to_knowledge.py -a $(API_KEY) -c $(CONFIG) -n $(NAME) $(PDFFILES)

list:
	$(PYTHON) list_knowledges.py -a $(API_KEY) -c $(CONFIG)


