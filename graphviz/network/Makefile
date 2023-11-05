CSVFILES = example.csv
DOTFILES = $(CSVFILES:.csv=.dot)
PNGFILES = $(DOTFILES:.dot=.png)

all: gen dot png

gen :
	python3 gencsv.py -o example.csv

dot : $(DOTFILES)

png : $(PNGFILES)

%.dot : %.csv
	python3 csv2dot.py -o $@ $<

%.png : %.dot
	sfdp -Tpng -o $@ $<

clean :
	rm -f $(DOTFILES) $(PNGFILES)

.PHONY : \
	all clean test dot png

