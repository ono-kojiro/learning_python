all :
	$(MAKE) -C read_json
	$(MAKE) -C japanese
	$(MAKE) -C mkdatabase

clean :
	$(MAKE) -C read_json  clean
	$(MAKE) -C japanese   clean
	$(MAKE) -C mkdatabase clean


