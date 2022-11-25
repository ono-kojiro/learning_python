URL = https://github.com/spdx/spdx-examples.git

all :
	python3 setup.py build

prepare :
	@if [ ! -e "spdx-examples" ]; then \
    	git clone $(URL); \
	else \
    	echo skip git clone; \
	fi

clean :
	rm -rf *.egg-info __pycache__ build dist

check test :
	tox

.PHONY : \
	all clean test check prepare

