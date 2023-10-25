DOTFILES = $(wildcard *.dot)
PNGFILES = $(DOTFILES:.dot=.png)

all : png

png : $(PNGFILES)

%.png : %.dot
	dot -Tpng -o $@ $<

clean :
	rm -f $(PNGFILES)

.PHONY : \
    all clean test


