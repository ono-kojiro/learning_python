ZIPFILE1 = $(HOME)/Downloads/Cisco/doc_jpg.zip

ZIPURL1 = https://www.cisco.com/content/dam/en_us/about/ac50/ac47/doc_jpg.zip
ZIPURL2 = https://www.cisco.com/content/dam/en_us/about/ac50/ac47/3015_jpeg.zip

ZIPFILE1 = $(shell basename $(ZIPURL1))
ZIPFILE2 = $(shell basename $(ZIPURL2))

#DOTFILES = $(wildcard *.dot)
DOTFILES = example.dot
PNGFILES = $(DOTFILES:.dot=.png)

all : dot png

help :
	@echo "usage : make <target>"
	@echo "target list"
	@echo "  icons"
	@echo "  rename"
	@echo "  dot"
	@echo "  clean"

dot :
	python3 dict2dot.py > example.dot

fetch :
	curl -L -O $(ZIPURL1)
	curl -L -O $(ZIPURL2)

extract :
	mkdir -p orig/doc_jpg
	mkdir -p orig/3015_jpeg
	unzip $(ZIPFILE1) -d orig/doc_jpg
	unzip $(ZIPFILE2) -d orig/3015_jpeg

icons :
	mkdir -p icons/doc_jpg
	mkdir -p icons/3015_jpeg
	python3 jpeg2png.py -o icons/doc_jpg   orig/doc_jpg
	python3 jpeg2png.py -o icons/3015_jpeg orig/3015_jpeg

rename :
	python3 rename.py

icon :
	$(MAKE) -C icons

image :
	$(MAKE) -C images

png : $(PNGFILES)

%.png : %.dot
	dot -Tpng -o $@ $<

debug :
	echo $(DOTFILES)

clean :
	rm -f $(PNGFILES)

.PHONY : \
    all clean test icons image dot


