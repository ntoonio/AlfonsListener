# Alfons Listener
Simple program for listening on a topic and when it's received running a script.

## Setup
### config.yaml
	info:
	    host: "host"
	    port: 443
	    username: "username"
	    password: "iot"
	    ssl: True

	commands:
	  - subscribe: topic
	    script: "script-to-run"
	  - subscribe: topic2
	    script: "script-to-run2"

### Creating a daemon

	$ ./service_install.sh

If you want to install the service under a name other than "alfonslistener" you can change the `name` variable on the top of the file.
