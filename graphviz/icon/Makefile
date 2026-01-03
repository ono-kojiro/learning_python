ZIPURL1 = https://www.cisco.com/content/dam/en_us/about/ac50/ac47/doc_jpg.zip
ZIPURL2 = https://www.cisco.com/content/dam/en_us/about/ac50/ac47/3015_jpeg.zip

ZIPFILE1 != basename $(ZIPURL1)
ZIPFILE2 != basename $(ZIPURL2)

all : fetch extract icon

fetch :
	if [ ! -e "$(ZIPFILE1)" ]; then \
		curl -L -O -C - $(ZIPURL1); \
	fi
	if [ ! -e "$(ZIPFILE2)" ]; then \
		curl -L -O -C - $(ZIPURL2); \
	fi

extract :
	mkdir -p orig/doc_jpg
	mkdir -p orig/3015_jpeg
	unzip -n -d orig/doc_jpg $(ZIPFILE1)
	unzip -n -d orig/3015_jpeg $(ZIPFILE2)

icon :
	mkdir -p icons/doc_jpg
	mkdir -p icons/3015_jpeg
	python3 jpeg2png.py -o icons/doc_jpg   orig/doc_jpg
	python3 jpeg2png.py -o icons/3015_jpeg orig/3015_jpeg

.PHONY : \
	all clean test fetch extract ison


