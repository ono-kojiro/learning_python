ZIPURL1 = https://www.cisco.com/content/dam/en_us/about/ac50/ac47/doc_jpg.zip
ZIPURL2 = https://www.cisco.com/content/dam/en_us/about/ac50/ac47/3015_jpeg.zip

ZIPURLS = $(ZIPURL1) $(ZIPURL2)

ZIPFILE1 = $(shell basename $(ZIPURL1))
ZIPFILE2 = $(shell basename $(ZIPURL2))

all : extract png

help :
	@echo "usage : make <target>"
	@echo "target list"
	@echo "  fetch"
	@echo "  extract"
	@echo "  png"

fetch :

	curl -L -O $(ZIPURL1)
	curl -L -O $(ZIPURL2)

extract :
	mkdir -p doc_jpg
	mkdir -p 3015_jpeg
	unzip $(ZIPFILE1) -d doc_jpg
	unzip $(ZIPFILE2) -d 3015_jpeg

png :
	mkdir -p doc_png
	mkdir -p 3015_png
	python3 jpeg2png.py -o ./doc_png  doc_jpg
	python3 jpeg2png.py -o ./3015_png 3015_jpeg

clean :
	rm -f doc_png/*.png
	rm -f 3015_png/*.png

mclean :
	$(MAKE) clean
	rm -rf doc_jpg 3015_jpeg doc_png 3015_png
	rm -f *.zip

.PHONY : \
    all clean test fetch extract png



