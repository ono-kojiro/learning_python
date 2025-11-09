TOPDIR = $(shell git rev-parse --show-toplevel)/openwebui

PDFFILES = $(wildcard $(HOME)/doc/linuc/latest/*.pdf)
PYTHON = PYTHONPATH=$(TOPDIR) python3

CONFIG = $(TOPDIR)/config.shrc
API_KEY = $(TOPDIR)/api_key.shrc

KNOWLEDGE = myknowledge


all : init

prepare:
	python3 -m pip install -r requirements.txt

init :
	python3 add_file_to_knowledge.py -n example files/*.md

clean :
	python3 delete_files.py
	python3 delete_knowledges.py

normalize:
	find ./files -type f -name "*.md" -print -exec python3 zen2han.py -o {} {} \;

async:
	./chat_completions_async.py template.shrc 2>debug.log

create :
	$(MAKE) -C knowledge create

add :
	$(MAKE) -C files add
	$(MAKE) -C collections add

list :
	$(MAKE) -C knowledge list 

chat :
	$(MAKE) -C chat

delete :
	$(MAKE) -C files delete
	$(MAKE) -C knowledge delete

.PHONY : \
	all clean test add list chat delete

