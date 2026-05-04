HTMLFILES = 57228_58735.html 56680_62855.html 56669_58756.html
TEXTFILES = $(HTMLFILES:.html=.txt)
JSONFILES = $(TEXTFILES:.txt=.ndjson)

all : text json

fetch:
	for filename in $(HTMLFILES); do \
		if [ ! -e "$${filename}" ]; then \
			wget https://www.aozora.gr.jp/cards/001779/files/$${filename}; \
		else \
			echo "Skip $${filename}"; \
		fi \
	done

text : $(TEXTFILES)

json : $(JSONFILES)

%.txt : %.html
	html2text -o $@ $<

%.ndjson : %.txt
	python3 txt2ndjson.py -o $@ $<

clean :
	rm -f $(TEXTFILES) $(JSONFILES)

