# Configuration

## Basic Configuration
```
$ sudo vi /etc/grafana/grafana.ini
```

```
[server]
protocol = https
http_port = 3000
domain = 192.168.0.XXX
root_url = %(protocol)s://%(domain)s:%(http_port)s/grafana
serve_from_sub_path = true
cert_file = /etc/grafana/mylocalserver.crt
cert_key  = /etc/grafana/mylocalserver.key

[dashboards]
min_refresh_interval = 1s

[auth.ldap]
enabled = true
config_file = /etc/grafana/ldap.toml
allow_sign_up = true
```

## LDAP Configuration
```
$ sudo vi /etc/grafana/ldap.toml
```

```
[[servers]]
host = "192.168.0.XXX"
port = 636
use_ssl = true
start_tls = false
ssl_skip_verify = true

bind_dn = "cn=Manager,dc=example,dc=com"
bind_password = 'xxxxxxxx'
timeout = 10
search_filter = "(cn=%s)"
search_base_dns = ["dc=example,dc=com"]

group_search_filter = "(&(objectClass=posixGroup)(memberUid=%s))"
group_search_base_dns = ["ou=Groups,dc=example,dc=com"]
group_search_filter_user_attribute = "uid"

[servers.attributes]
name = "gecos"
surname = ""
username = "cn"
member_of = "memberOf"
email =  "email"

[[servers.group_mappings]]
group_dn = "cn=grafanaadmin,ou=Groups,dc=example,dc=com"
org_role = "Admin"
grafana_admin = true

[[servers.group_mappings]]
group_dn = "cn=grafanaeditor,ou=Groups,dc=example,dc=com"
org_role = "Editor"

[[servers.group_mappings]]
group_dn = "*"
org_role = "Viewer"
```

## Settings
### HTTP
| Parameter | Value |
|-----------|-------|
| URL  | https://192.168.0.XXX/9200/ |
| Basic auth | Enable |

### Basic Auth Details
| Parameter | Value |
|-----------|-------|
| User  | (USERNAME) |
| Password | (PASSWORD) |

### Elasticsearch details
| Parameter | Value |
|-----------|-------|
| Index name  | [mymetrics-]YYYY.MM.DD |
| Pattern | Daily |
| Time field name | @timestamp |
| ElasticSearch version | 8.0+ |
| Max concurrent Shard Requests | 5 |
| Min time interval | 1s |
| X-Pack enabled | Off |

