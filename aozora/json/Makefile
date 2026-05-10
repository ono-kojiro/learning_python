HTMLDIR = ../html
JSONDIR = .

HTMLFILES = $(sort $(wildcard $(HTMLDIR)/*.html))
JSONFILES = $(addprefix $(JSONDIR)/, $(notdir $(HTMLFILES:.html=.json)))

all : json

json : $(JSONFILES)

$(JSONDIR)/%.json : $(HTMLDIR)/%.html
	python3 html2json.py -o $@ $<

clean :
	rm -f $(JSONFILES)

