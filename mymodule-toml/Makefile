all : test

sdist :
	python3 setup.py sdist --formats=xztar

develop :
	python3 setup.py develop --user

dist :
	python3 setup.py bdist_wheel

package :
	python3 -m build
	unzip -t dist/mymodule-0.0.1-py3-none-any.whl

install :
	python3 -m pip install ./dist/mypackage-0.0.1-py3-none-any.whl \
		--force-reinstall --user

uninstall :
	python3 -m pip uninstall mypackage --yes

test :
	pytest

clean :
	rm -rf *.egg-info __pycache__ build dist

mclean :
	$(MAKE) clean
	rm -f *~

.PHONY : \
    all clean dist install uninstall

