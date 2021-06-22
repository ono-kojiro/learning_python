LOGFILES = $(wildcard *.log)
JSONFILES = $(LOGFILES:.log=.json)
DATFILE = output.dat
PDFFILE = output.pdf

all : dat

dat : $(DATFILE)

$(DATFILE) : $(LOGFILES)
	./log2json.py -o $@ $(LOGFILES)

graph :
	gnuplot \
		-e "pdffile='$(PDFFILE)'" \
		-e "datfile='$(DATFILE)'" \
		dat2pdf.plt


clean :
	rm -f $(DATFILE)


