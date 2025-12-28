
CISCO_BASE_URL  = https://www.cisco.com/content/dam/en_us/about/ac50/ac47
DOC_JPG_URL   = $(CISCO_BASE_URL)/doc_jpg.zip
3015_JPEG_URL = $(CISCO_BASE_URL)/3015_jpeg.zip

#DOC_JPG_ZIP   = $(HOME)/Downloads/Cisco/doc_jpg.zip
DOC_JPG_ZIP   = $(shell basename $(DOC_JPG_URL))
3015_JPEG_ZIP = $(shell basename $(3015_JPEG_URL))

#DOTFILES = $(wildcard *.dot)
DOTFILES = example.dot
PNGFILES = $(DOTFILES:.dot=.png)
PDFFILES = $(DOTFILES:.dot=.pdf)

all : png pdf

help :
	@echo "usage : make <target>"
	@echo "target list"
	@echo "  icons"
	@echo "  rename"
	@echo "  dot"
	@echo "  clean"

prepare : fetch extract rename

dot :
	python3 dict2dot.py > example.dot

fetch :
	@if [ ! -e "$(DOC_JPG_ZIP)" ]; then \
		curl -s -L -O $(ZIPURL1); \
	fi
	
	@if [ ! -e "$(3015_JPEG_ZIP)" ]; then \
		curl -s -L -O $(ZIPURL2); \
	fi

extract :
	mkdir -p orig/doc_jpg
	mkdir -p orig/3015_jpeg
	unzip -o $(DOC_JPG_ZIP)   -d orig/doc_jpg
	unzip -o $(3015_JPEG_ZIP) -d orig/3015_jpeg

rename :
	mkdir -p icons/doc_jpg
	mkdir -p icons/3015_jpeg
	python3 jpeg2png.py -o icons/doc_jpg   orig/doc_jpg
	python3 jpeg2png.py -o icons/3015_jpeg orig/3015_jpeg

png : $(PNGFILES)

%.png : %.dot
	dot -Tpng -o $@ $<

pdf : $(PDFFILES)

%.pdf : %.dot
	dot -Tpdf -o $@ $<

debug :
	echo $(DOTFILES)

clean :
	rm -f $(PNGFILES)

.PHONY : \
    all clean prepare png test icons image dot


