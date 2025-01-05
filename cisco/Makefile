SCRIPT = automate.py
HOSTS = cisco

LOGFILE = output.log

all :
	rm -f $(LOGFILE)
	cat show_version.txt \
		| python3 $(SCRIPT) $(HOSTS) \
		| tee -a $(LOGFILE)
	
	cat show_running_config.txt \
		| python3 $(SCRIPT) $(HOSTS) \
		| tee -a $(LOGFILE)

