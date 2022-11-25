all : dist

sdist :
	python3 setup.py sdist --formats=xztar

develop :
	python3 setup.py develop --user

dist :
	python3 setup.py bdist_wheel

install :
	python3 -m pip install ./dist/mypackage-0.0.1-py3-none-any.whl \
		--force-reinstall --user

uninstall :
	python3 -m pip uninstall mypackage --yes

test : test1

test1 :
	PYTHONPATH=`pwd` python3 tests/test_import.py

clean :
	rm -rf *.egg-info __pycache__ build dist

.PHONY : \
    all clean dist install uninstall

