TOP_DIR = $(shell pwd)

ENV_NAME = myenv

ACTIVATE = . $(TOP_DIR)/$(ENV_NAME)/bin/activate
PYTHON   = $(ACTIVATE) && python3

PKGNAME     := $(shell cat pyproject.toml | tomlq -r '.project.name')
PKGVERSION  := $(shell cat pyproject.toml | tomlq -r '.project.version')
	
PACKAGE_WHL = $(TOP_DIR)/dist/$(PKGNAME)-$(PKGVERSION)-py3-none-any.whl

DIST_PACKAGES := $(shell /usr/bin/python3 -c "import sysconfig; print(sysconfig.get_paths()['purelib'])")
	
DEST_DIR = work/dest/python3-$(PKGNAME)-$(PKGVERSION)

all : test package

debug :
	ls $(PACKAGE_WHL)
	@echo $(DIST_PACKAGES)

help :
	@echo "usage: make TARGET"
	@echo ""
	@echo "  target:"
	@echo "    prepare"
	@echo "    env"
	@echo "    package"
	@echo "    install"
	@echo "    test"

prepare :
	sudo apt -y install \
		python3-pip python3-venv \
		python3-pytest python3-dotenv \
		python3-build

env :
	if [ ! -d "$(ENV_NAME)" ]; then \
		python3 -m venv $(ENV_NAME); \
	fi

	$(PYTHON) -m pip install -r requirements.txt

module-list :
	$(PYTHON) -m pip list

package :
	$(PYTHON) -m build

install :
	$(PYTHON) -m pip install -e .

test-cli :
	$(PYTHON) -m pytest && which mycli

test : pytest

deb :
	rm -rf $(DEST_DIR)
	mkdir -p $(DEST_DIR)
	mkdir -p $(DEST_DIR)$(DIST_PACKAGES)
	unzip -d $(DEST_DIR)$(DIST_PACKAGES) $(PACKAGE_WHL)
	sh mkdebpkg.sh -p $(PKGNAME) -v $(PKGVERSION) -i $(DEST_DIR) -o dist

check-deb :
	dpkg -c $(PKGNAME)_$(PKGVERSION)_all.deb

__sysinst :
	sudo python3 -m pip install --break-system-packages ./dist/$(PACKAGE_WHL)

__sysuninst :
	sudo python3 -m pip uninstall --break-system-packages $(PKGNAME)

show :
	pip show -f $(PKGNAME)

pytest :
	cd tests && $(PYTHON) -m pytest

.PHONY : \
	all clean test build

