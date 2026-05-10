JSONDIR   = ../json
NDJSONDIR = .

JSONFILES   = $(sort $(wildcard $(JSONDIR)/*.json))
NDJSONFILES = $(addprefix $(NDJSONDIR)/, $(notdir $(JSONFILES:.json=.ndjson)))

all : ndjson

ndjson : $(NDJSONFILES)

$(NDJSONDIR)/%.ndjson : $(JSONDIR)/%.json json2ndjson.py
	python3 json2ndjson.py -o $@ $<

clean :
	rm -f $(NDJSONFILES)

