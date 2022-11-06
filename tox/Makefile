all : build

sdist :
	python3 setup.py sdist --formats=xztar

develop :
	python3 setup.py develop --user

build :
	python3 setup.py build

dist :
	python3 setup.py bdist_wheel

install :
	python3 -m pip install ./dist/mymodule-0.0.1-py3-none-any.whl \
		--force-reinstall --user

uninstall :
	python3 -m pip uninstall mymodule --yes

test : check

check :
	tox

clean :
	rm -rf *.egg-info __pycache__ build dist

.PHONY : \
    all clean dist install uninstall

