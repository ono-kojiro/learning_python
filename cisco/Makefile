SCRIPT = automate.py
HOSTS = cisco

LOGFILE = output.log

all :
	rm -f $(LOGFILE)
	cat show_version.rc \
		| python3 $(SCRIPT) $(HOSTS) \
		| tee -a $(LOGFILE)
	
	cat show_running_config.rc \
		| python3 $(SCRIPT) $(HOSTS) \
		| tee -a $(LOGFILE)

