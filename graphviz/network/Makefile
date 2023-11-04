CSVFILES = example.csv
DOTFILES = $(CSVFILES:.csv=.dot)
PNGFILES = $(DOTFILES:.dot=.png)

all: dot png

dot : $(DOTFILES)

png : $(PNGFILES)

%.dot : %.csv
	python3 generate.py -o $@ $<

%.png : %.dot
	sfdp -Tpng -o $@ $<

clean :
	rm -f $(DOTFILES) $(PNGFILES)

.PHONY : \
	all clean test dot png

