HTMLFILES = 57228_58735.html \
			56680_62855.html 56669_58756.html 56689_63891.html \
			57108_60897.html 56684_65242.html

all : fetch 

fetch :
	@for filename in $(HTMLFILES); do \
		if [ ! -e "$${filename}" ]; then \
			echo "Download $${filename}"; \
			wget --quiet https://www.aozora.gr.jp/cards/001779/files/$${filename}; \
		else \
			echo "Skip $${filename}"; \
		fi \
	done

clean :
	rm -f $(HTMLFILES)

