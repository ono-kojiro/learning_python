PYTHONPATH = ..
PDFFILES = \
	$(wildcard $(HOME)/doc/linuc/*.pdf)

PYTHON = PYTHONPATH=$(PYTHONPATH) python3

CONFIG = ../config.shrc
API_KEY = ../api_key.shrc

NAME = myknowledge

all : help

debug :
	echo $(PDFFILES)

help :
	@echo "usage: make TARGET"
	@echo ""
	@echo "target:"
	@echo "  create"
	@echo "  list"
	@echo "  files"
	@echo "  add"
	@echo "  delete"

create :
	$(PYTHON) create_knowledge.py -a $(API_KEY) -c $(CONFIG) -n $(NAME)

list :
	$(PYTHON) list_knowledges.py -a $(API_KEY) -c $(CONFIG)

add:
	$(PYTHON) add_file_to_knowledge.py -a $(API_KEY) -c $(CONFIG) -n $(NAME) $(PDFFILES)

files:
	$(PYTHON) list_files.py -a $(API_KEY) -c $(CONFIG)

destroy:
	$(PYTHON) delete_knowledges.py -a $(API_KEY) -c $(CONFIG)

