all : init

prepare :
	python3 -m pip install -r requirements.txt

init :
	rm -rf work/
	mkdir -p work
	amcli startproject myproject --dir work/

