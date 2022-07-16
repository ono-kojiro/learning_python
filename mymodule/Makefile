all : dist

source :
	python3 setup.py sdist --formats=xztar
	python3 setup.py develop --user

dist :
	python3 setup.py bdist_wheel

install :
	python3 -m pip install ./dist/mymodule-0.0.1-py3-none-any.whl \
		--force-reinstall --user

uninstall :
	python3 -m pip uninstall mymodule --yes

test : test1 test2

test1 :
	PYTHONPATH=`pwd` python3 tests/test.py

test2 :
	cd tests && python3 test.py

clean :
	rm -rf *.egg-info __pycache__ build dist

.PHONY : \
    all clean dist install uninstall

