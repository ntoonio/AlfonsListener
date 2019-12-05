import os
import threading
import yaml
import subprocess
from shlex import split
import logging
import alfonsiot

PATH = os.path.dirname(os.path.realpath(__file__)) + "/"

# Set up logging
logger = logging.getLogger("listener")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(PATH + "listener.log")
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

with open(PATH + "config.yaml") as f:
	config = yaml.safe_load(f)

def switch(data, command):
	state = int(data == "ON")
	
	command = command.replace("%state%", str(state))
	x = split(command)
	
	executable = PATH + x[0]
	args = x[1:]
	
	cmd = [executable, *args]
	logger.info("Executing " + " ".join(cmd))

	result = subprocess.run(cmd, stdout=subprocess.PIPE)
	r = result.stdout
	logger.info("Exited with '{}'".format(r.decode("utf-8").replace("\n", "\\n")))

def onMessage(topic, payload):
	logger.info("Got message at: " + str(topic))

	for c in config["commands"]:
		if c["subscribe"] == topic:
			threading.Thread(target=switch, args=(payload, c["script"],)).start()

def onConnect(client, userdata, flags, rc):
	logger.info("Connected!")

	for c in config["commands"]:
		iot.subscribe(c["subscribe"], onMessage)

def onDisconnect(client, userdata, rc):
	logger.info("Disconnected... rc: " + str(rc))

logger.info("Did setup")

iot = alfonsiot.AlfonsIoT(host="alfons.antoon.io", port=443, username="iot-rf-listener", password="iot", ssl=True)
iot.mqttOnConnect = onConnect
iot.mqttOnDisconnect = onDisconnect
iot.start()

try:
	l = threading.Lock()
	l.acquire()
	l.acquire()
except KeyboardInterrupt:
	logger.info("Keyboard interrupt - exiting")

