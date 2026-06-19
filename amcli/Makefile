all : init

prepare :
	python3 -m pip install -r requirements.txt

init :
	rm -rf work/
	mkdir -p work
	amcli startproject myproject --dir work/
	amcli startapp     myapp --dir work/
	amcli installapp   myapp --project work/myproject/

mclean :
	rm -rf work

