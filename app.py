import os
import subprocess
import threading
import logging
import importlib

import yaml

import alfonsiot

BASE_PATH = "/usr/local/alfonslistener"
CONF_PATH = os.path.join(BASE_PATH, "config.yaml")
SCRIPT_PATH = os.path.join(BASE_PATH, "scripts")

# Testing SCRIPT_PATH since it's the deepest folder
if not os.path.exists(SCRIPT_PATH):
	os.makedirs(SCRIPT_PATH)

# Set up logging
logger = logging.getLogger("listener")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(os.path.join(BASE_PATH, "log.log"))
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)
# - - - - -

def _onConnect(iot):
	logger.info("Connected!")

	for c in config["commands"]:
		logger.debug("Subscribing to " + c["topic"])
		iot.subscribe(c["topic"])

def _onMessage(iot, topic, payload):
	logger.debug("Received message on topic '{}', with payload '{}'".format(topic, payload))

	for c in config["commands"]:	
		if c["topic"] == topic:
			pReturn = None

			if "python" in c:
				p = c["python"].split(":", 1)
				pName = p[0]
				pFunc = p[1]
				pLocation = os.path.join(BASE_PATH, "scripts", pName + ".py")
				
				try:
					pSpec = importlib.util.spec_from_file_location(pName, pLocation)
					pModule = importlib.util.module_from_spec(pSpec)
					pSpec.loader.exec_module(pModule)
				except Exception as e:
					logger.warning("Couldn't import the python file. Exception '{}'".format(e))

				logger.info("Running python script '{}'".format(c["python"]))

				try:
					pReturn = str(getattr(pModule, pFunc)(topic, payload))
				except Exception as e:
					logger.warning("Python script crashed with exception '{}'".format(e))
				else:
					logger.debug("Python script excited with '{}'".format(pReturn))

			if "script" in c and "python" in c and pReturn == None:
				logger.info("Python script returned with None, script will be skipped...")

			if "script" in c:
				sExec, sArgs = c["script"].split(" ", 1)

				cmd = os.path.expanduser(sExec) + " " + sArgs .replace("%payload%", payload if not pReturn else pReturn)

				logger.info("Executing '$ " + cmd + "'")
				threading.Thread(target=_runScript, args=(cmd,)).start()

def _runScript(cmd):
	try:
		result = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
	except Exception as e:
		logger.warning("Exited with exception: \n\t{}".format(e))
	else:
		logger.debug("Exited with '{}'".format(result.stdout.decode("utf-8").replace("\n", " \\n ")))

def main():
	global config

	if not os.path.exists(CONF_PATH) or not os.path.isfile(CONF_PATH):
		logger.info("No config file found at '{}'".format(CONF_PATH))
		return
	
	with open(CONF_PATH) as f:
		config = yaml.safe_load(f)
	
	logger.info("Read config")

	info = config["info"]

	_username = info["username"] if "username" in info else None
	_password = info["password"] if "password" in info else None

	logger.info("Connecting...")
	iot = alfonsiot.AlfonsIoT(server=info["server"], username=_username, password=_password)
	iot.start()

	iot.onConnect = _onConnect
	iot.onMessage = _onMessage

	try:
		logger.info("Locking...")
		lock = threading.Lock()
		lock.acquire()
		lock.acquire()
	except KeyboardInterrupt:
		pass

if __name__ == "__main__":
	main()
