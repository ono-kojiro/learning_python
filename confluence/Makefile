#URL = https://cwiki.apache.org/confluence/display/SVN/Apache+Subversion+Wiki
URL = https://cwiki.apache.org/confluence/

ALL_PDF = all.pdf

PDFS = $(sort $(filter-out $(ALL_PDF), $(wildcard *.pdf)))

all : merge

page :
	python3 get_pages.py -u $(URL) -o pages.json

spaces :
	python3 get_spaces.py -u $(URL) -o output.json

clean :
	rm -f *.pdf

test :
	@echo $(PDFS)

merge :
	gs -dNOPAUSE -sDEVICE=pdfwrite -sOUTPUTFILE=$(ALL_PDF) -dBATCH $(PDFS)


