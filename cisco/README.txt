# ssh config

Host cisco
  Hostname 192.168.0.xxx
  KexAlgorithms +diffie-hellman-group-exchange-sha1,diffie-hellman-group1-sha1,diffie-hellman-group14-sha1
  HostKeyAlgorithms +ssh-rsa,ssh-dss

# snmp v3 example

  $ snmpwalk -c 3 -u snmpuser \
      -a SHA-256 \
      -l authNoPriv \
      -A snmppass \
      192.168.0.249 1.3.6.1.2.1.1

